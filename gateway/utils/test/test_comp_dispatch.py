# test comp_dispatch.py

import sys
sys.path.extend(["..","."])
import comp_dispatch

if __name__ =="__main__":
    comp_dispatch_f = "../../comp_dispatch/test_board.json"
    print("comp_dispatch file:",comp_dispatch_f)
    comp_dispatch_ob = comp_dispatch.comp_dispatch(comp_dispatch_f) 

    print("comp_dispatch_ob.comps:",comp_dispatch_ob.comps)
    # output : {'A': {'models_list': ['wzs_p3_m1', 'wzs_p3_m2']}, 'E': {'models_list': ['wzs_p3_m1']}}
    print("comp_dispatch_ob.get_comp_lists() :",comp_dispatch_ob.get_comp_lists())
    # output :  ['A', 'E']
    print("comp_dispatch_ob.get_comp_models(\"A\"):",comp_dispatch_ob.get_comp_models("A"))
    # output : ['wzs_p3_m1', 'wzs_p3_m2']