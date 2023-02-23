
from application.app_v1.database import get_db,get_db2
import json
import os
from textractor import Textractor
from textractor.data.constants import TextractFeatures
from textractor.visualizers.entitylist import EntityList
from textractor.data.constants import TextractFeatures, Direction, DirectionalFinderType
from fastapi import FastAPI, status

from fastapi import FastAPI, Body, Depends,HTTPException, Security,Form

import re
import datetime
from PIL import Image
# def addData_all(role,country,state, lga, ward, pu, file, remark, type, lat, long, phone, email):
import urllib.request
import difflib
def ai(user,image,types):
    user_data =user
    
    queries = [

    "How many number of voters on register?" ,
    "How many number of Acrredited voters ?" ,
    "How many number of ballot papers issued to the polling unit?" ,
    "How many number of unused ballot papers ?" ,
    "How many number of spoiled ballot papers?" ,
    "How many number of used ballot papers ?"  ,
    "How many number of Rejected ballot?"  ,
  


    
]
  
    urllib.request.urlretrieve(
                image,
                "image.png")
            
    source=Image.open("image.png")
    extractor = Textractor(profile_name="default")
    document = extractor.analyze_document(
    file_source=Image.open("image.png"),
    features=[TextractFeatures.QUERIES,TextractFeatures.TABLES],
    queries=queries
)


    table = EntityList(document.tables[1])

    df = table[0].to_pandas()
    party_val = df.iloc[1:][1]
    party_matching = []
    party_real_values = ['A', 'AA', 'AAC', 'ADC', 'ADP', 'APC', 'APGA', 'APM', 'APP', 'BP', 'LP', 'NNPP', 'NRM', 'PDP', 'PRP', 'SDP','YPP', 'ZLP']
    for p in party_val:

        v = difflib.get_close_matches(p, party_real_values)
        
        if len(v) > 0:
            if p =="POP":
                v[0] = "PDP"
            elif p =="AOP":
                v[0] = "ADP"
            elif p =="SOP":
                v[0] ="SDP"
            elif p =="AOC":
                v[0] ="ADC"
            party_matching.append(v[0])

        else:
            pass
    
    number = {}
    total_register = ""
    total_acrredited =""
    total_rejected = ""
    spoilled =""
    valid_votes =""
    used_ballot =""
    ballot_issued = ""
    unused_ballot = ""
    for query in document.queries:
        if query.result:
            if query.query == 'How many number of voters on register?':
                value= re.sub("\D","",query.result.answer)
                if value =="":
                        value = 0
                value = int(value)

                total_register += f"TOTAL_REGISTERED_VOTERS = {value}"
            elif query.query == 'How many number of Acrredited voters ?':
                value= re.sub("\D","",query.result.answer)
                if value =="":
                        value = 0
                value = int(value)

                total_acrredited += f"TOTAL_ACCREDITED_VOTERS = {value}"
            
            elif query.query == 'How many number of ballot papers issued to the polling unit?':
                value= re.sub("\D","",query.result.answer)
                if value =="":
                        value = 0
                value = int(value)

                ballot_issued += f"BALLOT_ISSUED = {value}"
            
            elif query.query == 'How many number of unused ballot papers ?':
                value= re.sub("\D","",query.result.answer)
                if value =="":
                        value = 0
                value = int(value)

                unused_ballot += f"UNUSED_BALLOT = {value}"
                
            elif query.query == 'How many number of used ballot papers ?':
                value= re.sub("\D","",query.result.answer)
                if value =="":
                        value = 0
                value = int(value)

                used_ballot += f"USED_BALLOT = {value}"
            
            elif query.query == '':
                value= re.sub("\D","",query.result.answer)
                if value =="":
                        value = 0
                value = int(value)

                valid_votes += f"VALID_VOTES_C = {value}"
                
            elif query.query == 'How many number of spoiled ballot papers?':
                value= re.sub("\D","",query.result.answer)
                if value =="":
                        value = 0
                value = int(value)

                spoilled += f"SPOILED_BALLOT = {value}"
            
            elif query.query == '"How many number of Rejected ballot?"':
                value= re.sub("\D","",query.result.answer)
                if value =="":
                        value = 0
                value = int(value)

                total_rejected += f"TOTAL_REJECTED_VOTES = {value}"
            else:
                pass

    numberlist= [total_register,total_acrredited,total_rejected,spoilled,valid_votes,used_ballot,ballot_issued,unused_ballot]    
    numberlist = [x for x in numberlist if x != ""]
    numberquery = ", ".join(numberlist)


    values_matching = []
    party_values = df.iloc[1:][3]
    for v in party_values:
        n= re.sub("\D","",v)
        if n =="":
            n = 0
        n = int(n)
        values_matching.append(n)

    party_dictionary =  dict(zip(party_matching,values_matching))
    part = ""
    for key, value in party_dictionary.items():
        part += f"{key} ={value},"
    part = part[:-1]
    level_input = user_data['level_childs']
    country_name = level_input['country']
    state_name = level_input['state']
    district_name = level_input['district']
    constituency_name = level_input['constituency']
    lga_name = level_input['lga']
    ward_name = level_input['ward']
    pu_name = level_input['pollingUnit']
    with get_db2() as conn:
        cur = conn.cursor()

        try:
            if types == "presidential":
                sql = f"Update pu_result_table SET {part},{numberquery},status='collated' where country_id ={country_name} and state_id = {state_name} and lga_id={lga_name} and ward_id={ward_name} and pu_id = {pu_name}"
                cur.execute(sql)
                sql1 = f"""SELECT * FROM pu_result_table where country_id= {country_name} AND state_id = {state_name} and lga_id = {lga_name} and ward_id = {ward_name} and pu_id= {pu_name}"""

                final ={}
                try:
                    cur.execute(sql1)

                    results = cur.fetch_pandas_all()
                    results = results.to_json(orient="records")
                    results = json.loads(results)
                    parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                    total =["TOTAL_ACCREDITED_VOTERS","TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","BALLOT_ISSUED","UNUSED_BALLOT","SPOILED_BALLOT","VALID_VOTES_C","USED_BALLOT"]
            
                    data = ['DATE_TIME', 'PERSON_COLLATED','FILE']
                    parties_results = {}
                    total_results={}
                    other_data_results={}
                    for key in parties:
                        parties_results.update( {key:results[0][key]})
                    
                    for key in total:
                        total_results.update( {key:results[0][key]})

                    for key in data:
                        other_data_results.update( {key:results[0][key]})

                    final['results'] = parties_results
                    final['total'] = total_results
                    final['other_data'] = other_data_results

                    return final
                except Exception as e:
                    print(e)
                    return str(e)
                
                # return  {"message": f"Presidential Polling unit AI Submitted Successfully by {user_data['name']}"}
            elif types == "senate":
                sql = f"Update sen_pu_table SET {part},{numberquery},status='collated' where country_id ={country_name} and state_id = {state_name} AND DISTRICT_ID = {district_name} and lga_id={lga_name} and ward_id={ward_name} and pu_id = {pu_name}"
                cur.execute(sql)
                sql1 = f"""SELECT * FROM sen_pu_table where country_id= {country_name} AND state_id = {state_name} and lga_id = {lga_name} and ward_id = {ward_name} and pu_id= {pu_name}"""

                final ={}
                try:
                    cur.execute(sql1)

                    results = cur.fetch_pandas_all()
                    results = results.to_json(orient="records")
                    results = json.loads(results)
                    parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                    total =["TOTAL_ACCREDITED_VOTERS","TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","BALLOT_ISSUED","UNUSED_BALLOT","SPOILED_BALLOT","VALID_VOTES_C","USED_BALLOT"]
            
                    data = ['DATE_TIME', 'PERSON_COLLATED','FILE']
                    parties_results = {}
                    total_results={}
                    other_data_results={}
                    for key in parties:
                        parties_results.update( {key:results[0][key]})
                    
                    for key in total:
                        total_results.update( {key:results[0][key]})

                    for key in data:
                        other_data_results.update( {key:results[0][key]})

                    final['results'] = parties_results
                    final['total'] = total_results
                    final['other_data'] = other_data_results

                    return final
                except Exception as e:
                    print(e)
                    return str(e)
                # cur.execute(sql)
                # return  {"message": f"Senate Polling unit AI Submitted Successfully by {user_data['name']}"}

            elif types == "rep":
                sql = f"Update rep_pu_table SET {part},{numberquery},status='collated' where country_id ={country_name} and state_id = {state_name} AND CONST_ID = {constituency_name} and lga_id={lga_name} and ward_id={ward_name} and pu_id = {pu_name}"
                cur.execute(sql)
                sql1 = f"""SELECT * FROM rep_pu_table where country_id= {country_name} AND state_id = {state_name} and lga_id = {lga_name} and ward_id = {ward_name} and pu_id= {pu_name}"""

                final ={}
                try:
                    cur.execute(sql1)

                    results = cur.fetch_pandas_all()
                    results = results.to_json(orient="records")
                    results = json.loads(results)
                    parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                    total =["TOTAL_ACCREDITED_VOTERS","TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","BALLOT_ISSUED","UNUSED_BALLOT","SPOILED_BALLOT","VALID_VOTES_C","USED_BALLOT"]
            
                    data = ['DATE_TIME', 'PERSON_COLLATED','FILE']
                    parties_results = {}
                    total_results={}
                    other_data_results={}
                    for key in parties:
                        parties_results.update( {key:results[0][key]})
                    
                    for key in total:
                        total_results.update( {key:results[0][key]})

                    for key in data:
                        other_data_results.update( {key:results[0][key]})

                    final['results'] = parties_results
                    final['total'] = total_results
                    final['other_data'] = other_data_results

                    return final
                except Exception as e:
                    print(e)
                    return str(e)
                
                # return  {"message": f"Rep AI Submitted Successfully by {user_data['name']}"}
        except:
              raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Uploaded Image is not clear please upload high quality image"
        )
            
