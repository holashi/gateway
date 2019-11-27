# test groc_tools.py
# important : it should be very careful when deal with payload size while useing proto buffer
# this sample use grpc and send two images to the model server
import sys
sys.path.extend(["..","."])

import grpc
import base64
import io
from PIL import Image
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

#my tools
import tools
import grpc_tools
import model_info


if __name__=="__main__":



    img_path =  "/Users/harveyshi/wistron/github/aoi_gateway/images/bmp/CN01W26NWS2009920156A00_PT5101_41.bmp"
    img2_path = "/Users/harveyshi/wistron/github/aoi_gateway/images/png/CN01W26NWS200993001JA00_PT4504_0_NA_NA.png"
    img3_path = "/Users/harveyshi/wistron/github/aoi_gateway/images/bmp/Cw123213.bmp"
    image1 = tools.resize_and_serialize_image(img_path,30,30)
    image2 = tools.resize_and_serialize_image(img2_path,30,30)
    image3 = tools.resize_and_serialize_image(img3_path,30,30)
    images_list = [image1,image2,image3]

    model_info_config_path = "/Users/harveyshi/wistron/github/aoi_gateway/gateway_v2.0/model_connect_setting/wzs_p3_m1.json"
    model_info_ob = model_info.model_setting_grpc("wzs_p3_m2",model_info_config_path)
    
    
    result = grpc_tools.grpc_request(model_info_ob,images_list)
    print("grpc_tools.grpc_request(model_info_ob,images_list)",result)
    
    # [[0.12424355745315552, 0.8757564425468445], [0.9643155336380005, 0.0356844887137413], [0.12424355745315552, 0.8757564425468445]]
