from __future__ import annotations
import dataclasses
import os
from multiprocessing import JoinableQueue, Process
from PIL import Image
from ultralytics import YOLO
from ultralytics.nn.tasks import DetectionModel
from ultralytics.engine.results import Results

class Signal:
    def __init__(self):
        self.running = True
    def stop(self):
        self.running = False
@dataclasses.dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int

def alpha_to_color(image: Image.Image, color=(255, 255, 255)):
    """Alpha composite an RGBA Image with a specified color.

    Simpler, faster version than the solutions above.

    Source: http://stackoverflow.com/a/9459208/284318

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """
    image.load()  # needed for split()
    background = Image.new('RGB', image.size, color)
    background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
    return background
def has_transparency(img: Image.Image):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True
    return False
def expand_width_centered(rect: Rect, width: int):
    rect.x -= (width - rect.w)//2
    rect.w = width
def expand_height_centered(rect: Rect, height: int):
    rect.y -= (height - rect.h)//2
    rect.h = height
def scale_rect_centered(rect: Rect, scale: float):
    # scale must be <= 1
    scaled_w = int(scale*rect.w)
    scaled_h = int(scale*rect.h)
    rect.x += (rect.w - scaled_w)//2
    rect.y += (rect.h - scaled_h)//2
    rect.w = scaled_w
    rect.h = scaled_h
def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))
# this deals with the zoom and saving in a seperate thread than detection model
def crop_consumer(sig: Signal, q: JoinableQueue[tuple[str, Image.Image, Rect]], in_dir: str, out_dir: str, dims: list[int], border_ratio: float):
    while sig.running:
        path, img, rect = q.get()
        rel_path = os.path.relpath(path, in_dir)
        print(f'Cropping {path}, {(img.width, img.height)}, {(rect.x, rect.y, rect.w, rect.h)}')
        for dim in dims:
            if img.width<dim or img.height<dim:
                continue
            crop_box = dataclasses.replace(rect)
            expand_width_centered(crop_box, int(crop_box.w/(1-border_ratio)))
            expand_height_centered(crop_box, int(crop_box.h/(1-border_ratio)))
            if crop_box.w > dim or crop_box.h > dim:
                if crop_box.w > crop_box.h:
                    if crop_box.w > img.height:
                        tmp = Image.new(img.mode, (img.width, crop_box.w), (255, 255, 255))
                        tmp.paste(img, (0, (crop_box.w-img.height)//2))
                        img = tmp
                    expand_height_centered(crop_box, crop_box.w)
                else:
                    crop_box.h = min(crop_box.h, img.width)
                    expand_width_centered(crop_box, crop_box.h)
            if crop_box.w < dim:
                expand_width_centered(crop_box, dim)
            if crop_box.h < dim:
                expand_height_centered(crop_box, dim)
            crop_box.x = clamp(crop_box.x, 0, img.width-crop_box.w)
            crop_box.y = clamp(crop_box.y, 0, img.height-crop_box.h)

            out_img_path = os.path.join(out_dir, f'{dim}', rel_path)
            print(f'Cropped {out_img_path} to {(crop_box.x, crop_box.y, crop_box.w, crop_box.h)}')
            crop_box = (crop_box.x, crop_box.y, crop_box.w+crop_box.x, crop_box.h+crop_box.y)
            cropped = img.crop(crop_box)
            folder, _ = os.path.split(out_img_path)
            os.makedirs(folder,exist_ok=True)
            cropped.save(out_img_path)
        q.task_done()
    # process killed as daemon on main thread return
def detect_consumer(sig: Signal, det_q: JoinableQueue[str, Image.Image], crop_q: JoinableQueue[tuple[str, Image.Image, Rect]], model: DetectionModel):
    while sig.running:
        path, img = det_q.get()
        print(f'Detecting {path}')
        detect_res: Results = model(path)[0]
        detect_res.names
        human_indices = [i for i, cl in enumerate(detect_res.boxes.cls.cpu().numpy()) if detect_res.names[cl]=='person']
        if len(human_indices) == 1:
            x,y,x2,y2 = map(int,detect_res.boxes.xyxy[human_indices[0]].cpu().numpy())
            w,h = x2-x, y2-y
            crop_q.put((path, img, Rect(x,y,w,h)))
        det_q.task_done()
class AutoZoom:
    """
    @dims square dimension of the output picture
    @min_person_ratio how much portion of the area the person must occupy when zooming out the picture
    """
    def __init__(self, input_dir: str, output_dir: str, dims=[1024], min_border_ratio=0.1):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.dims = dims
        self.min_border_ratio = min_border_ratio
        exts = Image.registered_extensions()
        self.exts = {ex for ex, f in exts.items() if f in Image.OPEN}
    def __call__(self) -> os.Any:
        sig = Signal()
        in_dir, out_dir, dims, min_ratio = self.input_dir, self.output_dir, self.dims, self.min_border_ratio
        det_q = JoinableQueue()
        crop_q = JoinableQueue()
        min_dim = min(*dims) if len(dims)>1 else dims[0]
        model = YOLO('./pretrained/yolo11x.pt')
        p_det = Process(target=detect_consumer, args=(sig, det_q, crop_q, model), daemon=True) #make this number of GPU
        p_crops = [Process(target=crop_consumer, args=(sig, crop_q, in_dir, out_dir, dims, min_ratio), daemon=True) for _ in range(2)] #make this number of CPU
        p_det.start()
        for p in p_crops:
            p.start()
        for root, _, files in os.walk(in_dir):
            for file in files:
                _, ext = os.path.splitext(file)
                if not ext in self.exts:
                    continue
                img_path = os.path.join(root, file)
                try:
                    img = Image.open(img_path)
                    img.verify()
                except:
                    continue
                img = Image.open(img_path)
                if img.width>=min_dim and img.height>=min_dim:
                    det_q.put((img_path, img))
        det_q.join()
        crop_q.join()
        sig.stop()
if __name__ == '__main__':
    func = AutoZoom('./output/blonde-woman', './output/cropped-blonde-woman')
    func()