#             return {"message": "Uploaded Image is not clear please upload high quality image"}
       
        
        

    

def addData_pu(state, lga, ward, pu, file, remark, type, lat, long, phone, email ):
    with get_db2() as conn:
        cur = conn.cursor()
        try:
            sql = '''INSERT INTO userdata_pu
                    (
                    state_name,
                    lga_name,
                   ward_name,
                   pu_name,
                   remark,
                   
                   file,
                    file_type,
                    lat,
                    long,
                    phone,
                     email

                    )
                    VALUES(% s, % s, % s, % s, % s, % s, % s, % s, %s,%s, %s)'''
                    
            cur.execute(
                sql, (state, lga, ward, pu,  remark, file, type, lat, long, phone, email))
            conn.commit()
        # app.conn.close()
            return '1'
        except:
            return '0'

def getData_pu(country,state, lga, ward, pu):

    with get_db2() as conn:
        cur = conn.cursor()

        sql = f"SELECT * FROM userdata_pu WHERE country_id= {country} AND state_id = {state} AND lga_id= {lga} AND ward_id = {ward} AND pu_id = {pu}"
        try:
            cur.execute(sql)
            row_headers = [x[0] for x in cur.description]
            results = cur.fetch_pandas_all()
            res = results.to_json(orient="records")
            parsed = json.loads(res)
            # cur.close()
            json_data = parsed
            return json_data
        except Exception as e:
            print(e)
            return str(e)



