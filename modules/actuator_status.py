import numpy as np
import bisect

from utils.get_vehicle_motion_state_ts import GetVehicleMotionStateTS

class ActuatorStatus: 
    def __init__(self, *args, **kwargs):
        self.actuator_output_main_dict = kwargs.get('actuator0_output_dict')
        self.actuator_controls0_dict = kwargs.get('actuator_controls0_dict')
        self.vehicle_status_dict=kwargs.get("vehicle_status")
        self.hover_ts = kwargs.get("hover_ts")
        self.log_thresholds = kwargs.get("log_thresholds")
        self.params_from_log=kwargs.get("params_from_log")
    
    def actuator_thrust_hover_check(self): 
    
        vehicle_motion_state_ts = GetVehicleMotionStateTS()
        closest_timestamps_to_hover_index = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.actuator_controls0_dict["timestamp"], self.hover_ts)
        
        actuator_thrust_hover = [self.actuator_controls0_dict["control[3]"][i] for i in closest_timestamps_to_hover_index if self.actuator_controls0_dict["control[3]"][i] != 0]    
        actuator_thrust_hover_ts = [self.actuator_controls0_dict["timestamp"][i] for i in closest_timestamps_to_hover_index if self.actuator_controls0_dict["control[3]"][i] != 0]    
        fault_count = 0
        
        for index, thrust in enumerate(actuator_thrust_hover): 
            if thrust < self.log_thresholds.get_threshold("actuator_thrust_hover")[0] or thrust > self.log_thresholds.get_threshold("actuator_thrust_hover")[1]:
                fault_count += 1
            
        if fault_count > 0:
            return False
        
        return True

    def check_aux_main_start_value(self): 
        #TODO compare parameters to see what kind of motors is the drone using
        type_of_motor = self.params_from_log.get("FF_IESC_TYPE")
        actuator_output_0 = 0

        index = 0
        for value in self.vehicle_status_dict["arming_state"]:
            if value == 2: 
                armed_ts = self.vehicle_status_dict["timestamp"][index]
                break
            index += 1
        # Initialize variables to find the closest timestamp and its index
        closest_timestamp = None
        closest_index = -1
        smallest_diff = float('inf')
        
        for i, ts in enumerate(self.actuator_output_main_dict["timestamp"]):
            diff = abs(ts - armed_ts)
            if np.isscalar(diff) and diff < smallest_diff:
                smallest_diff = diff
                closest_timestamp = ts
                closest_index = i

        # DJI Motors with NO iESC board
        if type_of_motor == 0: 
            return False

        # DJI Motors with iESC board
        elif type_of_motor == 1:
            thresholds = self.log_thresholds.get_threshold("actuator_aux_main_start_dji_iesc")
            if (self.actuator_output_main_dict["output[0]"][closest_index] == thresholds).all() and\
                (self.actuator_output_main_dict["output[1]"][closest_index] == thresholds).all() and\
                (self.actuator_output_main_dict["output[2]"][closest_index] == thresholds).all(): 
                return True

        # Hobbywing Motors with iESC board
        elif type_of_motor == 2: 
            thresholds = self.log_thresholds.get_threshold("actuator_aux_main_start_hw_iesc")
            if (self.actuator_output_main_dict["output[0]"][closest_index] in thresholds) and\
                (self.actuator_output_main_dict["output[1]"][closest_index] in thresholds) and\
                (self.actuator_output_main_dict["output[2]"][closest_index] in thresholds): 
                return True
        return False

    def actuator_yaw_outputs_mean_at_hover(self):
        vehicle_motion_state_ts = GetVehicleMotionStateTS()
        closest_timestamps_to_hover_index = vehicle_motion_state_ts.find_closest_timestamps_indexes(self.actuator_controls0_dict["timestamp"], self.hover_ts)
        
        actuator_controls_yaw_sum=0
        actuator_controls_yaw_sum = sum(self.actuator_controls0_dict["control[2]"][i] for i in closest_timestamps_to_hover_index)
        actuator_controls_yaw_mean = actuator_controls_yaw_sum/len(closest_timestamps_to_hover_index)
        
        if actuator_controls_yaw_mean < 0.5: 
            return True
        else:
            return False

    def check_actuator_outputs(self):
        actuator_outputs_status = {}

        actuator_outputs_status["status"] = self.actuator_thrust_hover_check()

        actuator_outputs_status["value"] = {
            "actuator_thrust_0.5_at_hover" : self.actuator_thrust_hover_check(),
            "actuator_yaw_outputs_mean_at_hover": self.actuator_yaw_outputs_mean_at_hover(),
            "aux_main_starting_value": self.check_aux_main_start_value(),
            "aux_main_output_values": self.check_aux_main_start_value()
        }
        # actuator_outputs_status["actuator_aux_main_start_value_correct"] = self.check_aux_main_start_value()
        #TODO: Motor currents: no full -30 to +60 stuttering except in the manual portion of flight where pitch/roll/yaw are being railed by pilot.
        #TODO: Actuator control thrust reached full (0.94) for at least 2 seconds during manual punchout.

        return actuator_outputs_status