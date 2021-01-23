import googlemaps
import requests
import pandas as pd
import numpy as np

# =============================================================================
url=data="https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
api_key="AIzaSyBQiGBbojdpWwjM-yBb63NVSIXr_raPPQY"
#ad1=input("Adress 1")
#ad2=input("Adress 2")
#data="https://www.googleapis.com/geolocation/v1/geolocate?"
#r=requests.get(url+"origins="+ad1+"&destinations="+ad2+"&key="+api_key)

#distance=r.json()["rows"][0]["elements"][0]["distance"]["value"]
#if(distance/1000<=2.0):
 #   print("yes")
    
class Connect:
    def __init__(self,user_loc,driver_loc,user_des,driver_des,loc_value,des_value):
        self.user_loc=user_loc
        self.driver_loc=user_loc
        self.user_des=user_des
        self.driver_des=driver_des
        self.loc_value=loc_value
        self.des_value=des_value
    
    def check(self):
        r=requests.get(url+"origins="+self.user_loc+"&destinations="+self.driver_loc+"&key="+api_key)
        distance=r.json()["rows"][0]["elements"][0]["distance"]["value"]
        if(distance/1000<=int(self.loc_value)):
            close_loc=True
            print("a")
        else:
            close_loc=False
            print("b")
        r2=requests.get(url+"origins="+self.user_loc+"&destinatioans="+self.driver_loc+"&key="+api_key)
        time_difference=r.json()["rows"][0]["elements"][0]["duration"]["value"]
        if (time_difference<=int(self.des_value)):
            #note: in seconds
            close_des=True
            print("c")
        else:
            close_des=False
            print("d")
    def distance_calc(self):
        r3=requests.get(url+"origins="+self.user_loc+"&destinations="+self.user_des+"&key="+api_key)
        distance_done=r3.json()["rows"][0]["elements"][0]["distance"]["value"]
        Cbn=pd.read_csv("Carbon Saved.csv")
        print(Cbn)
        Cbn.iat[0,0]=float(float(Cbn.iat[0,0])+float(distance_done/1000))
        print(Cbn.iat[0,0])
        Cbn.at[0,"Carbon Saved"]=float((float(Cbn.iat[0,0])*138.87)/1000)
        Cbn.to_csv("Carbon Saved.csv",index=False)
        
