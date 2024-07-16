from utils.get_vehicle_motion_state_ts import GetVehicleMotionStateTS

class ManualControlSetpoint: 
    def __init__(self, *args, **kwargs):
        self.ards = args
        self.manual_control_setpoint_dict = kwargs.get("manual_control_setpoint")
        self.vehicle_local_position = kwargs.get("vehicle_local_position")
        self.vehicle_status = kwargs.get("vehicle_status")
        self.vehicle_land_detected_dict = kwargs.get("vehicle_land_detected_dict")
        self.log_thresholds = kwargs.get("log_thresholds")
    
    def manual_control_present(self):
        diff = 0
        prev = 0
        manual_control_setpoint_interval_fault = 0
        manual_control_ts_sec = []

        vehicle_status_idx_center_stick=[]
        local_pos_idx_center_stick=[]
        land_detector_center_stick=[]

        sticks_centered_ts = []
        sticks_not_centered_ts = []

        for index, value in enumerate(self.manual_control_setpoint_dict["timestamp"]): 
            # stick centered
            if  (self.log_thresholds.get_threshold("manual_control_stick_center_x")[0] < self.manual_control_setpoint_dict["x"][index] > self.log_thresholds.get_threshold("manual_control_stick_center_x")[1] and 
                self.log_thresholds.get_threshold("manual_control_stick_center_y")[0] < self.manual_control_setpoint_dict["y"][index] > self.log_thresholds.get_threshold("manual_control_stick_center_y")[1] and
                self.log_thresholds.get_threshold("manual_control_stick_center_z")[0] < self.manual_control_setpoint_dict["z"][index] > self.log_thresholds.get_threshold("manual_control_stick_center_z")[1]): 
                    sticks_centered_ts.append(value/100000)
            else: 
                sticks_not_centered_ts.append(value/1000000)
        
        vehicle_motion_state_ts = GetVehicleMotionStateTS()
        vehicle_status_idx_center_stick = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.vehicle_local_position["timestamp"], sticks_centered_ts)
        local_pos_idx_center_stick = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.vehicle_status["timestamp"], sticks_centered_ts)
        land_detector_center_stick = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.vehicle_land_detected_dict["timestamp"], sticks_centered_ts)

        vehicle_status_idx_noncenter_stick = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.vehicle_local_position["timestamp"], sticks_not_centered_ts)
        local_pos_idx_noncenter_stick = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.vehicle_status["timestamp"], sticks_not_centered_ts)
        land_detector_noncenter_stick = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.vehicle_land_detected_dict["timestamp"], sticks_not_centered_ts)
        
        hover_check_fault, hover_check_fault_ts = self.check_vehicle_motion(sticks_centered_ts,vehicle_status_idx_center_stick,local_pos_idx_center_stick,land_detector_center_stick)
        motion_check_fault, motion_check_fault_ts = self.check_vehicle_motion(sticks_not_centered_ts,vehicle_status_idx_noncenter_stick,local_pos_idx_noncenter_stick,land_detector_noncenter_stick)
        ts_interval_check_fault, ts_interval_check_fault_ts = self.check_interval_between_ts()

        if hover_check_fault > 0: 
            print("Manual Control Error! Zero velocity, stick not centered at",hover_check_fault, hover_check_fault_ts)
        elif motion_check_fault > 0: 
            print("Manual Control Error! Vehicle moving while stick centered ", motion_check_fault, motion_check_fault_ts)
        elif manual_control_setpoint_interval_fault > 0: 
            print("Manual Control Error! Time inteval btw ts > 0.5", manual_control_setpoint_interval_fault, manual_control_setpoint_interval_fault_ts )

        if hover_check_fault > 0 or motion_check_fault > 0 or manual_control_setpoint_interval_fault > 0:
            return False
        else: 
            return True

    def check_interval_between_ts(self):
        diff = 0
        prev = 0
        manual_control_setpoint_interval_fault = 0
        manual_control_setpoint_interval_fault_ts = []

        for value in self.manual_control_setpoint_dict["timestamp"]: 
            if diff == 0: 
                prev = value

            diff = (value - prev)/1000000
            prev=value

            if diff > self.log_thresholds.get_threshold("manual_control_timeinverval_diff"): 
                manual_control_setpoint_interval_fault+=1
                manual_control_setpoint_interval_fault_ts.append(value)
        
        return manual_control_setpoint_interval_fault, manual_control_setpoint_interval_fault_ts

    def check_vehicle_motion(self, ts, vehiclestatus_idx, localpos_idx, landdetector_idx): 
        manual_control_stick_fault = 0
        manual_control_stick_fault_ts = []

        vehiclestatus_idx = []
        localpos_idx= []
        landdetector_idx = []
        for index, value in enumerate(ts): 
        
            # armed and not landed
            if self.vehicle_status["arming_state"][vehiclestatus_idx] == 2 and \
                self.vehicle_land_detected_dict["landed"][landdetector_idx] == 0:  # not landed

                # TODO: only checking fo stick movements in position mode for now, 
                # see if we can comeup with more test cases for manual and altitude mode aswell
                # for index, value in enumerate(self.manual_control_setpoint_dict["timestamp"]):             
                if self.vehicle_status["nav_state"][vehiclestatus_idx] == 2: # in position mode
                    # if the vehicle is hovering
                    if (self.log_thresholds.get_threshold("hover_flight_vel")[0] < self.vehicle_local_position['vx'][localpos_idx] < self.log_thresholds.get_threshold("hover_flight_vel")[1] and 
                        self.log_thresholds.get_threshold("hover_flight_vel")[0] < self.vehicle_local_position['vy'][localpos_idx] < self.log_thresholds.get_threshold("hover_flight_vel")[1] and 
                        self.log_thresholds.get_threshold("hover_flight_vel")[0] < self.vehicle_local_position['vz'][localpos_idx] < self.log_thresholds.get_threshold("hover_flight_vel")[1]):
                            pass # sticks are centered, which is expected
                    else:
                        manual_control_stick_fault_ts.append(self.manual_control_setpoint_dict["timestamp"][index])
                        manual_control_stick_fault += 1

        return manual_control_stick_fault, manual_control_stick_fault_ts

    def check_manual_control(self):
        self.manual_control_status={}
        
        manual_control_present = self.manual_control_present()

        self.manual_control_ok = manual_control_present
        self.manual_control_status["status"] = manual_control_present
        self.manual_control_status["value"] = manual_control_present
        return self.manual_control_status