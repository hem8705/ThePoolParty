from flask import Flask, render_template, redirect, url_for, request
import pandas as pd
import numpy as np
import phonenumbers as pn
import math
import requests
import googlemaps
df=pd.read_csv('PeopleDetails.csv')
drivers=pd.read_csv('Drivers.csv')
riders=pd.read_csv('Riders.csv')
url=data="https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
api_key="AIzaSyBQiGBbojdpWwjM-yBb63NVSIXr_raPPQY"
global ispresent
global ispresent1
ispresent = None
ispresent1 = None

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def homepage ():
    return render_template ('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    df=pd.read_csv('PeopleDetails.csv')
    error = None
    success = None
    global phnumber
    if request.method == 'POST':
        phnumber = request.form['phnumber']
        password = request.form['password']
        dct=pn.parse(phnumber,"IN")
        for counter in range(0,len(df.index)):
            if int(phnumber)==int(df.at[counter,"Phone Number"]):
                if password == df.at[counter,"Password"]:
                    success = 'Log in successful'
                elif password == '' :
                    error = "Please enter the password"
                elif phnumber == '' :
                    error = "Please enter your phone number"
                elif dct['valid'] == False :
                    error = 'Please enter a subscribed phone number'
                else :
                    error = 'Incorrect phone number or password'
    df.to_csv('PeopleDetails.csv', index=False)
    return render_template('login.html', error=error, success=success)

@app.route('/signup', methods=['GET', 'POST'])
def signup ():
    df=pd.read_csv('PeopleDetails.csv')
    error = None
    success = None
    flag1 = 0
    flag2 = 0
    if request.method == 'POST':
        phnumber = request.form['phnumber']
        password = request.form['password-1']
        name = request.form['name']
        vehicle = request.form['vehicle']
        plateno = request.form['plateno']
        for counter in range(0,len(df.index)):
            if int(phnumber)==int(df.at[counter,"Phone Number"]):
                flag1 = 1
        for i in list(name):
            if i == ' ' or len(list(name)) < 5:
                flag2 = 1
        if request.form['password-1'] != request.form['password-2']:
            error = "Passwords don't match. Please try again."
        elif flag1 == 1 :
            error = "Phone number is already used for another account, please use a different number."
        elif len(password) < 8 :
            error = "Password needs to be a minimum of 8 characters"
        elif flag2 == 0 :
            error = "Name should have two words and have more than 5 characters"
        elif len(phnumber) != 10 :
            error = "Phone number should be 10 digits long (Enter without spaces or symbols)"
        elif phnumber == '' or name == '' or password == '':
            error = "Phone number, name and password are mandatory requirements"
        else:
            data_to_append = pd.DataFrame(np.array([[phnumber, password, name, 0, 0, True, vehicle, plateno]]))
            data_to_append.columns = ["Phone Number", "Password", "Name", "Rides Provided", "Rides Taken", "Safe", "Vehicle Details", "Vehicle Number Plate"]
            df=df.append(data_to_append, ignore_index=True)
            success = 'Sign up successful'
    df.to_csv('PeopleDetails.csv', index=False)
    return render_template('signup.html', error=error, success=success)

@app.route('/mainmenu', methods = ['GET', 'POST'])
def mainpage ():
    global ispresent, ispresent1
    ispresent = None
    ispresent1 = None
    return render_template('mainmenu.html', ispresent=ispresent, ispresent1=ispresent1)

@app.route('/driver', methods = ['GET', 'POST'])
def driver ():
    global mode
    mode = 'driver'
    global ispresent
    #ispresent = True

    drivers=pd.read_csv('Drivers.csv')
    for counter in range (0, len(df.index)):
        if int(phnumber) == int(df.at[counter, "Phone Number"]):
            val = df.at[counter, "Vehicle Details"]
            if type(val) == float :
                isthere = False
            else :
                isthere = True

    error = None
    success = None
    for counter in range (0, len(drivers.index)):
        if int(phnumber) == int(drivers.at[counter, "Phone Number"]):
            error = 'Ride offer already sent. Please wait till someone around you accepts the ride.'

        elif request.method == 'POST':
            destination = request.form['destination']
            time = request.form['time']
            seatsAvailable = request.form['seatsavailable']
            location = request.form['location']
            cprox = request.form['cprox']
            fprox = request.form['fprox']

            for counter in range (0, len(df.index)):
                if int(phnumber) == int(df.at[counter, "Phone Number"]):
                    name = df.at[counter, "Name"]
                    vehicle = df.at[counter, "Vehicle Details"]
                    plateno = df.at[counter, "Vehicle Number Plate"]

            data_to_append = pd.DataFrame(np.array([[name, phnumber, location, destination, seatsAvailable, time, vehicle, plateno, cprox, fprox]]))
            data_to_append.columns = ["Name", "Phone Number", "Location", "Destination", "Seats Available", "Time", "Vehicle Details", "Vehicle Number Plate", "Location Proximity", "Destination Proximity"]
            drivers=drivers.append(data_to_append, ignore_index=True)
            drivers.to_csv('Drivers.csv', index=False)
            success = True

            connected = pd.read_csv('ConnectedRides.csv')

            val = connected
            val1 = val[["Rider Ph", "Rider Name", "Rider Loc", "Rider Dest", "Rider Time"]]

            test = val1.at[0, "Rider Ph"]
            if type(test) == float :
                ispresent = False
            else :
                ispresent = True
                html = val1.to_html()

                text_file = open("templates/myriders.html", "w")
                text_file.write(html)
                text_file.close()

    return render_template('driversPerspective.html', isthere=isthere, success=success, error=error, ispresent=ispresent)

@app.route('/user', methods = ['GET', 'POST'])
def user ():
    global mode
    mode = 'rider'
    ispresent = False 
    ispresent1 = False

    error = None
    riders=pd.read_csv('Riders.csv')

    for counter in range (0, len(riders.index)):
        if int(phnumber) == int(riders.at[counter, "Phone Number"]):
            error = 'Ride request already sent. Please wait till someone around you offers a ride.'

        elif request.method == 'POST' :
            location = request.form['location']
            destination = request.form['destination']
            time = request.form['time']

            def find_name (phnumber):
                df=pd.read_csv('PeopleDetails.csv')
                for counter in range (0, len(df.index)):
                    if int(phnumber) == int(df.at[counter, "Phone Number"]):
                        name = df.at[counter, "Name"]
                        return name

            ride_to_append = pd.DataFrame(np.array([[find_name(phnumber), phnumber, location, destination, time]]))
            ride_to_append.columns = ["Name", "Phone Number", "Location", "Destination", "Time"]
            riders=riders.append(ride_to_append, ignore_index=True)
            riders.to_csv('Riders.csv', index=False)

    return render_template('userPerspective.html', index=False, error=error)

@app.route('/connector', methods = ['GET', 'POST'])
def connector ():
    ispresent = False
    ispresent1 = False

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
            else:
                close_loc=False
            r2=requests.get(url+"origins="+self.user_loc+"&destinatioans="+self.driver_loc+"&key="+api_key)
            time_difference=r.json()["rows"][0]["elements"][0]["distance"]["value"]
            time_difference = time_difference/1000
            if (time_difference<=int(self.des_value)):
                #note: in kilometers
                close_des=True
            else:
                close_des=False

            if close_des == True and close_loc == True :
                can_connect = True
            else :
                can_connect = False

            return can_connect

    #note: need to make sorting algo in terms of time

    rider1=pd.read_csv('Riders.csv')
    driver1=pd.read_csv('Drivers.csv')
    connected = pd.read_csv('ConnectedRides.csv')
    for counter in range (0, len(rider1.index)):
        if int(phnumber) == int(rider1.at[counter, "Phone Number"]):
            r_name = rider1.at[counter, "Name"]
            r_location = rider1.at[counter, "Location"]
            r_destination = rider1.at[counter, "Destination"]
            r_time = rider1.at[counter, "Time"]

            for counter1 in range (0, len(driver1.index)):
                d_ph = driver1.at[counter1, "Phone Number"]
                d_name = driver1.at[counter1, "Name"]
                d_location = driver1.at[counter1, "Location"]
                d_destination = driver1.at[counter1, "Destination"]
                d_time = driver1.at[counter1, "Time"]
                d_locprox = driver1.at[counter1, "Location Proximity"]
                d_destprox = driver1.at[counter1, "Destination Proximity"]
                d_vehicle = driver1.at[counter1, "Vehicle Details"]
                d_plateno = driver1.at[counter1, "Vehicle Number Plate"]
                d_seats = driver1.at[counter1, "Seats Available"]

                go1 = Connect(r_location, d_location, r_destination, d_destination, d_locprox, d_destprox)

                if go1.check() == True :
                    connected = pd.DataFrame()
                    connected_ap = pd.DataFrame(np.array([[d_ph, phnumber, d_name, r_name, d_location, r_location, d_destination, r_destination, d_time, r_time, d_vehicle, d_plateno, d_seats]]))
                    connected_ap.columns = ["Driver Ph", "Rider Ph", "Driver Name", "Rider Name", "Driver Loc", "Rider Loc", "Driver Dest", "Rider Dest", "Driver Time", "Rider Time", "Vehicle Details", "Vehicle Number Plate", "Seats Available"]
                    connected = connected.append(connected_ap, ignore_index=True)
                    connected.to_csv('ConnectedRides.csv', index=False)
                    break

    if mode == 'rider' :
        val = connected
        val1 = val[["Driver Ph", "Driver Name", "Driver Loc", "Rider Loc", "Driver Dest", "Driver Time", "Vehicle Details", "Vehicle Number Plate"]]
        html = val1.to_html()

        text_file = open("templates/connector.html", "w") 
        text_file.write(html) 
        text_file.close()

        add1 = val1.at[0, "Driver Loc"]
        add2 = val1.at[0, "Rider Loc"]

        test = val1.at[0, "Driver Ph"]
        if type(test) == float :
            ispresent1 = False
        else :
            ispresent1 = True

    return render_template ('connector.html')

@app.route('/map', methods = ['GET', 'POST'])
def map ():
    connected = pd.read_csv('ConnectedRides.csv')
    val = connected
    val1 = val[["Driver Ph", "Driver Name", "Driver Loc", "Rider Loc", "Driver Dest", "Driver Time", "Vehicle Details", "Vehicle Number Plate"]]

    add1 = val1.at[0, "Driver Loc"]
    add2 = val1.at[0, "Rider Loc"]

    return render_template ('maps.html', add1=add1, add2=add2)

if __name__ == '__main__' :
    app.run(debug=True)