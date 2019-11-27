import requests
def restful_request_server(
    only_one_flag,
    images, 
    model_url, 
    model_name
):
    time_out = 0.05 * len(images)
    if only_one_flag is True:
        if image_format == 'b64':
            imaegs = imaegs.decode()
        instances = [{model_input_name: imaegs}]
    else:
        if image_format == 'b64':
            instances = [{model_input_name: ir.decode()} for ir in imaegs] 
        else:
            instances = [{model_input_name: ir} for ir in imaegs] 
    payload = {"signature_name":model_signature_name,"instances": instances}
    data = json.dumps(payload)

    softmax_ary = []
    predict_api = "http://{model_url}/v1/models/{model_name}:predict".format(model_url=model_url,model_name=model_name)
    try:
        response = requests.post(predict_api, data=data, timeout=time_out)
        if response.status_code == 200:
            softmax_ary.append(response.json()['predictions'])
        else:
            raise Exception('Error code: {error_code}, Content: {content}'.format(
                error_code=response.status_code, content=response.content))
    except Exception as e: 
        print('Request tensorflow RESTful server error, message: {e}'.format(e=e))
    return softmax_ary