import uvicorn
import argparse
import os
from fastapi import FastAPI, HTTPException
import copy
from fastapi import Request
import requests
from PIL import Image
from urllib.parse import urlparse
import io
import base64

app = FastAPI()


v2_protocol = {
  "id": "string",
  "parameters": {
    "content_type": "str",
    "headers": {},
    "additionalProp1": {}
  },
  "inputs": [
    {
      "name": "string",
      "shape": [
        0
      ],
      "datatype": "string",
      "parameters": {
        "content_type": "string",
        "headers": {},
        "additionalProp1": {}
      },
      "data": "string"
    }
  ],
  "outputs": [
   
  ]
}

def convert_zero_shot_classification(input_data):
    v2_input = copy.deepcopy(v2_protocol)

    v2_input['inputs'][0]["name"]='array_inputs'
    v2_input['inputs'][0]['shape']=[-1]
    v2_input['inputs'][0]['datatype']='BYTES'
    v2_input['inputs'][0]['parameters']['content_type']='str'
    v2_input['inputs'][0]['data']=input_data['inputs']["inputs"]
    candidate_labels  ={
      "name": "candidate_labels",
      "shape": [
        -1
      ],
      "datatype": "BYTES",
      "parameters": {
        "content_type": "str",
        "headers": {},
        "additionalProp1": {}
      },
      "data": input_data['inputs']["candidate_labels"]
    }
    v2_input["inputs"].append(candidate_labels)

    # v2_input['parameters']=input_data['parameters']


    # // also for candidate labels

    return v2_input

def convert_object_detection(input_data):
    result = urlparse(input_data['inputs'])
    v2_input = copy.deepcopy(v2_protocol)
    if all([result.scheme, result.netloc]): # checking if Image url is provided then pass it as input other wise pass a PIL object as input
      inputs = input_data['inputs']
      v2_input['inputs'][0]['parameters']['content_type']='str'

    else:
      image = Image.open(r"sample.png") 
      stream = io.BytesIO()
      image.save(stream, format="PNG")
      stream.seek(0)
      inputs = base64.b64encode(stream.read()).decode('utf-8')

      v2_input['inputs'][0]['parameters']['content_type']='pillow_image'


  
    v2_input['inputs'][0]["name"]='inputs'
    v2_input['inputs'][0]['shape']=[-1]
    v2_input['inputs'][0]['datatype']='BYTES'
    v2_input['inputs'][0]['data']=inputs
    # print(v2_input)

    return v2_input

def convert_text_generation(input_data):
    v2_input = copy.deepcopy(v2_protocol)
    v2_input['inputs'][0]["name"]='array_inputs'
    v2_input['inputs'][0]['shape']=[-1]
    v2_input['inputs'][0]['datatype']='BYTES'
    v2_input['inputs'][0]['parameters']['content_type']='str'
    v2_input['inputs'][0]['data']=input_data['inputs']
    return v2_input

def convert_token_classification(input_data):
    v2_input = copy.deepcopy(v2_protocol)
    v2_input['inputs'][0]["name"]='args'
    v2_input['inputs'][0]['shape']=[-1]
    v2_input['inputs'][0]['datatype']='BYTES'
    v2_input['inputs'][0]['parameters']['content_type']='str'
    v2_input['inputs'][0]['data']=input_data['inputs']

    return v2_input

# https://text-gen-model-intern-mathew.demo1.truefoundry.com
INFERENCE_API_URL = "{model_deployed_url}/v2/models/{pipeline_name}/infer"


MODEL_CONVERSION_MAP = {
    "zero-shot-model": convert_zero_shot_classification,
    "object-detect-model": convert_object_detection,
    "text-gen-model": convert_text_generation,
    "token-class-model": convert_token_classification,
}

@app.post("/predict")
def inference(request:Request, input_data: dict = {
  "hf_pipeline": "",
  "model_deployed_url": "",
  "inputs": "",
  "parameters": ""
}):
    if input_data['hf_pipeline'] not in MODEL_CONVERSION_MAP:
        raise HTTPException(status_code=400, detail="Invalid pipeline name")

    conversion_func = MODEL_CONVERSION_MAP[input_data['hf_pipeline']]
    v2_input = conversion_func(input_data)

    # Make a request to the Seldon MLServer inference API
    url = INFERENCE_API_URL.format(model_deployed_url=input_data['model_deployed_url'], pipeline_name=input_data['hf_pipeline'])
    print(url)
    print(v2_input)
    response = requests.post(url, json=v2_input)
    print(response.text)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()



if __name__ == "__main__":


  uvicorn.run("app:app", host="0.0.0.0", port=8000)