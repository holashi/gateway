from flask import Flask,request
import sys
sys.path.extend(["./utils"])
from utils import gateway2
from utils.comp_dispatch import comp_dispatch

#import swpc specific tools
from utils import swpc

app = Flask(__name__)
comps_info_ob = comp_dispatch('/comp_dispatch/dispatch_rules.json')
# define service on http://host:port/predict_swpc
@app.route('/predict_swpc', methods=['POST','GET'])
def prediction_swpc():
    
    data_received = swpc.swpcinput_transformation(request)
   
    raw_response = gateway2.gateway("grpc",data_received,comps_info_ob)
    return_item = gateway2._grpc_result_integration(raw_response)
   
    swpc_return = swpc.swpcoutput_transformatino(request,return_item)
    return swpc_return


# curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://localhost:5000/predict
# define service on http://host:port/predict_grpc
@app.route('/predict_grpc', methods=['POST','GET'])
def prediction_grpc():
    data_received = request.json
    raw_response = gateway2.gateway("grpc",data_received,comps_info_ob)
    return_item = gateway2._grpc_result_integration(raw_response)
    return return_item

    
# define service on http://host:port/sayhello
@app.route('/sayhello')
def hello():
    return 'Hello world!'

if __name__ == "__main__":
    app.run()