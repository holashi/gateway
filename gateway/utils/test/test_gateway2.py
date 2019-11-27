# test gateway2.py


import sys
import os

sys.path.extend(["..","."])
import gateway2
import tools
os.system('clear')

if __name__ =='__main__':
    os.chdir('./..')
    model_name = 'wzs_p3_m1'
#    print('test model name:',model_name)

# test _get_class_map

    class_map = gateway2._get_class_map(model_name)
#    print("gateway2._get_class_map():\n",class_map)
    #  output : {'0': 'NG-MoreComponent', '1': 'NG-NoneComponent', '2': 'NG-OutsidePosition', '3': 'NG-UpsideDown', '4': 'OK'}
    

# test _grpc_result_mapping
    grpc_response = [[0.01,0.02,0.03,0.04,0.9],
                     [0.01,0.02,0.03,0.9,0.04],
                     [0.01,0.02,0.9,0.03,0.04],
                     [0.01,0.9,0.02,0.03,0.04],
                     [0.9,0.01,0.02,0.03,0.04],
                    ]
    grpc_result_mapping = gateway2._grpc_result_mapping(grpc_response,class_map)
#    print("gateway2._grpc_result_mapping():\n",grpc_result_mapping)
    # output : [(0.9, 'OK'), (0.9, 'NG-UpsideDown'), (0.9, 'NG-OutsidePosition'), (0.9, 'NG-NoneComponent'), (0.9, 'NG-MoreComponent')]

# test _json_to_grpc_dic
    img_path =  "/Users/harveyshi/wistron/github/aoi_gateway/images/bmp/CN01W26NWS2009920156A00_PT5101_41.bmp"
    img2_path = "/Users/harveyshi/wistron/github/aoi_gateway/images/png/CN01W26NWS200993001JA00_PT4504_0_NA_NA.png"
    image1 = tools.resize_and_serialize_image(img_path,20,20)
    image2 = tools.resize_and_serialize_image(img2_path,20,20)
    
    instance_1 = {"image":{"b64":image1},"comp":"A001","SN":'0001'}
    instance_2 = {"image":{"b64":image2},"comp":"A002","SN":'0002'}
    instance_3 = {"image":{"b64":image2},"comp":"E003","SN":'0003'}
    data_received = {
        "instance":[instance_1,instance_2,instance_3]
    }
    json_to_grpc_dic = gateway2._json_to_grpc_dic(data_received['instance'])
#    print("_json_to_grpc_dic():",json_to_grpc_dic)
    # output :{ "A":{
    #               "image":[b'iVBORw0KG...Jggg==', b'iVBO...ggg==']
    #               comp': ['A001', 'A002'],
    #               'SN': ['0001', '0002']
    #           },
    #           "E":{
    #               "image":[b'iVBORw0KGg...rkJggg=='],
    #               "comp":['E003'],
    #               "sn":['0003']
    #            },
    # }


# test _grpc_sender
    from comp_dispatch import comp_dispatch
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--comp-dispatch","-cd",default="../comp_dispatch/test_board.json",help="default board information with which components should be test")
    args,_ = parser.parse_known_args()
    comps_info_ob = comp_dispatch(args.comp_dispatch)
    grpc_response = gateway2._grpc_sender(data_received,comps_info_ob)
    print("_grpc_sender:",grpc_response)
    # output : {'A': {'wzs_p3_m1': [(0.9350354671478271, 'NG-NoneComponent'), (0.9350354671478271, 'NG-NoneComponent')], 
    #                 'wzs_p3_m2': [(0.9829896092414856, 'OK'), (0.7041807174682617, 'NG-MoreComponent')]}, 
    #           'E': {'wzs_p3_m1': [(0.9350354671478271, 'NG-NoneComponent')]}
    #          }


# test _grpc_result_integration_by_comps
    grpc_response_one_comp=grpc_response[list(grpc_response.keys())[0]]
    _grpc_result_integration_by_comps = gateway2._grpc_result_integration_by_comps(grpc_response_one_comp)
    print('_grpc_result_integration_by_comps:',_grpc_result_integration_by_comps)
    # output : [{'OK': 0.9829896092414856}, {'NG-NoneComponent': 0.9350354671478271}]


# test _grpc_result_integration
    grpc_result_integration = gateway2._grpc_result_integration(grpc_response)
    print("grpc_result_integration:",grpc_result_integration)
    # output : {'A': [{'OK': 0.9829896092414856}, {'NG-NoneComponent': 0.9350354671478271}], 'E': [{'NG-NoneComponent': 0.9350354671478271}]}


# test gateway with mode "grpc"

    mode = "grpc"
    gateway_response = gateway2.gateway(mode,data_received,comps_info_ob)
    print("gateway_response:",gateway_response)
    # output : {'A': {'wzs_p3_m1': [(0.9350354671478271, 'NG-NoneComponent'), (0.9350354671478271, 'NG-NoneComponent')], 
    #                 'wzs_p3_m2': [(0.9829896092414856, 'OK'), (0.7041807174682617, 'NG-MoreComponent')]}, 
    #           'E': {'wzs_p3_m1': [(0.9350354671478271, 'NG-NoneComponent')]}
    #          }


# demo response to client from gateway

    response_to_client = gateway2._grpc_result_integration(gateway_response)
    print("response_to_client:",response_to_client)
    # output : response_to_client: {'A': [{'OK': 0.9829896092414856}, {'NG-NoneComponent': 0.9350354671478271}], 
    #                               'E': [{'NG-NoneComponent': 0.9350354671478271}]}