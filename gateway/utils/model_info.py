# This module defines classes shows following:
#  
#  model_setting      : Base method to get model infomatino with given comp_dispatch_file
#  
#  model_setting_grpc : Base method to get model infomation for grpc with given model name. 
#                       Once given the model name, this class serchs the corresponding model  
#                       information in the file saved in model_setting/ temporary.
#                
#  model_class_map    : Get the model class map with given model_name from the location
#                       ../models_result_config/model_name.json

import json
class model_setting:
    def __init__(self,model_setting_f):
        self.model_setting_f = model_setting_f 
        with open(model_setting_f,"r") as f:
            tmp_model_info = json.load(f)

        self.name = tmp_model_info["name"]
        self.image_format = tmp_model_info["image_format"]
        self.image_input_height = tmp_model_info["image_input_height"]
        self.image_input_weight = tmp_model_info["image_input_weight"]
        self.result_type = tmp_model_info["result_type"]
        self.env_setting = tmp_model_info["env_setting"]
        
    def get_connect_info(self,connect_mode):
        return self.env_setting[connect_mode]

# This class defined tempory, and used for this temporary version
# The final goal is to get model information from the registory, not defined json file

class model_setting_grpc:
    def __init__(self,model_name,test_config_loc=None):
        self.model_name = model_name
        self.tmp_model_config_loc = test_config_loc or  "/model_connect_setting/{}.json".format(self.model_name)    
        with open(self.tmp_model_config_loc,"r") as f:
            tmp_model_info = json.load(f)
 
        self.grpc_env = tmp_model_info["env_setting"]["grpc"] 
        self.grpc_url = self.grpc_env["tfserving_grpc_url"]
        self.grpc_signature_name = self.grpc_env["signature_name"]
        self.grpc_model_input_name = self.grpc_env["model_input_name"]
        self.grpc_model_output_name = self.grpc_env["model_output_name"]

class model_class_map:
    def __init__(self,model_name,test_config_loc=None):
        self.model_name = model_name
        self.tmp_model_config_loc = test_config_loc or  "/models_result_config/{}.json".format(self.model_name)    
        with open(self.tmp_model_config_loc,"r") as f:
            tmp_model_info = json.load(f)
        self.model_result_type = tmp_model_info["result_type"]
    
    def get_class_mapping_dic(self):
        return self.model_result_type
  