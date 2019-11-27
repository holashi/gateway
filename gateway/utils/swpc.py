from PIL import Image
import io
import base64
import json

def swpcinput_transformation(request):

    comp = request.form['img_name'].split('_')[2][1]# 第三段第二個位置
    sn = request.form['img_name']
    # get image string
    PIL_img=Image.open(request.files["img_file"])
    output_buffer = io.BytesIO()
    PIL_img.save(output_buffer, format='PNG')
    base64_str = base64.urlsafe_b64encode(output_buffer.getvalue()).decode('utf-8')

    instance = {"image":{"b64":base64_str},"comp":comp,"SN":sn}
    data_received = {
    "instance":[instance]
    }
    return data_received

def swpcoutput_transformatino(request,response):
    response_buf = {}
    response_buf["org_name"]=request.form["img_name"]
    response_buf["kb_id"]=request.form["img_sn"]
    onesample=response[list(response.keys())[0]][0]
    # example :onesample={'OK': 0.9829896092414856}
    print(onesample)
    response_buf["ai_result"]=list(onesample.keys())[0]
    response_buf["ai_score"]=onesample[response_buf["ai_result"]]
    return json.dumps(response_buf)