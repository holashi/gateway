# test model_info.py

import sys
sys.path.extend(["..","."])
import model_info 

if __name__ =="__main__":

# test model_info.model_setting

    model_setting_f = "../../model_connect_setting/wzs_p3_m1.json"
    print("model_setting file: ",model_setting_f)
    # output : ../../model_connect_setting/wzs_p3_m1.json
    model_setting_ob = model_info.model_setting(model_setting_f) 
    print("model_setting_ob.result_type:",model_setting_ob.result_type)
    # output : [{'0': 'NG-MoreComponent', '1': 'NG-NoneComponent', '2': 'NG-OutsidePosition', '3': 'NG-UpsideDown', '4': 'OK'}]
    print("model_setting_ob.get_connect_info(\"rest\"):",model_setting_ob.get_connect_info("rest"))
    # output : {'tfs_method': 'rest', 'signature_name': 'classification', 'tfserving_rest': '10.34.127.5:48501', 'model_input_name': 'string_array', 'model_output_name': 'output_node'}


# test model_info.model_setting_grpc

    model_name = "wzs_p3_m1"
    model_setting_grpc_ob = model_info.model_setting_grpc(model_name,"../../model_connect_setting/wzs_p3_m1.json")
    # output : model_setting_grpc_ob = model_info.model_setting_grpc(model_name)
    print("model_name:",model_setting_grpc_ob.model_name)
    # output : wzs_p3_m1
    print("grpc_url:",model_setting_grpc_ob.grpc_url)
    # output : 10.34.127.5:48500
    print("grpc_signature_name:",model_setting_grpc_ob.grpc_signature_name)
    # output : classification
    print("grpc_model_input_name:",model_setting_grpc_ob.grpc_model_input_name)
    # output : string_array
    print("grpc_model_output_name:",model_setting_grpc_ob.grpc_model_output_name)
    # ooutput : utput_node


# test model_class_map
    
    import os
    os.chdir("./..")
    model_class_map = model_info.model_class_map(model_name)
    print("model_class_map.get_class_mapping_dic()",model_class_map.get_class_mapping_dic())
    # output : model_class_map.get_class_mapping_dic() {'0': 'NG-MoreComponent', '1': 'NG-NoneComponent', '2': 'NG-OutsidePosition', '3': 'NG-UpsideDown', '4': 'OK'}