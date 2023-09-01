import tkinter as tk              
from tkinter import ttk
import tkinter.font as font  
from tkinter import *
from track import get_planet_track, get_sat_track,get_voyager_track
import RPi.GPIO as GPIO
import click
from skyfield.api import load, wgs84, EarthSatellite, utc
import time
import serial
import sys
import threading
import numpy as np


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# set up GPIO pins
#X az
GPIO.setup(3, GPIO.OUT) # down
GPIO.setup(5, GPIO.OUT) # up
 
#Y
GPIO.setup(7, GPIO.OUT) # up and down elevaton altitude
GPIO.setup(8, GPIO.OUT)



root = tk.Tk()

root.geometry('900x900')
v = tk.IntVar()
root.title("Satellite Tracking Module")
tabControl = ttk.Notebook(root)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

  
tabControl.add(tab1, text ='Main')
tabControl.add(tab2, text ='Auto Tracking')
tabControl.add(tab3, text ='Manual Operation')
tabControl.add(tab4, text ='Setup')
tabControl.pack(expand = 1, fill ="both")

tabControl.hide(tab2)
tabControl.hide(tab3)
tabControl.hide(tab4)
global x
global y
flag=0

var3 = tk.StringVar() # don need this
var3.set('')
tk.Label(tab2, textvariable=var3, font=("Helvetica", 16)).grid(column= 0, row=1150, padx = 70, sticky='w')

# stops rading the encoer after getting to the right location 
def motor1():
    global dic_out
    global flag
    flag=0
    for i in dic_out:
        az=i['az'].degrees
        el=i['alt']. degrees
    # getAZ type is a string
    # az_range type is a numpy.float64
    # az and el is the location the dish is moving to (end)
    # x, y is the current location of the dish (start)
    for i in range(1):
        var3.set('') # reset 
        tk.Label(tab2, textvariable=var3, font=("Helvetica", 16)).grid(column= 0, row=1150, padx = 70, sticky='w')
        distance=round(float(az)-float(x))
        direction_y= round(float(el)-float(y)) # if positive turn up, nagitave turn the dish down
        direction_x= round(float(az)-float(x))
        if(flag==1):
            break
        for i in dic_out: # reset the output as it keeps changing 
            az=i['az'].degrees
            el=i['alt']. degrees
        if (direction_x<-2 ):
            GPIO.output(7, GPIO.LOW) # degree ++
            GPIO.output(8, GPIO.HIGH)
        if (direction_x>2 ):
            GPIO.output(8, GPIO.LOW) #degree--
            GPIO.output(7, GPIO.HIGH)
        if (direction_x <= 2 and direction_x>=-2 ):
            GPIO.output(7, GPIO.LOW) #degree--
            GPIO.output(8, GPIO.LOW)
        if (direction_y<-2 ):
            GPIO.output(3, GPIO.LOW) # degree ++
            GPIO.output(5, GPIO.HIGH)
        if (direction_y>2 ):
            GPIO.output(5, GPIO.LOW) #degree--
            GPIO.output(3, GPIO.HIGH)
        if (direction_y <= 2 and direction_y>=-2 ):
            GPIO.output(5, GPIO.LOW) #degree--
            GPIO.output(3, GPIO.LOW)




def call_motor():
    global flag
    flag=0
    while(True):
        positions()
        submit()
        if (flag==1): #  stoping the auto tracking 
            break
        motor1()

