# test tools.py

import sys
sys.path.extend(["..","."])
import tools


if __name__=="__main__":
    img_path = "/Users/harveyshi/wistron/github/aoi_gateway/images/png/CN01W26NWS200993001JA00_PT4504_0_NA_NA.png"
    
    
    image_open_and_serialize_image = tools.open_and_serialize_image(img_path)
    print("image_open_and_serialize_image:")
    print("\ttype:\t",type(image_open_and_serialize_image))
    # output : type:    <class 'str'>
    print("\timages:",image_open_and_serialize_image)
    # output : images: iVBORw0KGgoAAAANSUhEUgAAAF....AAAAElFTkSuQmCC

    image_resize_and_serialize = tools.resize_and_serialize_image(img_path,30,30)
    print("image_resize_and_serialize:")
    print("\ttype:\t",type(image_resize_and_serialize))
    # output :  type:    <class 'bytes'>
    print("\timages:",image_resize_and_serialize)
    # output : images: b'iVBORw0KGgoAAAANSUhEUgAAA...Mn2DD6wAAAABJRU5ErkJggg=='