def addData_ward(state, lga, ward,file, remark, type, lat, long, phone, email ):
    with get_db2() as conn:
        cur = conn.cursor()
        try:
            sql = '''INSERT INTO userdata_ward
                    (
                    state_name,
                    lga_name,
                   ward_name,
                   remark,               
                   file,
                    file_type,
                    lat,
                    long,
                    phone,
                     email

                    )
                    VALUES(% s, % s, % s, % s, % s, % s, % s, %s,%s,%s)'''
                    
            cur.execute(
                sql, (state, lga, ward,  remark, file, type, lat, long, phone, email))
            conn.commit()
        # app.conn.close()
            return '1'
        except:
            return '0'


def getData_ward(country,state, lga, ward):

    with get_db2() as conn:
        cur = conn.cursor()

        sql = f"SELECT * FROM userdata_ward WHERE country_id= {country} AND state_id = {state} AND lga_id= {lga} AND ward_id = {ward}"
        try:
            cur.execute(sql)
            row_headers = [x[0] for x in cur.description]
            results = cur.fetch_pandas_all()
            res = results.to_json(orient="records")
            parsed = json.loads(res)
            # cur.close()
            json_data = parsed
            return json_data
        except Exception as e:
            print(e)
            return str(e)


def addData_lga(state, lga,file, remark, type, lat, long, phone, email ):
    with get_db2() as conn:
        cur = conn.cursor()
        try:
            sql = '''INSERT INTO userdata_lga
                    (
                    state_name,
                    lga_name,
                   remark,
                   
                   file,
                    file_type,
                    lat,
                    long,
                    phone,
                     email

                    )
                    VALUES(% s, % s, % s, % s, % s, %s,%s, %s, %s)'''
                    
            cur.execute(
                sql, (state, lga, remark, file, type, lat, long, phone, email))
            conn.commit()
        # app.conn.close()
            return '1'
        except:
            return '0'


def getData_lga(country,state, lga):

    with get_db2() as conn:
        cur = conn.cursor()

        sql = f"SELECT * FROM userdata_lga WHERE country_id = {country} AND state_id = {state} AND lga_id= {lga}"
        try:
            cur.execute(sql)
            row_headers = [x[0] for x in cur.description]
            results = cur.fetch_pandas_all()
            res = results.to_json(orient="records")
            parsed = json.loads(res)
            # cur.close()
            json_data = parsed
            return json_data
        except Exception as e:
            print(e)
            return str(e)