def motorstop1():
    global flag
    flag=1
    GPIO.output(3, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(8, GPIO.LOW)
#     motor_thread.join()





# start_btn
start_btn = tk.Button(tab2, text="START", font=("Helvetica", 12), height = 2, width = 12, command=lambda: call_motor())  # start and make second one for stop
start_btn.grid(column= 0, row=600, sticky='w', padx = 200)
#stop_btn
stop_btn = tk.Button(tab2, text="STOP", font=("Helvetica", 12), height = 2, width = 12, command=lambda: motorstop1())
stop_btn.grid(column= 0, row=650, sticky='w', padx = 200)
 #----Encoder Information-------
def getPosition():
    lineArray = ["",""]
    if __name__ == '__main__':
        try:
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
        except serial.SerialException as e:
            print("No Angle Reading Device Found") 
            sys.exit()
        except:
            ser = serial.Serial('/dev/ttyACM1', 9600, timeout = 1)
        ser.flush()
    
    while True:
        if ser.in_waiting>0:
            lineArray[0] = ser.readline().decode('utf-8').rstrip()
            lineArray[1] = ser.readline().decode('utf-8').rstrip()
            return lineArray
            
#-----------------------------MAIN WINDOW----------------------------------------------------------  
getaz = StringVar()
getel = StringVar()

#dont show - values
def getAz():
    return getPosition()[1]
        
# def getPol():
#     return 15
def getEl():
    return getPosition()[0]




x_temp=0.0
y_temp=0.0
def positions():
    global x
    global y
    global x_temp
    global y_temp
    global flag
    # both are strings 
    x=getAz()
    y=getEl()
    if (x=="" or float(x)<=0.0) :
        x=x_temp # stop the jumps and glitchs in the outputs 
    if (y=="" or float(y)<=0.0):
        y=y_temp        
    if (float(x_temp)!=0.0 and ((float(x)-float(x_temp))<-5 or (float(x)-float(x_temp))>5)):
        x=x_temp # stop the jumps and glitchs in the outputs 
    if (float(y_temp)!=0.0 and ((float(y)-float(y_temp))<-5 or (float(y)-float(y_temp))>5)):
        y=y_temp
    if (float(x)>0.0):
        x_temp=x
    if (float(y)>0.0):
        y_temp=y
    getaz.set(x) # set the output
    getel.set(y)
    ttk.Label(tab2,textvariable = getaz , font=("Helvetica", 20, 'bold')).place(x=  550, y = 250)
    ttk.Label(tab2,textvariable = getel , font=("Helvetica", 20, 'bold')).place(x=  550, y = 300)

    root.update() # allow window to catch up
    time.sleep(0.2) 



 

def mainw():

    if (v.get()==1):
        tabControl.select(tab2)
        tabControl.hide(tab3)
        tabControl.hide(tab4)
    elif (v.get()==2):
        tabControl.select(tab3)
        tabControl.hide(tab2)
        tabControl.hide(tab4)
    elif (v.get()==3):
        tabControl.select(tab4)
        tabControl.hide(tab2)
        tabControl.hide(tab3)
    
 
ttk.Label(tab1, 
          text ="TRACKING MODE", font=("Helvetica", 24, 'bold')).place(x = 300, 
                               y = 100)  
                               
btn_auto = tk.Radiobutton(tab1, text="AUTO", font=("Helvetica", 24, 'bold'),  variable=v, value=1, command= mainw)
btn_auto.place(x= 50, y= 200)    

btn_auto = tk.Radiobutton(tab1, text="MANUAL", font=("Helvetica", 24, 'bold'),  variable=v, value=2, command= mainw)
btn_auto.place(x= 350, y= 200) 

btn_auto = tk.Radiobutton(tab1, text="SETUP", font=("Helvetica", 24, 'bold'),  variable=v, value=3, command= mainw)
btn_auto.place(x= 650, y= 200) 

                 

#-----------------------------AUTO TRACKING----------------------------------------------------------


# the var for the FOV limits 
az_minlimit=tk.StringVar()
az_maxlimit=tk.StringVar()
el_minlimit=tk.StringVar()
el_maxlimit=tk.StringVar()

az_minlimit.set('')
az_maxlimit.set('')
el_minlimit.set('')
el_maxlimit.set('')


var1 = StringVar() # object not found error
var = StringVar() # Ready 

var2 = StringVar() # location output
default_str="UTC Time: \nLocal Time: \nAzimuth: \nAltitude: "
var2.set(default_str)

name_var = tk.StringVar() # name of object 

error2=tk.StringVar() #OBJECT NOT FOUND IN FOV - error

set_lon=tk.StringVar() # set the location of ground station
set_lat=tk.StringVar()

set_lon.set('')
set_lat.set('')

ttk.Label(tab2,text ="OBJECT POSITION", font=("Helvetica", 14, 'bold')).grid(column = 0,row = 200, padx = 40,pady = 30, sticky='w')

# the placment of the object position 
ttk.Label(tab2,textvariable =var2, font=("Helvetica", 14)).grid(column = 0,row = 201, padx = 40,pady = 30, sticky='w')


# label
ttk.Label(tab2,text ="DEFINE OBJECT TO TRACK:", font=("Helvetica", 14, 'bold')).grid(column = 0,row = 0, padx = 30,pady = 30, sticky='w')

# Entry: name of the object 
name_entry  = ttk.Entry(tab2, textvariable=name_var)
name_entry .place(x=300, y=52)

# Button
# used to input the object name 
submit_button = tk.Button(tab2, text="Submit", font=("Helvetica", 12), height = 2, width = 10, command=lambda:call1())
submit_button.grid(column= 0, row=0, sticky='w', padx = 490,pady=42)

def call1():
    while(True):
        positions()
        submit()


global results
def submit():
    global results
    global dic_out
    if (set_lat.get()=='' or set_lon.get()==''): # set to default val
        latitude=38.827380 # position of the dish in gmu
        longitude=-77.305472
    else:
        latitude=float(set_lat.get())
        longitude=float(set_lon.get())
        
    var1.set('')#reset object not found is not
    var2.set(default_str) # empty results
    var.set('NOT READY')# results not ready yet
    error2.set('')# reset the error
    
    tk.Label(tab2, textvariable=error2, font=("Helvetica", 16)).grid(column= 0, row=1150, padx = 60, sticky='w')
    tk.Label(tab2,textvariable=var1, font=("Helvetica", 16)).grid(column= 0, row=1100, padx = 60, sticky='w') #reset the errors
    tk.Label(tab2, textvariable=var, font=("Helvetica", 16)).grid(column= 0, row=600, padx = 60, sticky='w')
    #use strip to ignore all space in string, .lower() to ignore case sensitivty
    output1=name_var.get().lower().strip()
#     while(True):
    if (time_input.get()==''): # no time zone input
        time_offset=0.0
    else:
        time_offset=float(time_input.get())
    if output1 in ["sun",'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'neptune', 'uranus', "pluto", "moon"]:
        dic_out=get_planet_track(planet=output1,latitude=latitude, longitude=longitude, points=1, angle=-180,time_offset=time_offset)
        var.set('READY') 
        Fov_limit(dic_out) #call the function to check on the limits
        str_out=print_views(dic_out)
        results = dic_out
        var2.set(str_out) # the location of the object            ttk.Label(tab2,textvariable= var2, font=("Helvetica", 14)).grid(column = 0,row = 201, padx = 40,pady = 30, sticky='w')
        tk.Label(tab2, textvariable=var, font=("Helvetica", 16)).grid(column= 0, row=600, padx = 60, sticky='w')
        root.update() # allow window to catch up
        time.sleep(0.1)
        

    elif output1.isdigit(): 
        #call the link with the sat list 
        stations_url ='http://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
        satellites = load.tle_file(stations_url)
        # values by id 
        by_number = {sat.model.satnum: sat for sat in satellites}
        
        if (int(output1) not in by_number ):# checking if the id is available in the list with 7k values 
            var1.set("OBJECT/DATA NOT FOUND")
        else:
            sat=by_number[int(output1)]
            dic_out=get_sat_track(time_offset=time_offset,sat=sat,norad_id=int(output1), latitude=latitude, longitude=longitude, points=1, angle=-180)
            var.set('READY')
            Fov_limit(dic_out) #call the function to check on the limits
            str_out=print_views(dic_out)# get the output as a string to set the lable 
            var2.set(str_out) # set var2 for the label
            ttk.Label(tab2,textvariable=var2, font=("Helvetica", 14)).grid(column = 0,row = 201, padx = 40,pady = 30, sticky='w')
            tk.Label(tab2, textvariable=var, font=("Helvetica", 16)).grid(column= 0, row=600, padx = 60, sticky='w') # for ready label
            root.update() # allow window to catch up

    elif output1=='voyager1':
        dic_out=get_voyager_track(time_offset=time_offset,latitude=latitude, longitude=-77.305472, points=1, angle=-180)
        var.set('READY') 
        Fov_limit(dic_out)
        str_out=print_views(dic_out) 
        var2.set(str_out)
        
        ttk.Label(tab2,textvariable =var2, font=("Helvetica", 14)).grid(column = 0,row = 201, padx = 40,pady = 30, sticky='w') # location output
        tk.Label(tab2, textvariable=var, font=("Helvetica", 16)).grid(column= 0, row=600, padx = 60, sticky='w')# ready
        root.update() # allow window to catch up




    else:
        var1.set("OBJECT/DATA NOT FOUND")
        tk.Label(tab2,textvariable=var1, font=("Helvetica", 16)).grid(column= 0, row=1100, padx = 60, sticky='w')
        #break
        #submit_thread.join()



def print_views(views):
    for i in views: # change the value to a string to output
        return ("UTC Time: %s\nLocal Time: %s\nAzimuth: %f\nAltitude: %f\n"%(str(i['UTC Time'])[:19],str(i["Local Time"])[:19], i['az'].degrees, i['alt'].degrees))

#---------------------------FOV limits----------------------
        
def Fov_limit(views):
    # if no limts are set, set the limits as the default values of -180 to 180 
    if (az_minlimit.get()=='' or az_maxlimit.get()=='' or el_minlimit.get() ==''or el_maxlimit.get()=='') :
        az_min=75
        az_max= 175
        
        el_min=15
        el_max=100
    else:
        az_min=float(az_minlimit.get()) # get the limit values 
        az_max=float(az_maxlimit.get())
        el_min=float(el_minlimit.get()) 
        el_max=float(el_maxlimit.get())

    for i in views:
        az=float(i['az'].degrees) # get the angle from the dictionary
        alt=float(i['alt'].degrees)
    if (az>az_max or az<az_min or alt>el_max or alt<el_min): # check if location is in the limit 
        error2.set('OBJECT NOT FOUND IN FOV')
        var.set('NOT READY')
        tk.Label(tab2, textvariable=error2, font=("Helvetica", 16)).grid(column= 0, row=1150, padx = 60, sticky='w')
        
#------------------------------end of FOV limit -------------------------------
ttk.Label(tab2,
          text ="DISH CURRENT POSITION", font=("Helvetica", 14, 'bold')).grid(column = 0,
                                    row = 200, 
                                    padx = 450,
                                    pady = 10, sticky='w')
ttk.Label(tab2,
          text ="Azimuth", font=("Helvetica", 14)).place(x=  450, y = 250)
ttk.Label(tab2,
          text ="Altitude", font=("Helvetica", 14)).place(x=  450, y = 300)

ttk.Label(tab2,text ="ERROR/WARNINGS", font=("Helvetica", 16, 'bold')).grid(column = 0,row = 1000, padx = 50,pady = 10,  sticky='w')

#-----------------------------MANUAL OPERATION---------------------------------------------------------
ttk.Label(tab3,
          text ="DISH CURRENT POSITION", font=("Helvetica", 16, 'bold')).place(x=  40, y = 82)

ttk.Label(tab3,
          text ="Azimuth", font=("Helvetica", 14)).place(x=  40, y = 130)
ttk.Label(tab3,
          text ="Altitude", font=("Helvetica", 14)).place(x=  40, y = 180)
 
#print positions
get_button = tk.Button(tab3, text="Get Dish Current Position", font=("Helvetica", 12), height = 2, width = 20, command=lambda: call2())
get_button .grid(column= 0, row=0, sticky='w', padx = 360,pady=62)
def call2(): # used to call position in a loop
    while (True):
        positions()
        limit()
ttk.Label(tab3,textvariable = getaz , font=("Helvetica", 20, 'bold')).place(x=  170, y = 130)
ttk.Label(tab3,textvariable = getel , font=("Helvetica", 20, 'bold')).place(x=  170, y = 175)

def limit():
    var3.set('')
    if (round(float(y))>100):
        var3.set('POSITION LIMIT REACHED') # dont allow the dish to move down if it is at the min angle
        #tk.Label(tab3,  textvariable=var3, font=("Helvetica", 16)).place(x= 100, y=400)
        GPIO.output(3, GPIO.LOW)
    if (round(float(y))<15):
        var3.set('POSITION LIMIT REACHED') 
        #tk.Label(tab3,  textvariable=var3, font=("Helvetica", 16)).place(x= 100, y=400)
        GPIO.output(5, GPIO.LOW)
    if (round(float(x))>175):
        var3.set('POSITION LIMIT REACHED') 
        #tk.Label(tab3,  textvariable=var3, font=("Helvetica", 16)).place(x= 100, y=400)
        GPIO.output(7, GPIO.LOW)
    if (round(float(x))<75):
        var3.set('POSITION LIMIT REACHED') 
        GPIO.output(8, GPIO.LOW)

    tk.Label(tab3,  textvariable=var3, font=("Helvetica", 16)).place(x= 100, y=400)
        
    
def moving_up(): # manual moving for the dish 
    GPIO.output(5, GPIO.LOW)
    GPIO.output(3, GPIO.HIGH)
def moving_down():
    GPIO.output(3, GPIO.LOW)
    GPIO.output(5, GPIO.HIGH)
    
def moving_right():
    GPIO.output(7, GPIO.LOW)
    GPIO.output(8, GPIO.HIGH)
    
def moving_left():
    GPIO.output(8, GPIO.LOW)
    GPIO.output(7, GPIO.HIGH)
    
def stop_moving():
    GPIO.output(3, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(8, GPIO.LOW)
    
m_stop = tk.Button(tab3, text="STOP", font=("Helvetica", 12), height = 2, width = 10, command=lambda: stop_moving())
m_stop.place(x= 420, y=280)
ttk.Label(tab3,text ="ACTION", font=("Helvetica", 18, 'bold')).place(x=  620, y = 80)
btn_UP = tk.Button(tab3, text="UP", font=("Helvetica", 12), height = 2, width = 10, command=lambda: moving_up())
btn_UP.place(x= 620, y=130)
btn_DOWN = tk.Button(tab3, text="DOWN", font=("Helvetica", 12), height = 2, width = 10, command=lambda: moving_down())
btn_DOWN.place(x= 620, y=230)
btn_EAST = tk.Button(tab3, text="EAST", font=("Helvetica", 12), height = 2, width = 10, command=lambda: moving_right())
btn_EAST.place(x= 520, y=180)
btn_WEST = tk.Button(tab3, text="WEST", font=("Helvetica", 12), height = 2, width = 10, command=lambda: moving_left())
btn_WEST.place(x= 720, y=180)



ttk.Label(tab3,text ="WARNINGS", font=("Helvetica", 16, 'bold')).place(x = 100,y = 350)
                                    

#-----------------------------SETUP----------------------------------------------------------

ttk.Label(tab4,text ="EL FOV LIMIT", font=("Helvetica", 14)).place(x = 50,y = 209)
ttk.Label(tab4,text ="Minimum", font=("Helvetica", 14)).place(x = 250,y = 130)
ttk.Label(tab4,text ="AZ FOV LIMIT", font=("Helvetica", 14)).place(x = 50,y = 159)
ttk.Label(tab4,text ="Maximum", font=("Helvetica", 14)).place(x = 450,y = 130)

entry_AZ_fov_min = ttk.Entry(tab4,textvariable=az_minlimit)
entry_AZ_fov_min.place(x=250, y=159)

entry_EL_fov_min = ttk.Entry(tab4,textvariable=el_minlimit)
entry_EL_fov_min.place(x=250, y=209)


entry_AZ_fov_max = ttk.Entry(tab4, textvariable=az_maxlimit)
entry_AZ_fov_max.place(x=450, y=159)

entry_EL_fov_max = ttk.Entry(tab4,textvariable=el_maxlimit)
entry_EL_fov_max.place(x=450, y=209)      


ttk.Label(tab4,text ="UTC TIME OFFSET", font=("Helvetica", 14)).place(x=50,y = 289)

time_input=tk.StringVar()
time_input.set('')
entry_time_zone = ttk.Entry(tab4,textvariable=time_input)
# Place it within the window.
entry_time_zone.place(x=50, y=320)

ttk.Label(tab4,text ="GROUND STATION LOCATION", font=("Helvetica", 14)).place(x = 400,y = 289)
ttk.Label(tab4,text ="LATITUDE", font=("Helvetica", 14)).place(x = 280,y = 320)       

ttk.Label(tab4,text ="LONGITUDE", font=("Hvetica", 14)).place(x = 580,y = 320)


entry_latitude = ttk.Entry(tab4,textvariable=set_lat)
# Place it within the window.
entry_latitude.place(x=380, y=320)

entry_longitude= ttk.Entry(tab4,textvariable=set_lon)
# Place it within the window.
entry_longitude.place(x=700, y= 320)

root.mainloop()  