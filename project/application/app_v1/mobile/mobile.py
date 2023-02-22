from application.app_v1.database import get_db,get_db2
from datetime import datetime
from datetime import datetime
import json
#import cv2
import boto3
import pytz

nigeria = pytz.timezone("Africa/Lagos") 
now = datetime.now(nigeria)


def submit_data(user,userdata_collate):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    now = datetime.now(nigeria)
    with get_db2() as conn:
        cur = conn.cursor()

        if role_input == "pns":
            country_name = level_input['country']
            timer = now.strftime("%m/%d/%Y %H:%M")
            del userdata_collate['UNUSED_BALLOT']
            del userdata_collate['SPOILED_BALLOT']
            del userdata_collate['USED_BALLOT']
            del userdata_collate['BALLOT_ISSUED']
            del userdata_collate['Total_Accredited_voters']
            userdata_collate['TOTAL_VALID_VOTES_C'] = userdata_collate['VALID_VOTES_C']
            del userdata_collate['VALID_VOTES_C']
            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            query = ", ".join(query)
            sql = f"""Update country_result_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name} """
            
            try:
                cur.execute(sql)
                # results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
        
        elif role_input == "pss":
            country_name = level_input['country']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            del userdata_collate['UNUSED_BALLOT']
            del userdata_collate['SPOILED_BALLOT']
            del userdata_collate['USED_BALLOT']
            del userdata_collate['BALLOT_ISSUED']
            del userdata_collate['Total_Accredited_voters']
            userdata_collate['TOTAL_VALID_VOTES_C'] = userdata_collate['VALID_VOTES_C']
            del userdata_collate['VALID_VOTES_C']
            query = [
            f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]

            query = ", ".join(query)
            sql = f"""Update state_result_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name} and state_id= {state_name} """
            print(sql)
            try:
                cur.execute(sql)
                # results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
        
                
        elif role_input == "pls":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")
            del userdata_collate['UNUSED_BALLOT']
            del userdata_collate['SPOILED_BALLOT']
            del userdata_collate['USED_BALLOT']
            del userdata_collate['BALLOT_ISSUED']
            del userdata_collate['Total_Accredited_voters']
            userdata_collate['TOTAL_VALID_VOTES_C'] = userdata_collate['VALID_VOTES_C']
            del userdata_collate['VALID_VOTES_C']
            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            
            query = ", ".join(query)
            sql = f"""Update lga_result_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name}"""
            try:
                cur.execute(sql)
                # results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)

        elif role_input == "pws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")
            del userdata_collate['UNUSED_BALLOT']
            del userdata_collate['SPOILED_BALLOT']
            del userdata_collate['USED_BALLOT']
            del userdata_collate['BALLOT_ISSUED']
            del userdata_collate['Total_Accredited_voters']
            userdata_collate['TOTAL_VALID_VOTES_C'] = userdata_collate['VALID_VOTES_C']
            del userdata_collate['VALID_VOTES_C']
            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            query = ", ".join(query)
            sql = f"""Update ward_result_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name} and ward_id= {ward_name}"""
            
            try:
                cur.execute(sql)
                # results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)

        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")
           
            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            
            query = ", ".join(query)
            sql = f"""Update pu_result_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""
            
            try:
                cur.execute(sql)
                # results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
        
        elif role_input == "sds":
                 raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to cancel Presidential Elections"
        )        



        elif role_input == "rcs":
             raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to cencel Presidential Elections"
        )        

        

def cancel_data(user,userdata_collate):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    now = datetime.now(nigeria)
    with get_db2() as conn:
        cur = conn.cursor()
        if role_input == "pns":
            country_name = level_input['country']
            timer = now.strftime("%m/%d/%Y %H:%M")
  
            sql = f"""Update country_result_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0, TOTAL_VALID_VOTES_C=0, Total_Rejected_votes=0,TOTAL_VOTES_CAST_C=0, YPP=0, ZLP=0 , date_time ='{timer}'
  Where country_id = {country_name} """
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
        
        elif role_input == "pss":
            country_name = level_input['country']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
       
            sql = f"""Update state_result_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0,TOTAL_VALID_VOTES_C=0, Total_Rejected_votes=0,TOTAL_VOTES_CAST_C=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} """
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
        
                
        elif role_input == "pls":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")

            sql = f"""Update lga_result_table SET  status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0,TOTAL_VALID_VOTES_C=0, Total_Rejected_votes=0,TOTAL_VOTES_CAST_C=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)

        elif role_input == "pws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")

            sql = f"""Update ward_result_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0, TOTAL_VALID_VOTES_C=0, Total_Rejected_votes=0,TOTAL_VOTES_CAST_C=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name} and ward_id= {ward_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)

        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")
  
            sql = f"""Update pu_result_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0, BALLOT_ISSUED=0,UNUSED_BALLOT=0,SPOILED_BALLOT=0,VALID_VOTES_C=0,USED_BALLOT=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
        
               
        elif role_input == "sds":
                 raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to cancel Presidential Elections"
        )        



        elif role_input == "rcs":
             raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to cencel Presidential Elections"
        )        
           



    
        
