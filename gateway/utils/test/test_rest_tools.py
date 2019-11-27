# reference https://github.com/tensorflow/serving/blob/master/tensorflow_serving/example/resnet_client.py
# This file try to sent images directly to tensorflow server and got response
# payload to tensorfload serving should be with the format 
# {
#   "signature_name":"signature_name",
#   "comps":["Comp1","comp2"...],
#   "instance":[
#                {
#                 // Example 1
#                   "<feature_name1>": <value>|<list>,
#                   "<feature_name2>": <value>|<list>,
#                   ...
#                },{
#                 // Example 2
#                   "<feature_name1>": <value>|<list>,
#                   "<feature_name2>": <value>|<list>,
#                   ...
#                }
#               ]
# }
import io
import base64
import json
import requests

def open_and_serialize_image(filename):
    with open(filename, "rb") as f:
        image = f.read()
    return base64.urlsafe_b64encode(image).decode()

# use base64_urlsafe_b64encode to encode image
img_path = "/Users/harveyshi/wistron/github/aoi_gateway/images/png/CN01W26NWS200993001JA00_PT4504_0_NA_NA.png"
img_0 = open_and_serialize_image(img_path)
# create data based on required format.

data = json.dumps({"signature_name": "classification", 
                    "comps":["R","C"],
                    "instances":[
                        {  
                            "string_array":img_0,
                        },
                        {
                            "string_array":img_0,
                        }
                        ]
                    })
# 
# data = json.dumps({"signature_name": "classification", 
#                     "instances":[
#                         {
#                             "string_array":{"b64":img_0}
#                         }
#                         ]
#                     })

headers = {"content-type": "application/json"}
json_response = requests.post('http://10.34.127.5:48501/v1/models/wzs_p3_m2/versions/1:predict', data=data, headers=headers)
predictions = json.loads(json_response.text)
print(predictions)