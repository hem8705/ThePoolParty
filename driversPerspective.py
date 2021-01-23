##drivers perspective
import pandas as pd
import numpy as np
number=1
df=pd.DataFrame(np.array([[1,"a","Name",1,1,True]])
df.columns=["Number","Driver Name","Destination","Time of Departure","Driver Phone Number","Available Seats"]
class driversPerspective:
                def __init__(self,number,name,destination,timing,phoneNo,SeatsAvailable):
                    self.number=number
                    self.name=name
                    self.destination=destination
                    self.timing=timing
                    self.phoneNo=phoneNo
                    self.seatsAvailable

                def createRide(self):
                    #creating a ride for where they are going
                    number=number+1
                    name=input("What is your name")
                    destination=input("Enter destination")
                    timing=input("Enter time of departure")
                    phoneNo=input("Enter your phone number")
                    seatsAvailable=input("Enter number of seats available")
                    df2=pd.DataFrame({"Number":[Number],
                                      "Name":[Name],
                                      "Destination":[Destination],
                                      "Time of Departure":[timing],
                                      "Driver Phone number":[phoneNo],
                                      "Available Seats":[seatsAvailable]})
                    df.append(df2)

                
                
                    
