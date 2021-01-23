from flask import Flask, render_template, redirect, url_for, request
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to The HitchHiker" 

@app.route('/login', methods=['GET', 'POST'])
def login():
    df=pd.read_csv('PeopleDetails.csv')
    error = None
    success = None
    if request.method == 'POST':
        phnumber = request.form['phnumber']
        password = request.form['password']
        for counter in range(0,len(df.index)):
            if int(phnumber)==int(df.at[counter,"Phone Number"]):
                if password == df.at[counter,"Password"]:
                    success = 'Log in successful'
                elif password == '' :
                    error = "Please enter the password"
                elif phnumber == '' :
                    error = "Please enter your phone number"
                else :
                    error = 'Incorrect phone number or password'
    df.to_csv('PeopleDetails.csv')
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
    df.to_csv('PeopleDetails.csv')
    return render_template('signup.html', error=error, success=success)

@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard ():

    provide_ride=True
    user_id=3
    rides_provided=pd.DataFrame(np.array([[3,"a",2,False],[4,"b",54,True]]))
    rides_provided.columns=["Id","Name","Rides Provided","Show_on_Leaderboard"]

    class leaderboard:
    
        def __init__(self,user_id,name):
            self.user_id=user_id
            self.name=name
            
        def update_rides(self):
            num_rows,num_columns=rides_provided.shape
            if (provide_ride==True):
                for counter1 in range(0,num_columns):
                    print(rides_provided[0,counter1], self.user_id)
                    if (int(rides_provided[0,counter1])==user_id):
                        rides_provided[2,counter1]=str(int(rides_provided[2,counter1])+1)
                        
        def print_leaderboard(self):
            in_order=pd.DataFrame(rides_provided.sort_values("Rides Provided",ascending=False,ignore_index=True))
            in_order.columns=["Id","Name","Rides Provided", "Show_on_Leaderboard"]
            #print(in_order)
            #for counter2 in range(0,len(rides_provided.index)):
                #print(in_order.at[counter2,"Name"]," ",in_order.at[counter2,"Rides Provided"])
            answer = "Hello, World"
            return answer

    go1=leaderboard(3,"a")
    return render_template('leaderboard.html', answer=go1.print_leaderboard())


if __name__ == '__main__':
    app.run(debug=True)
