# Use component dispatch file path as element to create comp_dispatch object.
# 
# Comp_dispatch object :
# 
#   attributes:
# 
#       comps: contents in the component dispatch file with key "Comps",and record the components with corresponding models
#           ex: {
#                 'A': {'models_list': ['model_1', 'model_21']}, 
#                 'B': {'models_list': ['model_1']}
#               }
# 
#       SN: contents in the component dispatch file with key "SN", this is the s/n number of production
# 
#   methods: 
# 
#       get_comp_lists(): get component code list record in the component dispatch file. Return python list ex: ['model_1', 'model_21']
#
#       get_comp_models(comp): get model name list with given component code. Return python list ex: ['A','B']

import json
class comp_dispatch:
    def __init__(self,comp_dispatch_f):
        self.comp_dispatch_f = comp_dispatch_f 
        with open(comp_dispatch_f,"r") as f:
            tmp_comp_dispatch_cont = json.load(f)

        self.comps =  tmp_comp_dispatch_cont["Comps"]
        self.SN = tmp_comp_dispatch_cont["MB_SN"]

    def get_comp_lists(self):
        return list(self.comps.keys())
    
    def get_comp_models(self,comp):
        return self.comps[comp]["models_list"]
    
    

# if __name__ =="__main__":
#     comp_dispatch_f = "../comp_dispatch/test_board.json"
#     print(comp_dispatch_f)
#     test_ob = comp_dispatch(comp_dispatch_f) 
#     print(test_ob.get_comp_models("A"))