def addData_district(state, district, file, remark, type, lat, long, phone, email ):
    with get_db2() as conn:
        cur = conn.cursor()
        try:
            sql = '''INSERT INTO userdata_district
                    (
                    state_name,
                    district_name,
                   remark,
                   
                   file,
                    file_type,
                    lat,
                    long,
                    phone,
                     email

                    )
                    VALUES(% s, % s, % s, % s, % s, % s, %s,%s, %s)'''
                    
            cur.execute(
                sql, (state, district, remark, file, type, lat, long, phone, email))
            conn.commit()
        # app.conn.close()
            return '1'
        except:
            return '0'


def getData_district(country,state, constituency):

    with get_db2() as conn:
        cur = conn.cursor()

        sql = f"SELECT * FROM userdata_district WHERE country_id= {country} AND state_id = {state} AND district_id= {constituency}"
        try:
            cur.execute(sql)
            row_headers = [x[0] for x in cur.description]
            results = cur.fetch_pandas_all()
            res = results.to_json(orient="records")
            parsed = json.loads(res)
            # cur.close()
            json_data = parsed
            return json_data
        except Exception as e:
            print(e)
            return str(e)

def addData_constituency(state, constituency, file, remark, type, lat, long, phone, email ):
    with get_db2() as conn:
        cur = conn.cursor()
        try:
            sql = '''INSERT INTO userdata_constituency
                    (
                    state_name,
                    constituency_name,
                   remark,
                   file,
                    file_type,
                    lat,
                    long,
                    phone,
                     email

                    )
                    VALUES(% s, % s, % s, % s, % s, % s, %s,%s, %s)'''
                    
            cur.execute(
                sql, (state, constituency, remark, file, type, lat, long, phone, email))
            conn.commit()
        # app.conn.close()
            return '1'
        except:
            return '0'


def getData_constituency(country,state, constituency):

    with get_db2() as conn:
        cur = conn.cursor()

        sql = f"SELECT * FROM userdata_constituency WHERE country_id= {country} AND state_id = {state} AND const_id = {constituency}"
        try:
            cur.execute(sql)
            row_headers = [x[0] for x in cur.description]
            results = cur.fetch_pandas_all()
            res = results.to_json(orient="records")
            parsed = json.loads(res)
            # cur.close()
            json_data = parsed
            return json_data
        except Exception as e:
            print(e)
            return str(e)


def addData_state(state,file, remark, type, lat, long, phone, email ):
    with get_db2() as conn:
        cur = conn.cursor()
        try:
            sql = '''INSERT INTO userdata_state
                    (
                    state_name,
                   remark,
                   
                   file,
                    file_type,
                    lat,
                    long,
                    phone,
                     email

                    )
                    VALUES(% s, % s, % s, % s, % s, %s,%s, %s)'''
                    
            cur.execute(
                sql, (state, remark,file, type, lat, long, phone, email))
            conn.commit()
        # app.conn.close()
            return '1'
        except:
            return '0'


def getData_state(country,state):

    with get_db2() as conn:
        cur = conn.cursor()

        sql = f"SELECT * FROM userdata_state WHERE country_id = {country} AND state_id ={state}"
        try:
            cur.execute(sql)
            row_headers = [x[0] for x in cur.description]
            results = cur.fetch_pandas_all()
            res = results.to_json(orient="records")
            parsed = json.loads(res)
            # cur.close()
            json_data = parsed
            return json_data
        except Exception as e:
            print(e)
            return str(e)


def addData_country(country,file, remark,type, lat, long, phone, email ):
    with get_db2() as conn:
        cur = conn.cursor()
        try:
            sql = '''INSERT INTO userdata_country
                    (country,
                   remark,
                   
                   file,
                    file_type,
                    lat,
                    long,
                    phone,
                     email

                    )
                    VALUES(% s, % s, % s, % s, % s, %s,%s, %s)'''
                    
            cur.execute(
                sql, (country,remark, file, type, lat, long, phone, email))
            conn.commit()
        # app.conn.close()
            return '1'
        except:
            return '0'


#needs to be updated

def getData_country(country):

    with get_db2() as conn:
        cur = conn.cursor()

        sql = f"SELECT * FROM userdata_country"
        try:
            cur.execute(sql)
            row_headers = [x[0] for x in cur.description]
            results = cur.fetch_pandas_all()
            res = results.to_json(orient="records")
            parsed = json.loads(res)
            # cur.close()
            json_data = parsed
            return json_data
        except Exception as e:
            print(e)
            return str(e)
