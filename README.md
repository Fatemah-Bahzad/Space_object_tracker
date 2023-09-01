# Space_object_tracker

the code is a part of a bigger project to apply a navigation system to a dish.
The software takes in an input like a name of a planet, ID number of a satellite, and gives back the location of the object. The base station location and time zone can be changed through the GUI
 
The overall code is between four files:
• client.py
• track.py
• GUI.py


For the program to run on any device, there are a number of libraries which are expected to be installed which include:
• pytz
• datetime • spktype01 • spktype21 • skyfield

command lines for Linux:
• pip install skyfield
• python3 −m pip install skyfield spktype01 spktype21
• pip install pytz
• pip install datetime

command lines windows:
• pip install skyfield
• python −m pip install skyfield spktype01 spktype21
• pip install pytz
• pip install datetime

GUI.py:
• using GPIO pins (3,5,7,8) to control the motors

• motor1(): takes in the values from software and encoders to move the motors accordingly as

needed

• call_motor(): used to calls the needed functions when (start) is pressed on the auto tab

• motorstop1(): when (stop) is pressed on the auto tab, stop the motors

• getPosition(): Serial reading of the encoder information

• getAz(), getEl(): get the values

• positions(): clear out any glitch from the encoder readings and setting the values to display on
the GUI

• mainw(): main GUI page set up

• call1(): call the needed functions when (submit) is pressed on the GUI.

• Submit(): takes in the input from the GUI after pressing on (submit) on the auto tab.

o LonandLathaveadefaultvalueofGMUlocation,andtheycanbechangedinthe set-up tab of the GUI

o Tolowertheupdaterateofthetargetedobjectlocation.Becausethedatafilewill have approximately 7000 satellites information and the program will have to load it

each time and look for the targeted object every time the location is being updated (approximately 1 second) it will cause a delay in the display. I decided to load the file 

(http://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMA T=tle)for the satellites and save the information locally to use it as an input for the TrackSatellite class in client.py.

o Timeoff-sethasadefaultvalueofzeroandcanbechangedintheset-uptabofthe GUI

o dic_outisadictionarywiththelocationofthetargetedobject.

§ {'UTC Time': now, "Local Time":local_time, 'alt': alt, 'az': az, 'distance':
distance}

§ {'Satellite ID':id,'UTC Time': now, "Local Time":local_time, 'alt': alt, 'az': az,
'distance': distance}

§ {'Voyager_1':self.sat,'UTC Time': now, "Local Time":local_time, 'alt': alt,
'az': az, 'distance': distance}

• Fov_limit(views): takes in dic_out as an input to check the FOV limits. The limits have a
default value of 75-175 for the az and 15-100 for el. Their values can be changed on the set-
up tab.

• call2(): calls the needed functions when (get dish current position) is pressed on the manual
tab

• Limit(): checks the FOV limits for the manual mode
• moving_up(),moving_down(),moving_right(),moving_left(): moves the motors depending on
the buttons pressed on the manual tab
• stop_moving(): stop moving the motors when (stop) is pressed on the manual tab
track.py:
§ makes it easier to call functions from client.py and connecting it to the GUI client.py:
• TrackPlanet class:
o Loadfilecalled“de421.bsp”
o Usewgs84.latlon()tocalculatethelocationofthegroundstation
o Ifatimeoffsetisgivenapplyitusingtimezone(timedelta(hours=time_offset)) o Ifnotimeoffsetisgiven,thedefaulttimezoneisEST.Implementitusing
datetime.datetime.now()
o ThelocaltimewillbedisplayedalongwithUTCtimezonebecauseSkyfielduses
UTC to retrieve the information and calculate the position. To make it easier on the user any local time they pick through the setup screen on the GUI will be display alongside UTC time.
• TrackSatellite class:
o TakesthedataasaninputfromGUI.py
o WillfollowthesamestepsasTrackPlanetclass
adding more object to track like a spacecraft might require adding more classes depending on the file the data is being retrieve from.

Reference:
“NORAD GP Element Setscurrent Data.” CelesTrak, https://celestrak.org/NORAD/elements/. “Naif.” NASA, NASA, https://naif.jpl.nasa.gov/naif/.
“Skyfield.” Skyfield - Documentation, https://rhodesmill.org/skyfield/.
