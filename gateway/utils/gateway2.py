#  Assume data_receive with the format as follow:
#    {
#       "instance":[
#           // image 1
#               {
#                   "image":{"b64":....},
#                   "comp":"A213",
#                   "SN":0001
#                },
#           // image 2 
#               {
#                   "image":{"b64":....}",
#                   "comp":"B223",
#                   "SN":0002
#                }
#           ]
#      }
#
#  Gateway receive data_received and use comp_dispatch/XX.json to create comp_model map.
#  Then, based on the comp_model map and the data_received["comp"], gateway dispatch 
#  data_received["image_list"] to the corresponding model
# import my lib

# from comp_dispatch import comp_dispatch
import model_info
import grpc_tools
import tools
import argparse
import numpy as np

# optional: map result to corresponding class
def _get_class_map(model_name):
    model_result_type_ob = model_info.model_class_map(model_name)
    return model_result_type_ob.model_result_type

# map grpc_result into fomat :
# [(max_sc,max_sc_mapping_result),(max_sc,max_sc_mapping_result),......]
# ,and each tupple represent a instance.

def _grpc_result_mapping(grpc_response,class_map):
    return [(np.max(inst),class_map[str(np.argmax(inst))]) for inst in grpc_response] 

# _json_to_grpc_dic():
# create the diction with the necessary information for grpc_request with the payload received in json format
# The input is data_received["instance"]
# The return diction with the format
# { "comp_code1":{
#               "image":[image1,image2...],
#               "comp":[comp1,comp2...],
#               "sn":[sn1,sn2...]
#           },
#    "comp_code2":{
#               "image":[image1,image2...],
#               "comp":[comp1,comp2...],
#               "sn":[sn1,sn2...]
#            },
# }
def _json_to_grpc_dic(payload_json_instance):
    grpc_data_dic= {}
    for ins in payload_json_instance:
        if ins['comp'][0] not in list(grpc_data_dic.keys()):
            grpc_data_dic[ins['comp'][0]]={}
            for k in ins.keys():
                if k =="image":
                    grpc_data_dic[ins['comp'][0]][k]=[ins[k]["b64"]]
                else:
                    grpc_data_dic[ins['comp'][0]][k]=[ins[k]]
        else:
            for k in ins.keys():
                    if k =="image":
                            grpc_data_dic[ins['comp'][0]][k].append(ins[k]["b64"])
                    else:
                        grpc_data_dic[ins['comp'][0]][k].append(ins[k])
    return grpc_data_dic
  
# comps_info is the dict {
#           "comp_code1":["model_name1","model_name2"],
#           "comp_code2":["model_name.."]
# }    
    

# The return grpc_response is in the format:
#  {
#    'model_1':[(instance1_model1_max_score,instance1_model1_mapping_result),
#               (instance2_model1_max_score,instance2_model1_mapping_result),
#               (),()...],
#    'model_2':[(instance1_model2_max_score,instance1_model2_mapping_result),
#               (instance2_model2_max_score,instance2_model2_mapping_result),
#               (),()...],
#    'model_3':...
#  }
# !! Notice: len(response_dict['model_1']) == len(response_dict['model_2']) == len(response_dict['model_3']) 
def _grpc_sender(data_received,comps_info_ob):
    grpc_response = {}
  
    # buffer_data[comp_code]["image"] is the image list used in grpc_request, ex: [image1,image2,...]
    # Important assume size of data_receive < 4MB, that is maximum size of grpc payload.
    buffer_data = _json_to_grpc_dic(data_received["instance"])

    for comp_code in buffer_data.keys():
        grpc_response[comp_code]={}
        if comp_code not in comps_info_ob.get_comp_lists():
            print("invalid component code")
            return None
        else:
        # comps_info_ob.get_comp_models(comp_code) should be the list like ['model_name1','model_name2']
            for model_name in comps_info_ob.get_comp_models(comp_code):
                model_info_grpc_ob = model_info.model_setting_grpc(model_name)
                class_map = _get_class_map(model_name)
                grpc_raw_response=grpc_tools.grpc_request(model_info_grpc_ob,buffer_data[comp_code]["image"])
                grpc_response[comp_code][model_name] = _grpc_result_mapping(grpc_raw_response,class_map)
    
    return grpc_response
    
    
# return list is in the format:
# [{'type_of_instance1':score_of_instance1},
#  {'type_of_instance2':score_of_instance2},
#  ...
# ]
def _grpc_result_integration_by_comps(grpc_response_one_comp):
    gateway_response = []
    model_names = list(grpc_response_one_comp.keys())
    for i in range(len(grpc_response_one_comp[model_names[0]])):
        tmp_sc = 0
        tmp_result_type = None
        for model in model_names:
            if tmp_sc<grpc_response_one_comp[model][i][0]:
                tmp_sc=grpc_response_one_comp[model][i][0]               # score
                tmp_result_type = grpc_response_one_comp[model][i][1]    # result type
        gateway_response.append({tmp_result_type:tmp_sc})
    return gateway_response

def _grpc_result_integration(grpc_response_dic):
    return_buf = {}
    for comp in list(grpc_response_dic.keys()):
        return_buf[comp]=_grpc_result_integration_by_comps(grpc_response_dic[comp])
    return return_buf
    

def _rest_sender(data_received,comps_info_ob):
    pass

# main gateway function 

def gateway(mode,data_received,comps_info_ob):

    if mode =="grpc":
        data_received_grpc=data_received
        return _grpc_sender(data_received_grpc,comps_info_ob)
    elif mode =="rest":
        data_received_rest=lambda rest:data_received
        return _rest_sender(data_received_rest,comps_info_ob)

# For chunking list of protobuf to small piece which is the same as the final dense of softmax
def chunks(unchunks_list, size_after):
    # For item i in a range that is a length of size_after,
    for i in range(0, len(unchunks_list), size_after):
        # Create an index range for unchunks_list of size_after items:
        yield unchunks_list[i:i+size_after]
