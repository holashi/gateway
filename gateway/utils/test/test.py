import json

f = "./test.json"

# class tmp_data_ob:
#     def __init__(self,one_sample_in_json_received):
#         self.

def _json_receiveor_parser_grpc(payload_json_instance):
    grpc_data_dic= {}
    for ins in payload_json_instance:
        if ins['comp'][0] not in grpc_data_dic.keys():
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

with open(f,"r") as f:
    data = json.load(f)
    instances = data['instances']
comp_d = {}
#print(instances)

# for ins in instances:
#     if ins['comp'] not in comp_d.keys():
#         comp_d[ins['comp']]={}
#         for k in ins.keys():
#             if k =="image":
#                 comp_d[ins['comp']][k]=[ins[k]["b64"]]
#             else:
#                 comp_d[ins['comp']][k]=[ins[k]]
#     else:
#       for k in ins.keys():
#             if k =="image":
#                     comp_d[ins['comp']][k].append(ins[k]["b64"])
#             else:
#                 comp_d[ins['comp']][k].append(ins[k])



a = _json_receiveor_parser_grpc(data['instances'])
print(a)

