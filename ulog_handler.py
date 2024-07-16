# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Response
from pyulog import ULog

from utils.get_vehicle_motion_state_ts import GetVehicleMotionStateTS
from utils.loadThresholds import ThreshHoldValuesLog
from utils.paramsFromLog import ParamsFromLog

from modules.sensor_status import SensorStatus
from modules.gyro_status import GyroStatus
from modules.battery_status import BatteryStatus
from modules.manual_control_setpoints import ManualControlSetpoint
from modules.check_firmware_status import FirmwareInfo
from modules.actuator_status import ActuatorStatus
from modules.parse_logged_messages import LoggedMessages
from modules.gps_status import GpsStatus
from modules.cpuload_status import cpuLoadStatus

app = Flask(__name__)
CORS(app)

def display_results_to_webpage(output):
    return Response(output, content_type='text/plain')

def ulog_messages_parser(ulog_file): 
    for m in ulog_file.logged_messages:
        print(m)
        m1, s1 = divmod(int(m.timestamp/1e6), 60)
        h1, m1 = divmod(m1, 60)
        return "{:d}:{:02d}:{:02d} {:}: {:}".format(
            h1, m1, s1, m.log_level_str(), m.message)

def create_dict_from_ulg(ulg_file):
    data_dict = {}
    bat_count=0
    for data in ulg_file.data_list:
        if "battery_status" in data.name: 
            # having to handle this battery by battery basis because in data.name - both the 
            # battery are tagged as 'battery_status', so i am creating a counter variable that 
            # seperates out batteries 
            if bat_count == 0: 
                data_dict["battery_status_0"] = data.data
                bat_count+=1
            elif bat_count == 1: 
                data_dict["battery_status_1"] = data.data
                bat_count+=1
        if "actuator_outputs" in data.name: 
            if data.data['noutputs'][0] == 8: 
                data_dict['actuator_outputs_0'] = data.data
            elif data.data['noutputs'][1] == 4: 
                data_dict['actuator_outputs_1'] = data.data
        else: 
            data_dict[data.name] = data.data

    if bat_count != 2: 
        print("2 BATTERIES NOT PRESENT!!") 
        return False
    else: 
        bat_count = 0

    return data_dict

@app.route('/upload', methods=['POST'])
def main_function():
    customer_log_file = request.files['customerLog']
    customer_ulg = ULog(customer_log_file.stream)

    ulg_data_dict = create_dict_from_ulg(customer_ulg)
    version = customer_ulg.get_version_info_str()
    log_thresholds = ThreshHoldValuesLog(fw_version=version)
    params_from_log = ParamsFromLog(customer_ulg=customer_ulg)


    check_firmware_status_instance = FirmwareInfo(ulog_file_object=customer_ulg, log_thresholds=log_thresholds)
    vehicle_motion_state_ts = GetVehicleMotionStateTS(
        vehicle_local_position=ulg_data_dict['vehicle_local_position'],
        vehicle_land_detected=ulg_data_dict["vehicle_land_detected"],
        manual_control_setpoint=ulg_data_dict['manual_control_setpoint'],
        log_thresholds=log_thresholds
    )

    battery_status_instance = BatteryStatus(
        bat0_data=ulg_data_dict['battery_status_0'],
        bat1_data=ulg_data_dict['battery_status_1'],
        hover_ts=vehicle_motion_state_ts.get_hover_ts(),
        vehicle_land_detected_dict = ulg_data_dict['vehicle_land_detected'],
        log_thresholds=log_thresholds
    )

    manual_control_setpoints_instance = ManualControlSetpoint(
        manual_control_setpoint=ulg_data_dict['manual_control_setpoint'],
        vehicle_local_position=ulg_data_dict['vehicle_local_position'], 
        vehicle_status = ulg_data_dict['vehicle_status'], 
        vehicle_land_detected_dict = ulg_data_dict['vehicle_land_detected'],
        log_thresholds=log_thresholds
    )

    gps_status_instance = GpsStatus(
        data=ulg_data_dict['vehicle_gps_position'],
        log_thresholds=log_thresholds
    )

    actuator_status_instance = ActuatorStatus(
        actuator0_output_dict=ulg_data_dict['actuator_outputs_0'],
        actuator1_output_dict=ulg_data_dict['actuator_outputs_1'],
        actuator_controls0_dict=ulg_data_dict['actuator_controls_0'],
        vehicle_land_detected_dict = ulg_data_dict['vehicle_land_detected'],
        vehicle_status=ulg_data_dict['vehicle_status'],
        hover_ts=vehicle_motion_state_ts.get_hover_ts(),
        log_thresholds=log_thresholds, 
        params_from_log=params_from_log
    )

    sensor_status_instance = SensorStatus(
        sensor_data=ulg_data_dict['sensor_combined'],
        hover_ts=vehicle_motion_state_ts.get_hover_ts(),
        fastforward_ts=vehicle_motion_state_ts.get_fast_forward_flight_ts(),
        log_thresholds=log_thresholds
    )
    cpu_load_instance = cpuLoadStatus(
        sensor_data=ulg_data_dict['cpuload'],
        vehicle_status=ulg_data_dict['vehicle_status'],
        vehicle_land_detected_dict = ulg_data_dict['vehicle_land_detected'],
        vehicle_local_position=ulg_data_dict['vehicle_local_position'], 
        log_thresholds=log_thresholds
    )

    logged_messages = LoggedMessages(
        ulog_object = customer_ulg
    )

    results = {
        "battery_status_dict": battery_status_instance.batteries_ok(),
        "gps_status_dict": gps_status_instance.gps_ok(),
        "accel_gyro_check_passed": sensor_status_instance.accel_gyro_check(),
        "actuator_output_checks_passed": actuator_status_instance.check_actuator_outputs(),
        "firmware_version": check_firmware_status_instance.fw_ok(),
        "manual_control_setpoint": manual_control_setpoints_instance.check_manual_control(), 
        "cpu load status": cpu_load_instance.cpuload_OK(),
        "check logged messages": logged_messages.check_logged_messages()
    }
    
    return jsonify(results)

if __name__ == '__main__':
    app.run()