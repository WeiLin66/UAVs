#!/usr/bin/env python3
import socket
import time
from dronekit import connect
from custom_drone import MyVehicle
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import utils

#time.sleep(10)
try:
    vehicle = connect('10.27.0.13:14551', wait_ready=True,
                      baud=115200, vehicle_class=MyVehicle)

# Bad TCP connection
except socket.error:
    print('No server exists!')

# Bad TTY connection
except exceptions.OSError as e:
    print('No serial exists!')

# API Error
except dronekit.APIException:
    print('Timeout!')

# Other error
except:
    print('Some other error!')



for _ in range(1):
    print(vehicle.gps_time)
    #"Latitude, Longtitude, Altitude"
    print(vehicle.location.global_relative_frame)
    #D4, D5, D6
    print(vehicle.attitude)
    #D1, D2, D3
    print(vehicle.velocity)
    #V, A, BatteryStatus
    print(vehicle.battery)
    #AirSpeed
    print(vehicle.airspeed)
    #GroundSpeed
    print(vehicle.groundspeed)
    #CurrentFlightMode
    print(vehicle.mode.name)
    #GPSStatus
    print(vehicle.gps_0)
    #Motor (report armed/disarmed)
    print(vehicle.armed)
    #waypointnumber
    print("waypoint %s " % vehicle.commands.next)
    print(vehicle.capabilities.flight_termination)
    #print(dronetime(vehicle))
    print("="*100)
    time.sleep(0.01)

for _ in range(5):
    print(utils.drone_message_dumper(vehicle))
    time.sleep(2)
producer = KafkaProducer(bootstrap_servers='10.1.181.230:9092',
                         value_serializer=lambda m: json.dumps(m).encode('ascii'),
                         client_id = 'DroneStatus')


# 試傳10次json格式的資料回雲端

while(1):
    print('send message to kafka!')
    producer.send('DroneStatus', utils.drone_message_dumper(vehicle)).add_errback(utils.on_send_error)
    time.sleep(1.0)

producer.flush()

vehicle.close()
