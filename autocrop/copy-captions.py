import os
import shutil
import sys

if __name__ == '__main__':
    in_dir, out_dir = sys.argv[1], sys.argv[2]
    for root, _, files in os.walk(in_dir):
        for file in files:
            if file.endswith('.txt'):
                continue
            img_rel_path = os.path.relpath(os.path.join(root,file), in_dir)
            out_img_path = os.path.join(out_dir, img_rel_path)
            if not os.path.exists(out_img_path):
                continue
            fn, _ = os.path.splitext(file)
            cap_file = os.path.join(root, fn+'.txt')
            if os.path.exists(cap_file):
                cap_rel_path = os.path.relpath(cap_file, in_dir)
                target = os.path.join(out_dir, cap_rel_path)
                tar_root, _ = os.path.split(target)
                os.makedirs(tar_root, exist_ok=True)
                shutil.copyfile(cap_file, target)
