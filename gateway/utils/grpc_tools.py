# reference https://github.com/tensorflow/serving/blob/master/tensorflow_serving/example/mnist_client.py
# important : it should be very careful when deal with payload size while useing proto buffer

# model_info: model_info.model_setting_grpc object with features example:
# model_name: model_1
# grpc_url: host:port
# grpc_signature_name: classification
# grpc_model_input_name: string_array
# grpc_model_output_name: output_node
# images_list : list contains images [image1,image2...]
#
# grpc proto buf result:
#   ex :image_list :[img1,img2,img3]
#       predict class : 2
#       grpc response [img1_score1,img1_score2,
#                      img2_score1,img2_score2,
#                      img3_score1,img3_score2
#                       ]

import grpc
import numpy as np
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

#import my tools
import model_info
import tools

# group grpc response by instance : 
# map response from format: [img1_sc1,img1,sc_2,..,img2_sc1,img2_sc2,...] 
# into format: [[img1_sc1,img1,sc_2,..],[img2_sc1,img2_sc2,...],...] 

def _group_grpc_result_by_instance(response,output_node):
    result = []
    result_batch_size = response.outputs[output_node].tensor_shape.dim[0].size
    response_val_size = len(response.outputs[output_node].float_val)
    
    for i in range(result_batch_size):
        result.append(response.outputs[output_node].float_val[i*round(response_val_size/result_batch_size):(i+1)*round(response_val_size/result_batch_size)])
    return result

def grpc_request(model_info,images_list):
    time_out = 20

    channel = grpc.insecure_channel(model_info.grpc_url)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    request = predict_pb2.PredictRequest()
    request.model_spec.signature_name = model_info.grpc_signature_name 
    request.model_spec.name = model_info.model_name 
   
   # it should be very careful when deal with payload size while useing proto buffer
    request.inputs[model_info.grpc_model_input_name].CopyFrom(
        tf.compat.v1.make_tensor_proto(images_list, shape=[len(images_list)])
        )
    response = stub.Predict(request, time_out)
    #result with the format [[image_1_sc1,image1_sc2..],[image2_sc1,image2_sc2,...]....]
    result = _group_grpc_result_by_instance(response,model_info.grpc_model_output_name)
    
    return result 
