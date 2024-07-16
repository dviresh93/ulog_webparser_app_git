from utils.get_vehicle_motion_state_ts import GetVehicleMotionStateTS

class BatteryStatus: 
    def __init__(self, *args, **kwargs):
        self.ards = args
        self.kwargs = kwargs 
        self.bat0_dict = kwargs.get('bat0_data')
        self.bat1_dict = kwargs.get('bat1_data')
        self.hover_ts = kwargs.get('hover_ts')
        self.log_thresholds = kwargs.get('log_thresholds')
        self.vehicle_land_detected_dict = kwargs.get('vehicle_land_detected_dict')
        self.bat_status_dict = {}
    
    def check_voltage(self, bat0_dict, bat1_dict): 
        fault_count = [0,0]
        voltage_dict = {}

        vehicle_not_landed_ts = []
        vehicle_not_landed_and_hovering_ts = []

        vehicle_motion_state_ts = GetVehicleMotionStateTS()
        bat0_not_landed_and_hovering_ts_indexes = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.bat0_dict["timestamp"], self.hover_ts)
        bat1_not_landed_and_hovering_ts_indexes = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.bat1_dict["timestamp"], self.hover_ts)
        # print(bat0_not_landed_and_hovering_ts_indexes)
        for index in bat0_not_landed_and_hovering_ts_indexes:  
            if self.bat0_dict['voltage_v'][index] == 0: 
                fault_count[0] += 1

        for index in bat1_not_landed_and_hovering_ts_indexes: 
            if self.bat1_dict['voltage_v'][index] == 0:
                fault_count[1] += 1

        if fault_count[0] == 0: 
            voltage_dict["bat0_status"] = True
        else:
            voltage_dict["bat0_status"] = False

        if fault_count[1] == 0: 
            voltage_dict["bat1_status"] = True
        else:
            voltage_dict["bat1_status"] = False
        
        voltage_dict["bat0_voltage_min_max"] = [min(self.bat0_dict['voltage_v']), max(self.bat0_dict['voltage_v'])]
        voltage_dict["bat1_voltage_min_max"] = [min(self.bat1_dict['voltage_v']), max(self.bat1_dict['voltage_v'])]

        return voltage_dict
    
    def check_current(self, bat0_dict, bat1_dict): 
        fault_count = [0,0]
        current_dict = {}

        vehicle_not_landed_ts = []
        vehicle_not_landed_and_hovering_ts = []
        
        vehicle_motion_state_ts = GetVehicleMotionStateTS()
        bat0_not_landed_and_hovering_ts_indexes = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.bat0_dict["timestamp"], self.hover_ts)
        bat1_not_landed_and_hovering_ts_indexes = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.bat1_dict["timestamp"], self.hover_ts)

        for index in bat0_not_landed_and_hovering_ts_indexes: 
            if self.bat0_dict['current_a'][index] == 0: 
                fault_count[0] += 1
            
        for index in bat1_not_landed_and_hovering_ts_indexes:
            if self.bat1_dict['current_a'][index] == 0: 
                fault_count[1] += 1

        # this will always fail because current sensor is not present on both the battery
        # TODO find a better way to handle this case
        if fault_count[0] == 0: 
            current_dict["bat0_status"] = True
        else:
            current_dict["bat0_status"] = False

        if fault_count[1] == 0: 
            current_dict["bat1_status"] = True
        else:
            current_dict["bat1_status"] = False

        current_dict["bat0_current_min_max"] = [min(self.bat0_dict['current_a']), max(self.bat0_dict['current_a'])]
        current_dict["bat1_current_min_max"] = [min(self.bat1_dict['current_a']), max(self.bat1_dict['current_a'])]
        
        return current_dict
    
    def check_soc(self, bat0_dict, bat1_dict): 
        fault_count = [0,0]
        soc_dict = {}

        vehicle_not_landed_ts = []
        vehicle_not_landed_and_hovering_ts = []
        
        vehicle_motion_state_ts = GetVehicleMotionStateTS()
        bat0_not_landed_and_hovering_ts_indexes = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.bat0_dict["timestamp"], self.hover_ts)
        bat1_not_landed_and_hovering_ts_indexes = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.bat1_dict["timestamp"], self.hover_ts)

        for index in bat0_not_landed_and_hovering_ts_indexes: 
            if self.bat0_dict['remaining'][index] == 0: 
                fault_count[0] += 1

        for index in bat1_not_landed_and_hovering_ts_indexes: 
            if self.bat1_dict['remaining'][index] == 0:  
                fault_count[1] += 1

        if fault_count[0] == 0:
            soc_dict["bat0_status"] = True
        else:
            soc_dict["bat0_status"] = False
        
        if fault_count[1] == 0:
            soc_dict["bat1_status"] = True
        else:
            soc_dict["bat1_status"] = False

        return soc_dict

    def check_current_at_hover(self, bat0_dict, bat1_dict): 
        # I am going to keep it this way because only of the battery have current sensosr on them
        # so with this, I am checking if any of the battery is good, I say true, else false
        # TODO need to a comeup with a better implementation for this
        bat0_fault_count = 0
        bat1_fault_count = 0
        current_at_hover = {}


        vehicle_not_landed_ts = []
        vehicle_not_landed_and_hovering_ts = []

        vehicle_motion_state_ts = GetVehicleMotionStateTS()        
        bat0_not_landed_and_hovering_ts_indexes = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.bat0_dict["timestamp"], self.hover_ts)
        bat1_not_landed_and_hovering_ts_indexes = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.bat1_dict["timestamp"], self.hover_ts)
        
        for index in bat0_not_landed_and_hovering_ts_indexes: 
            if self.log_thresholds.get_threshold("battery_current_hover")[0] < self.bat0_dict["current_a"][index] < self.log_thresholds.get_threshold("battery_current_hover")[1]: 
                bat0_fault_count += 1
        
        for index in bat1_not_landed_and_hovering_ts_indexes: 
            if self.log_thresholds.get_threshold("battery_current_hover")[0] < self.bat1_dict["current_a"][index] < self.log_thresholds.get_threshold("battery_current_hover")[1]: 
                bat1_fault_count += 1

        if bat0_fault_count == 0: 
            current_at_hover["bat0_status"] = False
        else: 
            current_at_hover["bat0_status"] = True
        
        if bat1_fault_count == 0: 
            current_at_hover["bat1_status"] = False
        else: 
            current_at_hover["bat1_status"] = True

        return current_at_hover

    def check_5v(self, bat0_dict, bat1_dict): 
        # TODO: still need to implement this, need to check how is this done in auterion suite
        return False, False

    def batteries_ok(self):
        # check voltage data 
        # check 5v data > 4.65
        # current at hover 30 - 50 A
        voltage_dict = self.check_voltage(self.bat0_dict,self.bat1_dict)
        current_dict = self.check_current(self.bat0_dict,self.bat1_dict)
        current_at_hover_dict = self.check_current_at_hover(self.bat0_dict,self.bat1_dict)
        
        soc_dict = self.check_soc(self.bat0_dict,self.bat1_dict)

        battery_count = 0
        if soc_dict['bat0_status'] and soc_dict['bat1_status']: 
            battery_count = 2
        elif (not soc_dict['bat0_status'] and soc_dict['bat1_status']) or \
            (soc_dict['bat0_status'] and not soc_dict['bat1_status']): 
                battery_count = 1
                
        # Intermediate variables for clarity
        soc_ok = battery_count == self.log_thresholds.get_threshold("battery_count")
        voltage_ok = voltage_dict["bat0_status"] and voltage_dict["bat1_status"]
        current_ok = current_dict["bat0_status"] and current_dict["bat1_status"]
        current_at_hover_ok = current_at_hover_dict["bat0_status"] and current_at_hover_dict["bat1_status"]

        # Combine all conditions into the final status
        self.bat_status_dict["status"] = (
            voltage_ok and
            current_ok and
            soc_ok and
            current_at_hover_ok
        )

        self.bat_status_dict["value"] = {
            "both_battery_voltages_present" : voltage_ok,
            "both_battery_current_present": current_ok, 
            "both_battery_soc_present" : soc_ok, 
            "both_battery_current_at_hover_OK" : current_at_hover_ok
        }

        #TODO: need to understand how is this computed in auterion suite
        # self.bat_status_dict["both_battery_5v_greater_than_4.65"] = self.check_5v(self.bat0_dict,self.bat1_dict)

        return self.bat_status_dict
