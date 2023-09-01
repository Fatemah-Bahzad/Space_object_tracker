from skyfield.api import load, wgs84, EarthSatellite, utc
from datetime import datetime, timezone, timedelta
from skyfield.constants import AU_KM
from skyfield.vectorlib import VectorFunction
from spktype01 import SPKType01
from spktype21 import SPKType21


import datetime
import pytz


class TrackPlanet:
    def __init__(self, lat=0.0, lon=0.0, planet=None):
        self.ts = load.timescale()
        self.eph = load('de421.bsp') # data needed to get the location for the planets 
        self.earth =  self.eph['earth']
        self.planet = None
        if planet is not None:
            if (planet=="jupiter"): 
                planet="JUPITER BARYCENTER"# name of the object in the data file
            elif (planet=="pluto"): 
                planet="PLUTO BARYCENTER"
            elif (planet=="neptune"): 
                planet="NEPTUNE BARYCENTER"
            elif (planet=="uranus"): 
                planet="URANUS BARYCENTER"
            elif (planet=="saturn"): 
                planet="SATURN BARYCENTER"
            self.planet = self.eph[planet]
        self.lon = lon
        self.lat = lat
        self.loc = self.earth + wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)
        self.sat = None

    def get_view(self, points=100,time_offset=0.0):
        if (time_offset==0.0): #default value for the timezone (est)
            local_time=datetime.datetime.now()
        else:
            tzinfo = timezone(timedelta(hours=time_offset))
            local_time=datetime.datetime.now(tzinfo)
        
        #local_time=datetime.datetime.now() ## if need to change the timezone change this 
        ts = load.timescale()
        now =datetime.datetime.now(pytz.utc)  
        t=self.ts.from_datetime(now)
        difference = self.planet - self.loc
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()
        return {'UTC Time': now, "Local Time":local_time, 'alt': alt, 'az': az, 'distance': distance}

        
        


class TrackSatellite:
    def __init__(self, lat=0.0, lon=0.0, tle=None, url=False, id1=None,sat=None ):
        self.lon = lon
        self.lat = lat
        self.loc = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)
        self.ts = load.timescale()
        self.sat=sat# this need to be moved to the gui and used as in input


    def get_view(self, points=100,time_offset=0.0):
        if (time_offset==0.0): #default value for the timezone (est)
            local_time=datetime.datetime.now()
        else:
            tzinfo = timezone(timedelta(hours=time_offset))
            local_time=datetime.datetime.now(tzinfo)
        #local_time=datetime.datetime.now()
        #print(local_time)
        ts = load.timescale()
        now =datetime.datetime.now(pytz.utc)
        t=self.ts.from_datetime(now)
        difference = self.sat - self.loc
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()
        return {'Satellite ID':id,'UTC Time': now, "Local Time":local_time, 'alt': alt, 'az': az, 'distance': distance}


class EphemeralClass(VectorFunction):
    def __init__(self, kernel, target, type_obj):
        self.kernel = kernel
        self.target = target
        if self.target==-202:
            self.center=4
        elif type_obj == "type01":
            self.center = 10
        else:
            self.center = 0

    def _at(self, t):
        if self.center == 10 or self.center == 4:
            r, v = self.kernel.compute_type01(self.center, self.target, t.whole, t.tdb_fraction)
        else:
            r, v = self.kernel.compute_type21(0, self.target, t.whole, t.tdb_fraction)

        return r / AU_KM, v / AU_KM, None, None


class TrackBodyT21:
    def __init__(self, lat=0.0, lon=0.0):
        self.lat = lat
        self.lon = lon
        self.ts = load.timescale()
        self.eph = load('de421.bsp')
        self.earth = self.eph['earth']
        kernel = SPKType21.open('2065803.bsp')
        #print(kernel)
        self.body_eph = EphemeralClass(kernel=kernel, target=2065803, type_obj="type21")
        #print(self.body_eph)
        self.loc = self.earth + wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)
        self.sat = None

    def get_view(self, time_start, time_stop=None, points=100):
        ##########
        local_time=datetime.datetime.now()
        print(local_time)
        ts = load.timescale()
        now =datetime.datetime.now(pytz.utc)
        t=self.ts.from_datetime(now)
        ########
        t1 = self.ts.from_datetime(datetime=time_start)
        difference = self.body_eph - self.loc
        topocentric = difference.at(t=t1)

        alt, az, distance = topocentric.altaz()
        #return {'time': t1, 'alt': alt, 'az': az, 'distance': distance}
        return {'i':self.sat,'UTC Time': now, "Local Time":local_time, 'alt': alt, 'az': az, 'distance': distance}
    
