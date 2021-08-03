import time
def millis():
    return int(round(time.time() * 1000))  

def armed(vehicle):
    if vehicle.armed:
        return 'armed'
    else:
        'disarmed'


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


def drone_message_dumper():
    
    test_msg = {
        'DroneId': '06cdcf5a-0e98-4599-a638-6b17d288e948',
        'Latitude': 0,
        'Longtitude': 0,
        'Altitude': 0,
        'D1': 0,
        'D2': 0,
        'D3': 0,
        'D4': 0,
        'D5': 0,
        'D6': 0,
        'V': 0,
        'A': 0,
        'AirSpeed': 0,
        'GroundSpeed': 0,
        'TeleQuality': 0,
        'GPSTime': '12:45:01',
        'GPSStatus': 1,
        'BatteryStatus': 0.0,
        'CurrentWaypointNumber': 1,
        'DistanceToWaypoint': 25.5,
        'CurrentFlightMode': '0',
        'DataTime': 0,
        'Motor': 0,
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