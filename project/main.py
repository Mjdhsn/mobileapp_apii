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


    return mobile.submit_data(user,userdata_collate)

#  routes for mobile application
@app.post("/mobile_submit-senate",  tags=["Mobile app routes"])
async def check_number_collate(user:dict= Body(...),userdata_collate:dict= Body(...)):
    
    """
      This route is for collation submit
    """


    return mobile.submit_data_senate(user,userdata_collate)

#  routes for mobile application
@app.post("/mobile_submit-rep",  tags=["Mobile app routes"])
async def check_number_collate(user:dict= Body(...),userdata_collate:dict= Body(...)):
    
    """
      This route is for collation submit
    """


    return mobile.submit_data_rep(user,userdata_collate)



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

@app.post("/mobile-cancel-rep",tags=["Mobile app routes"])
async def check_number_cancel(user:dict= Body(...),userdata_collate:dict= Body(...)):
    """
      This route is for collation cancel
"""
    
    return mobile.cancel_data_rep(user,userdata_collate)

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

@app.post("/mobile-getdata-rep",tags=["Mobile app routes"])
async def check_number_message(user:dict= Body(...)):
    """
      This route to get current data of collation form

      input -  user data from login repsonse

    """
    return mobile.get_data_rep(user)





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


handler = Mangum(app=app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",  reload=True, access_log=False,port=8000)
