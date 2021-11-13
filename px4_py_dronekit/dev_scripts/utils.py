import socket
import time
from dronekit import connect


def millis():
    return int(round(time.time() * 1000))  

def armed(vehicle):
    if vehicle.armed:
        return 'armed'
    else:
        return 'disarmed'


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
        'DroneId': '06cdcf5a-0e98-4599-a638-6b17d288e948',
        'Latitude': vehicle.location.global_relative_frame.lat,
        'Longtitude': vehicle.location.global_relative_frame.lon,
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
        'GPSTime': time.strftime('%H:%M:%S',time.localtime(time.time())),
        'GPSStatus': vehicle.gps_0.satellites_visible,
        'BatteryStatus': vehicle.battery.level,
        'CurrentWaypointNumber': 1,
        'DistanceToWaypoint': 25.5,
        'CurrentFlightMode': vehicle.mode.name,
        'DataTime': str(millis()),
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