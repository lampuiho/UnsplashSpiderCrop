import os
import shutil
import sys

if __name__ == '__main__':
    in_dir, out_dir = sys.argv[1], sys.argv[2]
    out_set = []
    for root, _, files in os.walk(out_dir):
        for file in files:
            if file.endswith('.txt'):
                continue
            img_rel_path = os.path.relpath(os.path.join(root,file), out_dir)
            fn, _ = os.path.splitext(file)
            if not os.path.exists(os.path.join(root,fn+'.txt')):
                cap_rel_path, _ = os.path.splitext(img_rel_path)
                cap_rel_path += '.txt'
                src = os.path.join(in_dir, cap_rel_path)
                tar = os.path.join(out_dir, cap_rel_path)
                if os.path.exists(src):
                    shutil.copyfile(src, tar)
