import socket
import time
from dronekit import connect, LocationGlobalRelative, LocationGlobal
from datetime import datetime

def dronetime(vehicle):
    time = vehicle.gps_time.gps_time
    converted = "% s " % time
    converted1 = int(converted[0:10])
    dronetime = datetime.fromtimestamp(converted1)
    dronetime = dronetime.strftime("%X")
    return(dronetime)

def armed(vehicle):
    if vehicle.armed:
        return 'armed'
    else:
        return 'disarmed'

def mode(vehicle):
    if vehicle.mode.name == 'STABILIZE':
        return '0'
    elif vehicle.mode.name == 'AUTO':
        return '3'
    elif vehicle.mode.name == 'GUIDED':
        return '4'
    elif vehicle.mode.name == 'LOITER':
        return '5'
    elif vehicle.mode.name == 'RTL':
        return '6'
    elif vehicle.mode.name == 'LAND':
        return '9'
    else:
        return vehicle.mode.name

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

def download_mission():
    
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

'''
'TeleQuality': 0,
'GPSTime': '12:45:01',
'GPSStatus': 1,
'BatteryStatus': 0.0,
'CurrentWaypointNumber': 1,
'DistanceToWaypoint': 25.5,
'CurrentFlightMode': '0',
這些資料不知道是不是因為硬體設置不完全，所以無法撈到，暫時是寫死的
這部份要請虎尾幫忙看是哪邊出問題
'''


def drone_message_dumper(vehicle):
    
    test_msg = {
        'DroneSID': '724fc1fa-e3d1-4ec6-b98a-a7aec3de6d23',
        'Latitude': vehicle.location.global_relative_frame.lat,
        'Longitude': vehicle.location.global_relative_frame.lon,
        'Altitude': vehicle.location.global_relative_frame.alt,
        'D1': vehicle.velocity[0],
        'D2': vehicle.velocity[1],
        'D3': vehicle.velocity[2],
        'D4': vehicle.attitude.pitch,
        'D5': vehicle.attitude.yaw,
        'D6': vehicle.attitude.roll,
        'V': vehicle.battery.voltage,
        'A': vehicle.battery.current,
        'AirSpeed': vehicle.airspeed,
        'GroundSpeed': vehicle.groundspeed,
        'TeleQuality': 0,
        'GPSTime': dronetime(vehicle),
        'GPSStatus': vehicle.gps_0.satellites_visible,
        'BatteryStatus': vehicle.battery.level,
        'CurrentWaypointNumber': vehicle.commands.next,
        'DistanceToWaypoint':25,
        'CurrentFlightMode': mode(vehicle),
        'DataTime': vehicle.gps_time.date_time,
        'Motor': armed(vehicle),
    }

    return test_msg

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)
    # logs if send success

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)
    # handle exception
