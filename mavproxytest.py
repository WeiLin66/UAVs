from dronekit import connect

vehicle = dronekit.connect('/dev/ttyACM0')  # ... and other connection options
udp_conn = MAVConnection('udpin:221.120.82.20:14667', source_system=1)
vehicle._handler.pipe(udp_conn)
udp_conn.master.mav.srcComponent = 1  # needed to make QGroundControl work!
udp_conn.start()