def upload_data(user,userdata_postmedia):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    phone = user_data['phone']
    # email = user_data['email']

    now = datetime.now(nigeria)
    remark = userdata_postmedia['remark']
        #ml = userdata_postmedia['ml']

    file = userdata_postmedia['file']
    type = userdata_postmedia['type']
    lat = userdata_postmedia['lat']
    long = userdata_postmedia['long']
    
    with get_db2() as conn:
        cur = conn.cursor()
        if role_input == "pns":
            country_name = level_input['country']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = '''INSERT INTO userdata_country
                            (country_id,
                            remark,
                        
                            file,
                            file_type,
                            lat,
                            long,
                            phone,
                            date

                            )
                            VALUES(% s, % s, % s, % s, %s,%s, %s,%s)'''
                            
                cur.execute(
                        sql, (country_name,remark, file, type, lat, long, phone,timer))
                conn.commit()
                return '1'
            except:
                return '0'
        
        elif role_input == "pss":
            country_name = level_input['country']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")

       
            try:
                sql = '''INSERT INTO userdata_state
                        (
                        country_id,
                        state_id,
                        remark,
                    
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s,% s, % s, % s, % s, % s, %s, %s,%s)'''
                        
                cur.execute(
                    sql, (country_name,state_name, remark,file, type, lat, long, phone,timer))
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'
        
                
        elif role_input == "pls":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = '''INSERT INTO userdata_lga
                        (
                        country_id,
                        state_id,
                        lga_id,
                        remark,                    
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s,% s,% s, % s, % s, % s, %s,%s,%s,%s)'''
                cur.execute(
                    sql, (country_name,state_name, lga_name, remark, file, type, lat, long, phone,timer))
                
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'

        elif role_input == "pws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")


            try:
                sql = '''INSERT INTO userdata_ward
                        (
                        country_id,
                        state_id,
                        lga_id,
                        ward_id,
                        remark,               
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s,% s, % s, % s, % s, % s, % s, %s,%s,%s,%s)'''
                        
                cur.execute(
                    sql, (country_name,state_name, lga_name, ward_name,  remark, file, type, lat, long, phone,timer))
                
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'

        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = '''INSERT INTO userdata_pu
                        (
                        country_id,
                        state_id,
                        lga_id,
                        ward_id,
                        pu_id,
                        remark,
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s, % s,% s, % s, % s, % s, % s, % s, %s,%s, %s,%s)'''
                        
                cur.execute(
                    sql, (country_name,state_name, lga_name, ward_name, pu_name,  remark, file, type, lat, long, phone,timer))
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'

           
        
        elif role_input == "sds":
            country_name = level_input['country']
            district_name = level_input['district']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            try:
                sql = '''INSERT INTO userdata_district
                        (
                        country_id,
                        state_id,
                        district_id,
                        remark,
                    
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s,% s, % s, % s, % s, % s, %s, %s, %s,%s)'''
                        
                cur.execute(
                    sql, (country_name,state_name, district_name, remark, file, type, lat, long, phone,timer))
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'
            


        elif role_input == "sls":
            country_name = level_input['country']
            district_name = level_input['district']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")
            try:
                sql = '''INSERT INTO userdata_lga
                        (
                        country_id,
                        state_id,
                        lga_id,
                        remark,
                    
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s,% s, % s, % s, % s, % s, %s,%s, %s,%s)'''
                        
                cur.execute(
                    sql, (country_name,state_name, lga_name, remark, file, type, lat, long, phone,timer))
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'

        elif role_input == "sws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = '''INSERT INTO userdata_ward
                        (
                        country_id,
                        state_id,
                        lga_id,
                        ward_id,
                        remark,               
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s,% s, % s, % s, % s, % s, % s, %s,%s,%s,%s)'''
                        
                cur.execute(
                    sql, (country_name,state_name, lga_name, ward_name,  remark, file, type, lat, long, phone,timer))
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'


        elif role_input == "spa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = '''INSERT INTO userdata_pu
                        (
                        country_id,
                        state_id,
                        lga_id,
                        ward_id,
                        pu_id,
                        remark,
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s, % s,% s, % s, % s, % s, % s, % s, %s,%s, %s,%s)'''
                        
                cur.execute(
                    sql, (country_name,state_name, lga_name, ward_name, pu_name,  remark, file, type, lat, long, phone,timer))
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'

        elif role_input == "rcs":
            country_name = level_input['country']
            constituency_name = level_input['constituency_name']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = '''INSERT INTO userdata_constituency
                        (
                        country_id,
                        state_id,
                        const_id,
                        remark,
                    
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s,% s, % s, % s, % s, % s, %s, %s, %s,%s)'''
                        
                cur.execute(
                    sql, (country_name,state_name, constituency_name, remark, file, type, lat, long, phone,timer))
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'

        elif role_input == "rls":
            country_name = level_input['country']
            district_name = level_input['district']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = '''INSERT INTO userdata_lga
                        (
                        country_id,
                        state_id,
                        const_id,
                        lga_id,
                        remark,
                    
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s,% s, % s, % s, % s, % s,%s, %s, %s,%s)'''
                        
                cur.execute(
                    sql, (country_name,state_name, lga_name, remark, file, type, lat, long, phone,timer))
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'

        elif role_input == "rws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")

            

            try:
                sql = '''INSERT INTO userdata_ward
                        (
                        country_id,
                        state_id,
                        const_id,
                        lga_id,
                        ward_id,
                        remark,               
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s,% s, % s, % s, % s, % s, % s, %s,%s,%s,%s)'''
                        
                cur.execute(
                    sql, (country_name,state_name, lga_name, ward_name,  remark, file, type, lat, long, phone,timer))
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'


        elif role_input == "rpa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = '''INSERT INTO userdata_pu
                        (
                        country_id,
                        state_id,
                        lga_id,
                        const_id,
                        ward_id,
                        pu_id,
                        remark,
                        file,
                        file_type,
                        lat,
                        long,
                        phone,
                        date

                        )
                        VALUES(% s, % s,% s, % s, % s, % s, % s, % s, % s, %s, %s,%s)'''
                        
                cur.execute(
                    sql, (country_name,state_name, lga_name, ward_name, pu_name,  remark, file, type, lat, long, phone,timer))
                conn.commit()
            # app.conn.close()
                return '1'
            except:
                return '0'
        
        
        



        
def message(user):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    name = user_data['name']
    aspirant_photo = ''
    typo =user_data['type_of_election'] 

    now = datetime.now(nigeria)
  
    with get_db2() as conn:
        cur = conn.cursor()
        if role_input == "pns":
            country_name = level_input['country']
            timer = now.strftime("%m/%d/%Y %H:%M")
            try:
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at National"]
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            except:
                return '0'
        
        elif role_input == "pss":
            country_name = level_input['country']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
       
            try:
                sql = f"""select distinct state_name from pu_result_table where state_id={state_name}"""
                print()
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at " +f"{result[0]}"]
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            # app.conn.close()
            except:
                return '0'
        
                
        elif role_input == "pls":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = f"""select distinct state_name,lga_name from pu_result_table where state_id={state_name} and lga_id={lga_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at " +f"{result[0]}/{result[1]}"]
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            # app.conn.close()
            except:
                return '0'

        elif role_input == "pws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = f"""select distinct state_name,lga_name,ward_name from pu_result_table where state_id={state_name} and lga_id={lga_name} and ward_id={ward_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at " +f"{result[0]}/{result[1]}/{result[2]}"]
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            # app.conn.close()
                return '1'
            except:
                return '0'

        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = f"""select distinct state_name,lga_name,ward_name,pu_name from pu_result_table where state_id={state_name} and lga_id={lga_name} and ward_id={ward_name} and pu_id={pu_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Agent" ]
                message4 = ["at " +f"{result[0]}/{result[1]}/{result[2]}/{result[3]}"]
                
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            # app.conn.close()
                return '1'
            except:
                return '0'
            
        elif role_input == "sss":
            country_name = level_input['country']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            try:
                sql = f"""select distinct state_name from sen_pu_table where state_id={state_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at " +f"{result[0]}"]
                
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            except:
                return '0'

           
        
        elif role_input == "sds":
            country_name = level_input['country']
            district_name = level_input['district']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            try:
                sql = f"""select distinct state_name,district_name from sen_pu_table where state_id={state_name} and district_id={district_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at " +f"{result[0]}/{result[1]}"]
                
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            except:
                return '0'
            
        
            


        elif role_input == "sls":
            country_name = level_input['country']
            district_name = level_input['district']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")
            try:
                sql = f"""select distinct state_name,district_name,lga_name from sen_pu_table where state_id={state_name} and district_id={district_name} and lga_id={lga_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at " +f"{result[0]}/{result[1]}/{result[2]}"]
                
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            except:
                return '0'

        elif role_input == "sws":
            country_name = level_input['country']
            state_name = level_input['state']
            district_name = level_input['district']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = f"""select distinct state_name,district_name,lga_name,ward_name from sen_pu_table where state_id={state_name} and district_id={district_name} and lga_id={lga_name} and ward_id={ward_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at " +f"{result[0]}/{result[1]}/{result[2]}/{result[3]}"]
                
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                
                return out
            except:
                return '0'


        elif role_input == "spa":
            country_name = level_input['country']
            state_name = level_input['state']
            district_name = level_input['district']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = f"""select distinct state_name,district_name,lga_name,ward_name,pu_name from sen_pu_table where state_id={state_name} and district_id={district_name} and lga_id={lga_name} and ward_id={ward_name} and pu_id={pu_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Agent" ]
                message4 = ["at " +f"{result[0]}/{result[1]}/{result[2]}/{result[3]}/{result[4]}"]
                
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            except:
                return '0'
        
        elif role_input == "rss":
            country_name = level_input['country']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            try:
                sql = f"""select distinct state_name from rep_pu_table where state_id={state_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at " +f"{result[0]}"]
                
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            except:
                return '0'

        elif role_input == "rcs":
            country_name = level_input['country']
            constituency_name = level_input['constituency']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            try:
                sql = f"""select distinct state_name,constituency_name from rep_pu_table where state_id={state_name} and const_id={constituency_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at " +f"{result[0]}/{result[1]}"]
                
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            except:
                return '0'

        elif role_input == "rls":
            country_name = level_input['country']
            constituency_name = level_input['constituency']

            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")
            try:
                sql = f"""select distinct state_name,constituency_name,lga_name from rep_pu_table where state_id={state_name} and const_id={constituency_name} and lga_id={lga_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at " +f"{result[0]}/{result[1]}/{result[2]}"]
                
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            except:
                return '0'

        elif role_input == "rws":
            country_name = level_input['country']
            state_name = level_input['state']
            constituency_name = level_input['constituency']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = f"""select distinct state_name,constituency_name,lga_name,ward_name from rep_pu_table where state_id={state_name} and const_id={constituency_name} and lga_id={lga_name} and ward_id={ward_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Supervisor" ]
                message4 = ["at " +f"{result[0]}/{result[1]}/{result[2]}/{result[3]}"]
                
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            except:
                return '0'


        elif role_input == "rpa":
            country_name = level_input['country']
            state_name = level_input['state']
            constituency_name = level_input['constituency']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")

            try:
                sql = f"""select distinct state_name,constituency_name,lga_name,ward_name,pu_name from rep_pu_table where state_id={state_name} and const_id={constituency_name} and lga_id={lga_name} and ward_id={ward_name} and pu_id={pu_name}"""
                cur.execute(sql)
                result = cur.fetchone()
                message1 = ["Welcome"]
                message2 = [name]
                message3 = [typo + " " + "elections as Agent" ]
                message4 = ["at " +f"{result[0]}/{result[1]}/{result[2]}/{result[3]}/{result[4]}"]
                
                out = {"message":message1+message2+message3+message4,"aspirant_avatar":aspirant_photo}
                return out
            except:
                return '0'
        
        

def get_data(user):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    now = datetime.now(nigeria)
    with get_db2() as conn:
        cur = conn.cursor()

        if role_input == "pns":
            country_name = level_input['country']
            timer = now.strftime("%m/%d/%Y %H:%M")
            
            sql = f"""select * from country_result_table Where country_id = {country_name} """
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","TOTAL_VALID_VOTES_C","TOTAL_VOTES_CAST_C"]
    
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)

        elif role_input == "pss":
            country_name = level_input['country']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
           
            sql = f"""select * from state_result_table  Where country_id = {country_name} and state_id= {state_name} """
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","TOTAL_VALID_VOTES_C","TOTAL_VOTES_CAST_C"]
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)

        
                
        elif role_input == "pls":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")

            sql = f"""select * from lga_result_table  Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name}"""
            
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","TOTAL_VALID_VOTES_C","TOTAL_VOTES_CAST_C"]
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)


        elif role_input == "pws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")
            
            sql = f"""select * from ward_result_table  Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name} and ward_id= {ward_name}"""
            
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","TOTAL_VALID_VOTES_C","TOTAL_VOTES_CAST_C"]    
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)


        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")
            
            sql = f"""select * from pu_result_table  Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""
            
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_ACCREDITED_VOTERS","TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","BALLOT_ISSUED","UNUSED_BALLOT","SPOILED_BALLOT","VALID_VOTES_C","USED_BALLOT"]
    
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)

        
            
        elif role_input == "sds":
                 raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to View Presidential Elections"
        )        



        elif role_input == "rcs":
             raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to View Presidential Elections"
        )        
            



       



      


def get_data_senate(user):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    now = datetime.now(nigeria)
    with get_db2() as conn:
        cur = conn.cursor()

        if role_input == "pns":
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to View Senate Elections"
        )        
            
           

        elif role_input == "pss":
          raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to View Senate Elections"
        )        
            
        
                
        elif role_input == "pls":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")

            sql = f"""select * from  sen_lga_table  Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name}"""
            
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","TOTAL_VALID_VOTES_C","TOTAL_VOTES_CAST_C"]
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)


        elif role_input == "pws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")
            
            sql = f"""select * from sen_ward_table  Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name} and ward_id= {ward_name}"""
            
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","TOTAL_VALID_VOTES_C","TOTAL_VOTES_CAST_C"]    
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)


        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")
            
            sql = f"""select * from sen_pu_table  Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""
            
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_ACCREDITED_VOTERS","TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","BALLOT_ISSUED","UNUSED_BALLOT","SPOILED_BALLOT","VALID_VOTES_C","USED_BALLOT"]
    
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)

        
        elif role_input == "sds":
            country_name = level_input['country']
            district_name = level_input['district']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            
            sql = f"""select * from sen_district_table  Where country_id = {country_name}  and state_id= {state_name} and district_id = {district_name}"""
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","TOTAL_VALID_VOTES_C","TOTAL_VOTES_CAST_C"]    
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)



     


        elif role_input == "rcs":
             raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to View Senate Elections"
        )        
            
            



            

def get_data_rep(user):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    now = datetime.now(nigeria)
    with get_db2() as conn:
        cur = conn.cursor()

        if role_input == "pns":
             raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to View Rep Elections"
        )        
            

        elif role_input == "pss":
             raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to View Rep Elections"
        )        
            

        
                
        elif role_input == "pls":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")

            sql = f"""select * from rep_lga_table  Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name}"""
            
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","TOTAL_VALID_VOTES_C","TOTAL_VOTES_CAST_C"]
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)


        elif role_input == "pws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")
            
            sql = f"""select * from rep_ward_table  Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name} and ward_id= {ward_name}"""
            
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","TOTAL_VALID_VOTES_C","TOTAL_VOTES_CAST_C"]    
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)


        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")
            
            sql = f"""select * from rep_pu_table  Where country_id = {country_name} and state_id= {state_name} and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""
            
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_ACCREDITED_VOTERS","TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","BALLOT_ISSUED","UNUSED_BALLOT","SPOILED_BALLOT","VALID_VOTES_C","USED_BALLOT"]
    
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)

        
        elif role_input == "sds":
             raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to View Rep Elections"
        )        
            


      

        elif role_input == "rcs":
            country_name = level_input['country']
            constituency_name = level_input['constituency']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            
            sql = f"""select * from rep_constituency_table  Where country_id = {country_name}  and state_id= {state_name} and const_id= {constituency_name}"""
            
            final={}
            try:
                cur.execute(sql)
                results = cur.fetch_pandas_all()
                results = results.to_json(orient="records")
                results = json.loads(results)
                parties = ["A","AA","AAC","ADC","ADP","APC","APGA","APM","APP","BP","LP","NNPP","NRM","PDP","PRP","SDP","YPP","ZLP"]
                total =["TOTAL_REGISTERED_VOTERS","TOTAL_REJECTED_VOTES","TOTAL_VALID_VOTES_C","TOTAL_VOTES_CAST_C"]    
                data = ['DATE_TIME', 'PERSON_COLLATED']
                parties_results = {}
                total_results={}
                other_data_results={}
                for key in parties:
                    parties_results.update( {key:results[0][key]})
               
                for key in total:
                    total_results.update( {key:results[0][key]})
                
                other_data_results.update({'person_collated':user_data['name']})
                other_data_results.update({"time":timer})

                
                final['results'] = parties_results
                final['total'] = total_results
                final['other_data'] = other_data_results
                return final
            except Exception as e:
                print(e)
                return str(e)







from fastapi import status, HTTPException

def submit_data_senate(user,userdata_collate):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    now = datetime.now(nigeria)
    with get_db2() as conn:
        cur = conn.cursor()

        if role_input == "pns":
            
            raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail=f'You are not Authorized to collate Senate Elections'
    )
        
        elif role_input == "pss":

            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to collate Senate Elections"
        )
            
        
                
        elif role_input == "pls":
            country_name = level_input['country']
            # district_name = level_input['district']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")
            del userdata_collate['UNUSED_BALLOT']
            del userdata_collate['SPOILED_BALLOT']
            del userdata_collate['USED_BALLOT']
            del userdata_collate['BALLOT_ISSUED']
            del userdata_collate['Total_Accredited_voters']
            userdata_collate['TOTAL_VALID_VOTES_C'] = userdata_collate['VALID_VOTES_C']

            del userdata_collate['VALID_VOTES_C']
            sql = f"""SELECT DISTINCT state_id,state_name, district_id,district_name FROM sen_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            district_name = results[0]['DISTRICT_ID']
            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            
            query = ", ".join(query)
            sql = f"""Update sen_lga_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name} and state_id= {state_name} and district_id = {district_name} and lga_id= {lga_name}"""
            
            try:
                cur.execute(sql)
                # results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
            
            # return {"You are not Authorized to collate Senate Elections"}
            

        elif role_input == "pws":
            country_name = level_input['country']
            # district_name = level_input['district']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")
            del userdata_collate['UNUSED_BALLOT']
            del userdata_collate['SPOILED_BALLOT']
            del userdata_collate['USED_BALLOT']
            del userdata_collate['BALLOT_ISSUED']
            del userdata_collate['Total_Accredited_voters']
            userdata_collate['TOTAL_VALID_VOTES_C'] = userdata_collate['VALID_VOTES_C']
            del userdata_collate['VALID_VOTES_C']
            sql = f"""SELECT DISTINCT state_id,state_name, district_id,district_name FROM sen_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            district_name = results[0]['DISTRICT_ID']
            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            
            query = ", ".join(query)
            sql = f"""Update sen_ward_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name} and state_id= {state_name} and district_id = {district_name} and lga_id= {lga_name} and ward_id= {ward_name}"""
            
            try:
                cur.execute(sql)
                # results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
            
            

        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            sql = f"""SELECT DISTINCT state_id,state_name, district_id,district_name FROM sen_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            district_name = results[0]['DISTRICT_ID']
            timer = now.strftime("%m/%d/%Y %H:%M")
            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            
            query = ", ".join(query)
            sql = f"""Update sen_pu_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name} and state_id= {state_name} and district_id ={district_name} and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""
            
            try:
                cur.execute(sql)
                # results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
        
        elif role_input == "sds":
            country_name = level_input['country']
            district_name = level_input['district']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            del userdata_collate['UNUSED_BALLOT']
            del userdata_collate['SPOILED_BALLOT']
            del userdata_collate['USED_BALLOT']
            del userdata_collate['BALLOT_ISSUED']
            del userdata_collate['Total_Accredited_voters']
            userdata_collate['TOTAL_VALID_VOTES_C'] = userdata_collate['VALID_VOTES_C']
            del userdata_collate['VALID_VOTES_C']
            
            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            
            query = ", ".join(query)
            sql = f"""Update sen_district_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name}  and state_id= {state_name} and district_id = {district_name}"""
            
            try:
                cur.execute(sql)
                # results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)



            
            


            

        elif role_input == "rcs":
              raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to collate Senate Elections"
        )
            
            



           

def cancel_data_senate(user,userdata_collate):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    now = datetime.now(nigeria)
    with get_db2() as conn:
        cur = conn.cursor()
        if role_input == "pns":
               raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to Cancel Senate Elections"
        )
            
            
        
        elif role_input == "pss":
             raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to Cancel Senate Elections"
        )
            
        
                
        elif role_input == "pls":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            sql = f"""SELECT DISTINCT state_id,state_name, district_id,district_name FROM sen_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            district_name = results[0]['DISTRICT_ID']
            timer = now.strftime("%m/%d/%Y %H:%M")
  
            sql = f"""Update sen_lga_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0,TOTAL_VALID_VOTES_C=0, Total_Rejected_votes=0,TOTAL_VOTES_CAST_C=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} and district_id={district_name} and lga_id= {lga_name} """
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
             
             
            

        elif role_input == "pws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            sql = f"""SELECT DISTINCT state_id,state_name, district_id,district_name FROM sen_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            district_name = results[0]['DISTRICT_ID']
            timer = now.strftime("%m/%d/%Y %H:%M")
  
            sql = f"""Update sen_ward_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0, TOTAL_VALID_VOTES_C=0, Total_Rejected_votes=0,TOTAL_VOTES_CAST_C=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} and district_id={district_name} and lga_id= {lga_name} and ward_id= {ward_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
             
            

        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            sql = f"""SELECT DISTINCT state_id,state_name, district_id,district_name FROM sen_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            district_name = results[0]['DISTRICT_ID']
            timer = now.strftime("%m/%d/%Y %H:%M")
  
            sql = f"""Update sen_pu_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0, BALLOT_ISSUED=0,UNUSED_BALLOT=0,SPOILED_BALLOT=0,VALID_VOTES_C=0,USED_BALLOT=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} and district_id={district_name} and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
        
        elif role_input == "sds":
            country_name = level_input['country']
            state_name = level_input['state']
            district_name = level_input['district']
        
            timer = now.strftime("%m/%d/%Y %H:%M")
  
            sql = f"""Update sen_district_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0, TOTAL_VALID_VOTES_C=0, Total_Rejected_votes=0,TOTAL_VOTES_CAST_C=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} and district_id={district_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
             
            



        elif role_input == "rcs":
             raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to Cancel Senate Elections"
        )
           


           



def submit_data_rep(user,userdata_collate):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    now = datetime.now(nigeria)
    with get_db2() as conn:
        cur = conn.cursor()

        if role_input == "pns":
            
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to collate Rep Elections"
        )
        
        elif role_input == "pss":
                 raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to collate Rep Elections"
        )
            
        
                
        elif role_input == "pls":
            country_name = level_input['country']
            # constituency_name = level_input['constituency']
            state_name = level_input['state']
            lga_name = level_input['lga']
            timer = now.strftime("%m/%d/%Y %H:%M")
            del userdata_collate['UNUSED_BALLOT']
            del userdata_collate['SPOILED_BALLOT']
            del userdata_collate['USED_BALLOT']
            del userdata_collate['BALLOT_ISSUED']
            del userdata_collate['Total_Accredited_voters']
            userdata_collate['TOTAL_VALID_VOTES_C'] = userdata_collate['VALID_VOTES_C']
            del userdata_collate['VALID_VOTES_C']
            sql = f"""SELECT DISTINCT state_id,state_name, const_id,constituency_name FROM rep_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            constituency_name = results[0]['CONST_ID']

            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            
            query = ", ".join(query)
            sql = f"""Update rep_lga_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name} and state_id= {state_name} and const_id= {constituency_name} and lga_id= {lga_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
            

        elif role_input == "pws":
            country_name = level_input['country']
            # constituency_name = level_input['constituency']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")
            del userdata_collate['UNUSED_BALLOT']
            del userdata_collate['SPOILED_BALLOT']
            del userdata_collate['USED_BALLOT']
            del userdata_collate['BALLOT_ISSUED']
            del userdata_collate['Total_Accredited_voters']
            userdata_collate['TOTAL_VALID_VOTES_C'] = userdata_collate['VALID_VOTES_C']
            del userdata_collate['VALID_VOTES_C']
            sql = f"""SELECT DISTINCT state_id,state_name, const_id,constituency_name FROM rep_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            constituency_name = results[0]['CONST_ID']
            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            
            query = ", ".join(query)
            sql = f"""Update rep_ward_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name} and state_id= {state_name} and const_id= {constituency_name} and lga_id= {lga_name} and ward_id= {ward_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)

            

        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            sql = f"""SELECT DISTINCT state_id,state_name, const_id,constituency_name FROM rep_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            constituency_name = results[0]['CONST_ID']
            
            timer = now.strftime("%m/%d/%Y %H:%M")
            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            
            query = ", ".join(query)
            sql = f"""Update rep_pu_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name} and state_id= {state_name} and const_id={constituency_name} and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""
            
            try:
                cur.execute(sql)
                # results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
        
        elif role_input == "sds":
                 raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to collate Rep Elections"
        )
            


     

            

        elif role_input == "rcs":
            country_name = level_input['country']
            constituency_name = level_input['constituency']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            del userdata_collate['UNUSED_BALLOT']
            del userdata_collate['SPOILED_BALLOT']
            del userdata_collate['USED_BALLOT']
            del userdata_collate['BALLOT_ISSUED']
            del userdata_collate['Total_Accredited_voters']
            userdata_collate['TOTAL_VALID_VOTES_C'] = userdata_collate['VALID_VOTES_C']
            del userdata_collate['VALID_VOTES_C']
            query = [
             f"{key}={value[0] if isinstance(value, list) else value}" for key, value in userdata_collate.items()]
            
            query = ", ".join(query)
            sql = f"""Update rep_constituency_table SET {query} , date_time ='{timer}',status='collated' Where country_id = {country_name}  and state_id= {state_name} and const_id= {constituency_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)


        

           
        
           

def cancel_data_rep(user,userdata_collate):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    now = datetime.now(nigeria)
    with get_db2() as conn:
        cur = conn.cursor()
        if role_input == "pns":
                  raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to Cancel Rep Elections"
        )
            
        
        elif role_input == "pss":
              raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to Cancel Rep Elections"
        )
            
        
                
        elif role_input == "pls":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            sql = f"""SELECT DISTINCT state_id,state_name, const_id,constituency_name FROM rep_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            constituency_name = results[0]['CONST_ID']
            timer = now.strftime("%m/%d/%Y %H:%M")
  
            sql = f"""Update rep_lga_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0, TOTAL_VALID_VOTES_C=0, Total_Rejected_votes=0,TOTAL_VOTES_CAST_C=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} and const_id={constituency_name} and lga_id= {lga_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
            

        elif role_input == "pws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            sql = f"""SELECT DISTINCT state_id,state_name, const_id,constituency_name FROM rep_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            constituency_name = results[0]['CONST_ID']
            timer = now.strftime("%m/%d/%Y %H:%M")
  
            sql = f"""Update rep_ward_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0, TOTAL_VALID_VOTES_C=0, Total_Rejected_votes=0,TOTAL_VOTES_CAST_C=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} and const_id={constituency_name} and lga_id= {lga_name} and ward_id= {ward_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
            

        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            sql = f"""SELECT DISTINCT state_id,state_name, const_id,constituency_name FROM rep_pu_table WHERE 
            state_id = {state_name} AND 
            lga_id = {lga_name}"""
        # else:
        #     sql = "SELECT DISTINCT state_id, lga_id, WARD_ID ,WARD_NAME FROM pu_result_table"

        
            cur.execute(sql)
            results = cur.fetch_pandas_all()
            results = results.to_json(orient="records")
            results = json.loads(results)            #cur.close()
            constituency_name = results[0]['CONST_ID']
            timer = now.strftime("%m/%d/%Y %H:%M")
  
            sql = f"""Update rep_pu_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0, BALLOT_ISSUED=0,UNUSED_BALLOT=0,SPOILED_BALLOT=0,VALID_VOTES_C=0,USED_BALLOT=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} and const_id={constituency_name} and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
        
        elif role_input == "sds":
              raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not Authorized to Cancel Rep Elections"
        )
            


            

        elif role_input == "rcs":
            country_name = level_input['country']
            state_name = level_input['state']
            constituency_name = level_input['constituency']
            timer = now.strftime("%m/%d/%Y %H:%M")
  
            sql = f"""Update rep_constituency_table  SET status='canceled', A=0, AA=0, AAC=0, ADC=0, ADP=0, APC=0, APGA=0, APM=0, APP=0, BP=0, LP=0, NNPP=0, NRM=0, PDP=0, PRP=0, SDP=0,TOTAL_VALID_VOTES_C=0, Total_Rejected_votes=0,TOTAL_VOTES_CAST_C=0, YPP=0, ZLP=0 , date_time ='{timer}'
 Where country_id = {country_name} and state_id= {state_name} and const_id={constituency_name} """
            
            try:
                cur.execute(sql)
                results = cur.fetchall()
                conn.commit()
                res= {}
                res.update({'person_collated':user_data['name']})
                res.update({"time":timer})
                return res
            except Exception as e:
                print(e)
                return str(e)
           


        







import re
import difflib



def scanner(user,rawtext,table,final_map,sharp):
    now = datetime.now(nigeria)
    timer = now.strftime("%m/%d/%Y %H:%M")
    # user_data = user['user']
    user_data = json.loads(user)
    name = user_data[0]
    level= user_data[3]

    user_data =user
    total_register = ""
    total_acrredited =""
    total_rejected = ""
    spoilled =""
    valid_votes =""
    used_ballot =""
    ballot_issued = ""
    unused_ballot = ""
    for key,value in final_map.items():
        if "Voters on the Register" in key:
            value= re.sub("\D","",value)
            if value =="":
                value = 0
            value = int(value)
            total_register += f"TOTAL_REGISTERED_VOTERS ={value}"
            
        elif "Accredited" in key:
            value= re.sub("\D","",value)
            if value =="":
                value = 0
            value = int(value)
            total_acrredited += f"TOTAL_ACCREDITED_VOTERS ={int(value)}"
        elif "Rejected" in key:
            value= re.sub("\D","",value)
            if value =="":
                value = 0
            value = int(value)
            total_rejected += f"TOTAL_REJECTED_VOTES={value}"
        elif "Spoilled" in key:
            value= re.sub("\D","",value)
            if value =="":
                value = 0
            value = int(value)
            spoilled += f"SPOILED_BALLOT={value}"
        elif "Total Valid Votes" in key:
            value= re.sub("\D","",value)
            if value =="":
                value = 0
            value = int(value)
            valid_votes += f"VALID_VOTES_C ={value}"
        elif "Used Ballots Papers" in key:
            value= re.sub("\D","",value)
            if value =="":
                value = 0
            value = int(value)
            used_ballot += f"USED_BALLOT ={value}"
        elif "Ballot Papers Issued" in key:
            value= re.sub("\D","",value)
            if value =="":
                value = 0
            value = int(value)
            ballot_issued += f"BALLOT_ISSUED ={value}"
        elif "Unused Ballot Papers" in key:
            value= re.sub("\D","",value)
            if value =="":
                value = 0
            value = int(value)
            unused_ballot += f"UNUSED_BALLOT ={value}"
        else:
            pass

    numberlist= [total_register,total_acrredited,total_rejected,spoilled,valid_votes,used_ballot,ballot_issued,unused_ballot]    
    numberlist = [x for x in numberlist if x != ""]
    numberquery = ", ".join(numberlist)
            
            
            
            
            
            


    party_real_values = ['A', 'AA', 'AAC', 'ADC', 'ADP', 'APC', 'APGA', 'APM', 'APP', 'BP', 'LP', 'NNPP', 'NRM', 'PDP', 'PRP', 'SDP','YPP', 'ZLP']
    for i, tab in enumerate(table):
        if "IN WORDS" in tab:
            table_values = table[i+1:]
    final_list = []
    party_val = []
    party_values = []
    for i, val in enumerate(table_values):
        values  =  val[2:3][0]
        party = val[1:2][0]
        party_val.append(party)
        party_values.append(values)

    party_val = [x for x in party_val if x != ' ']
    # print(party_val)
    # valuess = [x for x in valuess if x != ' ']
    party_matching = []
    for p in party_val:
        
        v = difflib.get_close_matches(p, party_real_values)
        if p =="POP":
            v[0] = "PDP"
        elif p =="AOP":
            v[0] = "ADP"
        elif p =="SOP":
            v[0] ="SDP"
        elif p =="AOC":
            v[0] ="ADC"
        party_matching.append(v[0])
    values_matching = []


    for v in party_values:
        n= re.sub("\D","",v)
        if n =="":
            n = 0
        n = int(n)
        values_matching.append(n)
        
    party_dictionary =  dict(zip(party_matching,values_matching))

    level_input = level

    
    country_name = level_input['country']
    state_name = level_input['state']
    district_name = level_input['district']
    constituency_name = level_input['constituency']
    lga_name = level_input['lga']
    ward_name = level_input['ward']
    pu_name = level_input['pollingUnit']

    # country_name = 1
    # state_name = 1
    # district_name = 1
    # constituency_name = 1
    # lga_name = 10
    # ward_name = 1
    # pu_name = 1


     
    s3 = boto3.resource('s3')
    bucket = "electionuploads104030-dev" 
    
    
   
    part = ""
    for key, value in party_dictionary.items():
        part += f"{key} ={value},"
    part = part[:-1]
    for val in rawtext:
        if "HOUSE OF REPRESENTATIVES" in val:
            table_name = "REP_PU_TABLE"
            final_query = f"Update {table_name} SET {part},{numberquery} where country_id ={country_name} and state_id = {state_name} AND CONST_ID = {constituency_name} and lga_id={lga_name} and ward_id={ward_name} and pu_id = {pu_name}"
            image_string = cv2.imencode('.png', sharp)[1].tostring()
            image_name = f"collation/photos/rep/{country_name}_{state_name}_{constituency_name}_{lga_name}_{pu_name}.jpg"
            s3.Bucket(bucket).put_object(Key=image_name, Body=image_string, 
                                ContentType="image/png", ACL="public-read")
            sql = f"""Update rep_pu_table SET file='{image_name}' Where country_id = {country_name} and  state_id= {state_name}  and const_id= {constituency_name} and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""
            
            # sql = "Insert"
        elif "SENATE" in val:
            table_name = "SENATE_PU_TABLE"
            final_query = f"Update {table_name} SET {part},{numberquery} where country_id ={country_name} and state_id = {state_name} and district_id={district_name} and lga_id={lga_name} and ward_id={ward_name} and pu_id = {pu_name}"
            image_string = cv2.imencode('.png', sharp)[1].tostring()
            image_name = f"collation/photos/{country_name}_{state_name}_{district_name}_{lga_name}_{pu_name}_senate.jpg"
            s3.Bucket(bucket).put_object(Key=image_name, Body=image_string, 
                                ContentType="image/png", ACL="public-read")
            sql = f"""Update SENATE_PU_TABLE SET file='{image_name}' Where country_id = {country_name} and  state_id= {state_name}  and district_id= {district_name} and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""

        elif "PRESIDENT" in val:
            table_name = "PU_RESULT_TABLE"
            final_query = f"Update {table_name} SET {part},{numberquery} where country_id ={country_name} and state_id = {state_name} and lga_id={lga_name} and ward_id={ward_name} and pu_id = {pu_name}"
            image_string = cv2.imencode('.png', sharp)[1].tostring()
            image_name = f"collation/photos/{country_name}_{state_name}_{lga_name}_{pu_name}_presidential.jpg"
            s3.Bucket(bucket).put_object(Key=image_name, Body=image_string, 
                                ContentType="image/png", ACL="public-read")
            sql = f"""Update PU_RESULT_TABLE SET file='{image_name}' Where country_id = {country_name} and  state_id= {state_name}  and lga_id= {lga_name} and ward_id= {ward_name} and pu_id= {pu_name}"""

    with get_db2() as conn:
        cur = conn.cursor()
        try:
            cur.execute(final_query)
            cur.execute(sql)
            if table_name == 'REP_PU_TABLE':
                return {"message": f"Rep Submitted Successfully by {user_data['name']}"}
            elif table_name == "SENATE_PU_TABLE":
                return {"message": f"Senate Submitted Successfully by {user_data['name']}"}
            elif table_name == "PU_RESULT_TABLE":
                return  {"message": f"Presidential Submitted Successfully by {user_data['name']}"}
            else:
                return {"message": "Please capture again properly"}

        except:
            return {"message": "Please capture again properly"}


    
def get_data_time(user):
    user_data = user['user']
    role_input = user_data['role']
    level_input = user_data['level_childs']
    now = datetime.now(nigeria)
    timer = now.strftime("%m/%d/%Y %H:%M")

    with get_db2() as conn:
        cur = conn.cursor()

        if role_input == "pns":
            country_name = level_input['country']
            sql = f"""Update country_result_table  set time_start='{timer}' where country_id = 1 """
            try:
                cur.execute(sql)
                return {f"Started at {timer}"}
            except Exception as e:
                print(e)
                return str(e)
           
            
           

        elif role_input == "pss":
            country_name = level_input['country']
            state_name = level_input['state']

            sql = f"""Update state_result_table  set time_start='{timer}' where country_id = 1 and state_id={state_name}"""
            try:
                cur.execute(sql)
                return {f"Started at {timer}"}
            except Exception as e:
                print(e)
                return str(e)
           
              
            
        
                
        elif role_input == "pls":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            sql = f"""Update lga_result_table  set time_start='{timer}' where country_id = 1 and state_id={state_name}  and lga_id={lga_name} """
            try:
                cur.execute(sql)
                return {f"Started at {timer}"}
            except Exception as e:
                print(e)
                return str(e)
           
              


        elif role_input == "pws":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            timer = now.strftime("%m/%d/%Y %H:%M")
            
            sql = f"""Update ward_result_table  set time_start='{timer}' where country_id = 1 and state_id={state_name} and lga_id={lga_name} and ward_id={ward_name}"""
            try:
                cur.execute(sql)
                return {f"Started at {timer}"}
            except Exception as e:
                print(e)
                return str(e)
           
              


        elif role_input == "ppa":
            country_name = level_input['country']
            state_name = level_input['state']
            lga_name = level_input['lga']
            ward_name = level_input['ward']
            pu_name = level_input['pollingUnit']
            timer = now.strftime("%m/%d/%Y %H:%M")

            sql = f"""Update pu_result_table  set time_start='{timer}' where country_id = 1 and state_id={state_name} and lga_id={lga_name} and ward_id={ward_name} and pu_id={pu_name}"""
            try:
                cur.execute(sql)
                return {f"Started at {timer}"}
            except Exception as e:
                print(e)
                return str(e)
           
            
           

        
        elif role_input == "sds":
            country_name = level_input['country']
            district_name = level_input['district']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            
            sql = f"""Update sen_district_table  set time_start='{timer}' where country_id = 1 and state_id={state_name} and district_id={district_name} """
            try:
                cur.execute(sql)
                return {f"Started at {timer}"}
            except Exception as e:
                print(e)
                return str(e)
    

        elif role_input == "rcs":
            country_name = level_input['country']
            constituency_name = level_input['constituency']
            state_name = level_input['state']
            timer = now.strftime("%m/%d/%Y %H:%M")
            sql = f"""Update rep_constituency_table  set time_start='{timer}' where country_id = 1 and state_id={state_name} and const_id={constituency_name}"""
            try:
                cur.execute(sql)
                return {f"Started at {timer}"}
            except Exception as e:
                print(e)
                return str(e)
           