#command line to use this class
#python track.py track_voyager --lat 38.827480 --lon -77.305472 --initial_time "2023/01/05-00:00:00"  --points 1 --angle -100
class TrackBodyT01: #line being printed and isk where from 
    def __init__(self, lat=0.0, lon=0.0):
        #lat north s
        #lon e w 
        self.lat = lat
        self.lon = lon
        self.ts = load.timescale()
        self.eph = load('de421.bsp')
        self.earth = self.eph['earth']
        self.sun = self.eph['sun']
        kernel = SPKType01.open('Voyager_1.a54206u_V0.2_merged.bsp') 
        self.body_eph = EphemeralClass(kernel=kernel, target=-31, type_obj="type01") #not sure how to change this to fit 

        self.sat = None
        self.loc = self.earth + wgs84.latlon(latitude_degrees=self.lat, longitude_degrees=self.lon)



    def get_view(self, points=100,time_offset=0.0):
        if (time_offset==0.0): #default value for the timezone (est)
            local_time=datetime.datetime.now()
        else:
            tzinfo = timezone(timedelta(hours=time_offset))
            local_time=datetime.datetime.now(tzinfo)
        #local_time=datetime.datetime.now()
        ts = load.timescale()
        now =datetime.datetime.now(pytz.utc)
        t=self.ts.from_datetime(now)
        difference = self.body_eph.at(t) - self.loc.at(t)
        topocentric = difference
        alt, az, distance = topocentric.altaz()
        return {'Voyager_1':self.sat,'UTC Time': now, "Local Time":local_time, 'alt': alt, 'az': az, 'distance': distance}

#this works for voyager 1
# class TrackBodyT01:
#     def __init__(self, lat=0.0, lon=0.0):
#         self.lat = lat
#         self.lon = lon
#         self.ts = load.timescale()
#         self.eph = load('data/de421.bsp')
#         self.earth = self.eph['earth']
#         self.sun = self.eph['sun']
#         kernel = SPKType01.open('data/Voyager_1.a54206u_V0.2_merged.bsp')
#         print(kernel)
#         self.body_eph = EphemeralClass(kernel=kernel, target=-31, type_obj="type01")
#         print("()()()()")
#         print(self.body_eph)
#         self.sat = None
#         self.loc = self.earth + wgs84.latlon(latitude_degrees=self.lat, longitude_degrees=self.lon)
# 
#     def get_view(self, time_start, time_stop=None, points=100):
#         local_time=datetime.datetime.now() # just use this as t1 but have to change more shit 
#         ts = load.timescale()
#         now =datetime.datetime.now(pytz.utc)
#         t=self.ts.from_datetime(now)
#         t1 = self.ts.from_datetime(datetime=time_start)
# #         if time_stop is not None:
# #             t2 = self.ts.from_datetime(datetime=time_stop)
# #             ret_list = []
# #             times = self.ts.linspace(t1, t2, points)
# #             for t in times:
# #                 topocentric = self.body_eph.at(t) - self.loc.at(t)
# #                 alt, az, distance = topocentric.altaz()
# #                 ret_list.append({'time': t, 'alt': alt, 'az': az, 'distance': distance})
# #             return ret_list
# #         else:
#         difference = self.body_eph.at(t) - self.loc.at(t)
#         topocentric = difference
# 
#         alt, az, distance = topocentric.altaz()
#         #return {'time': t1, 'alt': alt, 'az': az, 'distance': distance}
#         return {'Voyager_1':self.sat,'UTC Time': now, "Local Time":local_time, 'alt': alt, 'az': az, 'distance': distance}
