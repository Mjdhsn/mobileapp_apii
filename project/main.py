#Twitter: Bek Brace
#Instagram: Bek Brace

import uvicorn
from fastapi import FastAPI, Body, Depends,HTTPException, Security,Form
import random
from requests.structures import CaseInsensitiveDict
from fastapi.middleware.cors import CORSMiddleware
import json, requests
from fastapi import FastAPI, Request
import uvicorn
from pydantic import BaseModel
from application.app_v1.mobile import mobile,upload_data
from mangum import Mangum

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from fastapi_jwt import (
    JwtAccessBearerCookie,
    JwtAuthorizationCredentials,
    JwtRefreshBearer,
)

app = FastAPI()


origins = ["*"]
security = HTTPBearer()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



'''....................................................Mobile app routes.................................................... '''





#  routes for mobile application
@app.post("/mobile_submit",  tags=["Mobile app routes"])
async def check_number_collate(user:dict= Body(...),userdata_collate:dict= Body(...)):
    
    """
      This route is for collation submit
    """

    print("user",user)
    print("userdata",userdata_collate)
    return mobile.submit_data(user,userdata_collate)

#  routes for mobile application
@app.post("/mobile_submit-senate",  tags=["Mobile app routes"])
async def check_number_collate(user:dict= Body(...),userdata_collate:dict= Body(...)):
    
    """
      This route is for collation submit
    """


    return mobile.submit_data_senate(user,userdata_collate)

# #  routes for mobile application
# @app.post("/mobile_submit-rep",  tags=["Mobile app routes"])
# async def check_number_collate(user:dict= Body(...),userdata_collate:dict= Body(...)):
    
#     """
#       This route is for collation submit
#     """


#     return mobile.submit_data_rep(user,userdata_collate)



@app.post("/mobile-cancel",tags=["Mobile app routes"])
async def check_number_cancel(user:dict= Body(...),userdata_collate:dict= Body(...)):
    """
      This route is for collation cancel
    """

    
    return mobile.cancel_data(user,userdata_collate)


@app.post("/mobile-cancel-senate",tags=["Mobile app routes"])
async def check_number_cancel(user:dict= Body(...),userdata_collate:dict= Body(...)):
    """
      This route is for collation cancel
    """

    
    return mobile.cancel_data_senate(user,userdata_collate)

# @app.post("/mobile-cancel-rep",tags=["Mobile app routes"])
# async def check_number_cancel(user:dict= Body(...),userdata_collate:dict= Body(...)):
#     """
#       This route is for collation cancel
# """
    
#     return mobile.cancel_data_rep(user,userdata_collate)

@app.post("/mobile-postmedia",tags=["Mobile app routes"])
async def check_number_postmedia(user:dict= Body(...),userdata_collate:dict= Body(...)):
    """
      This route is for post images or videos

        post - {

            remark : this is from additional remarks 
            file : this is file name
            type : type of the file
            lat : latitude
            long : longitude
            phone : take this value from check-number response
            email : take this value from check-number response

        }

    """
   
    return mobile.upload_data(user,userdata_collate)


@app.post("/mobile-message",tags=["Mobile app routes"])
async def check_number_message(user:dict= Body(...)):
    """
      This route is for message

      input -  user data from login repsonse

    """
    return mobile.message(user)

@app.post("/mobile-getdata",tags=["Mobile app routes"])
async def check_number_message(user:dict= Body(...)):
    """
      This route to get current data of collation form

      input -  user data from login repsonse

    """
    return mobile.get_data(user)


@app.post("/mobile-getdata-senate",tags=["Mobile app routes"])
async def check_number_message(user:dict= Body(...)):
    """
      This route to get current data of collation form

      input -  user data from login repsonse

    """
    return mobile.get_data_senate(user)

# @app.post("/mobile-getdata-rep",tags=["Mobile app routes"])
# async def check_number_message(user:dict= Body(...)):
#     """
#       This route to get current data of collation form

#       input -  user data from login repsonse

#     """
#     return mobile.get_data_rep(user)





