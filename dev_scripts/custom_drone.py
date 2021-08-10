from dronekit import connect, Vehicle

class GPSTime:

    def __init__(self, gps_time=None, date_time=None):
        self.gps_time = gps_time
        self.date_time = date_time
    
    def __str__(self):
        return f"gps_time: {self.gps_time}, date_time: {self.date_time}"

class MyVehicle(Vehicle):
    def __init__(self, *args):
        super(MyVehicle, self).__init__(*args)

        # Create an Vehicle.raw_imu object with initial values set to None.
        self._datelogger = GPSTime()

        # Create a message listener using the decorator.
        @self.on_message('SYSTEM_TIME')
        def listener(self, name, message):
            #print(message)
            self._datelogger.gps_time = message.time_unix_usec
            self._datelogger.date_time = message.time_unix_usec
            self.notify_attribute_listeners('gps_time', self._datelogger)

    @property
    def gps_time(self):
        return self._datelogger