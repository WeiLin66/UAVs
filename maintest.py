# -*- coding: utf-8 -*-

from __future__ import print_function


import time
from dronekit import connect, LocationGlobalRelative, LocationGlobal, VehicleMode
import math

vehicle = connect('127.0.0.1:14551', wait_ready=True)

# Download the vehicle waypoints (commands). Wait until download is complete.


cmds = vehicle.commands
cmds.download()
cmds.wait_ready()
 

def get_location_metres(original_location, dNorth, dEast):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
    specified `original_location`. The returned Location has the same `alt` value
    as `original_location`.

    The function is useful when you want to move the vehicle around specifying locations relative to 
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius=6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt)


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5


def distance_to_current_waypoint():
    """
    Gets distance in metres to the current waypoint. 
    It returns None for the first waypoint (Home location).
    """
    global nextwaypoint
    nextwaypoint = vehicle.commands.next
    
    if nextwaypoint==0:
        return 0
    ##陣列數量與任務規劃的航點
    missionitem=vehicle.commands[nextwaypoint-1] #commands are zero indexed
    lat = missionitem.x
    lon = missionitem.y
    alt = missionitem.z
    targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    return distancetopoint
"""
def download_mission():
    
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
"""
for _ in range(30):
     #print(vehicle.gps_time)
     "Latitude, Longtitude, Altitude"
     print(vehicle.location.global_relative_frame)
     #D4, D5, D6
     print("HIGHT",vehicle.attitude)
     #D1, D2, D3
     print(vehicle.velocity)
     #V, A, BatteryStatus
     print("Battery: %s" % vehicle.battery)
     #AirSpeed
     print(vehicle.airspeed)
     #GroundSpeed
     print(vehicle.groundspeed)
     #CurrentFlightMode
     print(vehicle.mode)
     #GPSStatus
     print(vehicle.gps_0)
     #Motor (report armed/disarmed)
     print(vehicle.armed)
     #waypointnumber
     print("waypoint %s " % vehicle.commands.next)
     #distance
     print('Distance to waypoint %s' %  distance_to_current_waypoint())
     print("="*100)
     time.sleep(1)
     """
     if vehicle.mode == "AUTO" and nextwaypoint == False :
         print("mission ended")
         break;
         """
vehicle.mode= VehicleMode("RTL")

vehicle.close()