@app.get('/mlPredict',tags=["Mobile app routes"])
def mlprediction(urlkey: str= None):
    url = "https://api.clip.jina.ai:8443/post"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] ="5410503a33dee287bf3bb7a5f6b9653c"
    data = f"""{{"data":[{{"uri": "{urlkey}",
    "matches": [{{"text": "people walking on a street"}},
            {{"text": "fight on a street"}},
            {{"text": "fire on a street"}},
            {{"text": "street violence"}},
            {{"text": "car crash"}},
            {{"text": "cars on a road"}},
            {{"text": "violence in office"}},
            {{"text": "person walking in office"}},
            {{"text": "Gun in the street"}},
            {{"text": "People fighting with Guns"}},
            {{"text": "Bandits on bike with Weapon"}},
            {{"text": "Explosive device"}},
            {{"text": "Knife in a hand"}}
            ]}}],
            "execEndpoint":"/rank"}}
    """
    resp = requests.post(url, headers=headers, data=data)
    resp = resp.json()
    v = resp['data'][0]['matches']
    outputlabel = v[0]['text']
    outputscore = v[0]['scores']['clip_score']['value']
    results = {outputlabel: outputscore}
    return results





@app.post("/mobile-start",tags=["Mobile app routes"])
async def check_number_message(user:dict= Body(...)):
    """
      This route to get current data of time

      input -  user data from login repsonse

    """
    return mobile.get_data_time(user)


@app.post("/mobile-starttime",tags=["Mobile app routes"])
async def check_number_message(user:dict= Body(...)):
    """
      This route to get current data time

      input -  user data from login repsonse

    """
    return mobile.get_data_time(user)




@app.post("/aiprediction",tags=["AI route"])
async def check_number_message(user:dict= Body(...), image:str=Body(...),types:str=None):
    
    """

      input -  user data from login repsonse
      input2 - image url

    """
    # print(user)
    # print('################')
    # print(image)
    return upload_data.ai(user,image,types)



# import boto3
# import base64
# import numpy as np
# import cv2
# try:
#     from skimage import filters
# except ImportError:
#     from skimage import filter as filters
# from parser2 import *
# from pdf2image import convert_from_path
# import urllib.request
# import shutil
# import os


# @app.post("/mobile-scanner",  tags=["Mobile app routes"])
# async def check_nr_collate(pucode:str=None,imageurl:str=None):
#     try:
#         print(pucode,imageurl)
#         textract = boto3.client("textract")
#         # encoded_img = user['image'].split(",")[1]
#         # binary = base64.b64decode(encoded_img)
#         # image = np.asarray(bytearray(binary), dtype=np.uint8)
#         # image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#         # print(img_np_arr)
#         os.system('wget {} -O {}'.format(imageurl,"filename.pdf"))
#         pil_image_lst = convert_from_path('filename.pdf')
#         print(pil_image)
#         pil_image = pil_image_lst[0]
#         image = np.array(pil_image) 
#         # img_object = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
#         print(image)
#         gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#         # blur
#         smooth = cv2.GaussianBlur(gray, (33,33), 0)

#         division = cv2.divide(gray, smooth, scale=255)

# # sharpen using unsharp masking
#         sharp = filters.unsharp_mask(division, radius=1.5, amount=2.5, multichannel=False, preserve_range=False)
#         sharp = (255*sharp).clip(0,255).astype(np.uint8)
#         print(sharp)
#         is_success, im_buf_arr = cv2.imencode(".jpg", sharp)
#         byte_im = im_buf_arr.tobytes()
#         print('ok')

#         response = textract.analyze_document(Document={'Bytes': byte_im}, FeatureTypes=["FORMS", "TABLES"])
#         print(response)
#         raw_text = extract_text(response, extract_by="LINE")
#         word_map = map_word_id(response)
#         table = extract_table_info(response, word_map)
#         key_map = get_key_map(response, word_map)
#         value_map = get_value_map(response, word_map)
#         final_map = get_kv_map(key_map, value_map)
#         for key,value in table.items():
#             table = value
#     except Exception:
#         return {"message": "There was an error uploading the file"}
 
        
#     return mobile.scanner(pucode,raw_text,table,final_map,sharp)












handler = Mangum(app=app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",  reload=True, access_log=False,port=8000)
