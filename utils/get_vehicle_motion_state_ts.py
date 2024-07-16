import bisect

class GetVehicleMotionStateTS: 
    def __init__(self,*args, **kwargs):
        self.vehicle_local_position = kwargs.get('vehicle_local_position')
        self.vehicle_land_detected = kwargs.get('vehicle_land_detected')
        self.manual_control_setpoint = kwargs.get('manual_control_setpoint')
        self.log_thresholds = kwargs.get('log_thresholds')

    def get_hover_ts(self): 
        #TODO: see if you can come up with a better solution
        # issue i have here is, every time it is not landed, and veocity is not 0, I get a ts
        # but this needs to be a more timewindow bases approach, where I need sections of ts where  
        # it is hovering for atleast 5 sec 
        hover_ts_arr = []
        zero_vel_ts = []
        notlanded_ts = []
        
        vehicle_not_landed_ts=[]
        vehicle_not_landed_indexes=[]
        for index, value in enumerate(self.vehicle_land_detected['timestamp']): 
            if self.vehicle_land_detected['landed'][index] == 0: 
                vehicle_not_landed_ts.append(value)
        tmp_vehicle_ts = []
        for i in self.vehicle_local_position['timestamp']: 
            tmp_vehicle_ts.append(i/1000000)
        vehicle_not_landed_indexes = self.find_closest_timestamps_indexes(vehicle_not_landed_ts, tmp_vehicle_ts)
        # filtering the sections with 0 velocities 
        for index in vehicle_not_landed_indexes:
            if (self.log_thresholds.get_threshold("hover_flight_vel")[0] < self.vehicle_local_position['vx'][index] < self.log_thresholds.get_threshold("hover_flight_vel")[1] and 
                self.log_thresholds.get_threshold("hover_flight_vel")[0] < self.vehicle_local_position['vy'][index] < self.log_thresholds.get_threshold("hover_flight_vel")[1] and 
                self.log_thresholds.get_threshold("hover_flight_vel")[0] < self.vehicle_local_position['vz'][index] < self.log_thresholds.get_threshold("hover_flight_vel")[1]):
                
                ts_in_sec = self.vehicle_local_position['timestamp'][index]/1_000_000.0
                rounded_ts =  round(ts_in_sec, 1)
                zero_vel_ts.append(rounded_ts)

        for index, ts in enumerate(self.vehicle_land_detected["timestamp"]):
            if self.vehicle_land_detected["landed"][index] == 0:
                ts_in_sec = ts/1_000_000.0
                rounded_ts = round(ts_in_sec, 1)
                notlanded_ts.append(rounded_ts)

        notlanded_ts_set = set(notlanded_ts)  # Convert list to set for faster lookup
        hover_ts_arr = [ts for ts in zero_vel_ts if ts in notlanded_ts_set]

        return hover_ts_arr
    
    def get_fast_forward_flight_ts(self):
        fastforward_ts_arr = [0]
        # filtering the sections with 0 velocities 
        for index in range(len(self.vehicle_local_position['vx'])):
            if (self.vehicle_local_position['vx'][index] is not None):
                if (((self.vehicle_local_position['vx'][index] > self.log_thresholds.get_threshold("fastfwd_flight_vel")[1]) or (self.vehicle_local_position['vx'][index] < self.log_thresholds.get_threshold("fastfwd_flight_vel")[1])) or
                    ((self.vehicle_local_position['vy'][index] > self.log_thresholds.get_threshold("fastfwd_flight_vel")[1]) or (self.vehicle_local_position['vx'][index] < self.log_thresholds.get_threshold("fastfwd_flight_vel")[1]))
                ): 
                    ts_in_sec = self.vehicle_local_position['timestamp'][index]/1_000_000.0
                    rounded_ts =  round(ts_in_sec, 1)
                    fastforward_ts_arr.append(rounded_ts)

        return fastforward_ts_arr



    def find_closest_timestamps_indexes(self, reference_timestamps, target_timestamps):
        """
        Finds the indexes of the closest timestamps in 'reference_timestamps' for each timestamp in 'target_timestamps'.

        Args:
            reference_timestamps (list): List of timestamps to search within (in seconds).
            target_timestamps (list): List of target timestamps to find the closest matches for (in seconds).

        Returns:
            list: List of indexes of the closest timestamps in 'reference_timestamps' for each timestamp in 'target_timestamps'.
        """
        reference_timestamps_in_sec = [ts / 1000000 for ts in reference_timestamps]
        closest_timestamps_index = []
        
        for target in target_timestamps:
            pos = bisect.bisect_left(reference_timestamps_in_sec, target)
            
            if pos == 0:
                closest_timestamps_index.append(0)
            elif pos == len(reference_timestamps_in_sec):
                closest_timestamps_index.append(len(reference_timestamps_in_sec) - 1)
            else:
                before = reference_timestamps_in_sec[pos - 1]
                after = reference_timestamps_in_sec[pos]
                if after - target < target - before:
                    closest_timestamps_index.append(pos)
                else:
                    closest_timestamps_index.append(pos - 1)
        
        return closest_timestamps_index