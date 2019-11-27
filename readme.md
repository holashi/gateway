## __model gateway prototype__  
    This prototype is used to dispatch models based on the request.
    The key that the prototype reference to is "Comp". And the service is created based on flask. 

### __Start the Services__  
1. According to the templete in ```./comp_dispatch/dispatch_rules.json```, modify the file to determine the relationships between components and corresponding models.  
2. Files in ```/model_connect_setting``` describe the model serving(connection) informatin, and the model is served with the tensorflow serving.  
3. Files in ```/model_result_config``` describe the relationship between  tensorflow model result and the corresponding meaning.  
4. After prepare the files above, run ```sh build_img.sh``` to build the docker images which used for the gateway service.
5. With the docker image, run or refer to ```run_img.sh``` to start your serving.
6. The serving url will be ```http://host:port/predict_grpc```, more service url can be found in the notation in the file ```/gateway/main.py```.

###  __Request Format__
    The request with the format
    {
       "instance":[
           // image 1
               {
                   "image":{"b64":....},
                   "comp":"A001",
                   "SN":0001
                },
           // image 2 
               {
                   "image":{"b64":....}",
                   "comp":"B002",
                   "SN":0002
                }
           ]
      }
