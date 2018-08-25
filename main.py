from multiprocessing import Pool
import multiprocessing as multi
from PIL import Image
import traceback
import argparse
import os

from openslide import OpenSlide


def _get_concat_h(img_lst):
    width, height, h = sum([img.width for img in img_lst]), img_lst[0].height, 0
    dst = Image.new('RGB', (width, height))
    for img in img_lst:
        dst.paste(img, (h, 0))
        h += img.width
    return dst

def _get_concat_v(img_lst):
    width, height, v = img_lst[0].width, sum([img.height for img in img_lst]), 0
    dst = Image.new('RGB', (width, height))
    for img in img_lst:
        dst.paste(img, (0, v))
        v += img.height
    return dst

def convert(data):
    UNIT_X, UNIT_Y = 5000, 5000
    try:
        fname, input_dir, output_dir = data
        save_name = fname.split(".")[0] + ".jpg"
        print("Processing : %s"%fname)
        os_obj = OpenSlide(input_dir+"/"+fname)
        w, h = os_obj.dimensions
        w_rep, h_rep = int(w/UNIT_X)+1, int(h/UNIT_Y)+1
        w_end, h_end = w%UNIT_X, h%UNIT_Y
        w_size, h_size = UNIT_X, UNIT_Y
        w_start, h_start = 0, 0
        v_lst = []
        for i in range(h_rep):
            if i == h_rep-1:
                h_size = h_end 
            h_lst = []
            for j in range(w_rep):
                if j == w_rep-1:
                    w_size = w_end
                img = os_obj.read_region((w_start,h_start), 0, (w_size,h_size))
                img = img.convert("RGB")
                h_lst.append(img)
                w_start += UNIT_X
            v_lst.append(h_lst)
            w_size = UNIT_X
            h_start += UNIT_Y
            w_start = 0
        concat_h = [_get_concat_h(v) for v in v_lst]
        concat_hv = _get_concat_v(concat_h)
        concat_hv.save(output_dir+"/"+save_name)
    except:
        print("Can't open image file : %s"%fname)
        traceback.print_exc()
    return    

def main():
    parser = argparse.ArgumentParser(description='This script is ...'
                                    , formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--input", "-i", default="./input",
                        help="Directory name where the input image is saved. default='./input'")
    parser.add_argument("--output", "-o", default="./output",
                        help="Directory name where the converted image is saved. default='./output'")
    parser.add_argument("--multi", "-m", type=int, default=2,
                        help="Number of CPU cores to use for conversion. default=2")

    args = parser.parse_args()
    print("------- Program Started -------")

    try:
        f_lst = sorted([f for f in os.listdir(args.input) if ".svs" in f])
        f_lst = [[f,args.input,args.output] for f in f_lst]
        p = Pool(args.multi)
        print("------- Convert Started -------")
        p.map(convert, f_lst)
        print("------- Convert Ended -------")
        p.close()
    except:
        traceback.print_exc()
    
    print("------- Program Ended -------")
    return


if __name__ == "__main__":
    main()
