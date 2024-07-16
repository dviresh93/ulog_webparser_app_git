import numpy as np 
class SensorStatus: 
    def __init__(self, *args, **kwargs):
        self.ards = args
        self.sensors_combined_dict = kwargs.get('sensor_data')
        self.hover_ts_arr = kwargs.get('hover_ts')
        self.fastforward_ts_arr = kwargs.get('fastforward_ts')
        self.log_thresholds = kwargs.get('log_thresholds')
        
        self.accelgyro_noise_status = {}
    
    def check_raw_accel_data_fastforward(self): 
        self.accel_noisedata_count = [0,0,0]
        
        self.accel_x_noise_fastforward = [self.sensors_combined_dict["accelerometer_m_s2[0]"][i] for i, ts in enumerate(self.fastforward_ts_arr) if ts in self.fastforward_ts_arr]
        self.accel_y_noise_fastforward = [self.sensors_combined_dict["accelerometer_m_s2[1]"][i] for i, ts in enumerate(self.fastforward_ts_arr) if ts in self.fastforward_ts_arr]
        self.accel_z_noise_fastforward = [self.sensors_combined_dict["accelerometer_m_s2[2]"][i] for i, ts in enumerate(self.fastforward_ts_arr) if ts in self.fastforward_ts_arr]
                
        for data in self.accel_x_noise_fastforward: 
            if data < self.log_thresholds.get_threshold("accel_noise_fastforward")[0] and data > self.log_thresholds.get_threshold("accel_noise_fastforward")[1]: 
                self.accel_noisedata_count[0] +=1 
        for data in self.accel_y_noise_fastforward:
            if data < self.log_thresholds.get_threshold("accel_noise_fastforward")[0] and data > self.log_thresholds.get_threshold("accel_noise_fastforward")[1]:
                self.accel_noisedata_count[1] += 1
        for data in self.accel_z_noise_fastforward: 
            if data < self.log_thresholds.get_threshold("accel_noise_fastforward")[0] and data > self.log_thresholds.get_threshold("accel_noise_fastforward")[1]:
                self.accel_noisedata_count[2] += 1

        return self.accel_noisedata_count

    def check_raw_accel_gyro_data_hover(self):
        self.accel_noisedata_count = [0,0,0]
        self.gyro_noisedata_count = [0,0,0]
        
        self.accel_x_hover = [self.sensors_combined_dict["accelerometer_m_s2[0]"][i] for i, ts in enumerate(self.hover_ts_arr) if ts in self.hover_ts_arr]
        self.accel_y_hover = [self.sensors_combined_dict["accelerometer_m_s2[1]"][i] for i, ts in enumerate(self.hover_ts_arr) if ts in self.hover_ts_arr]
        self.accel_z_hover = [self.sensors_combined_dict["accelerometer_m_s2[2]"][i] for i, ts in enumerate(self.hover_ts_arr) if ts in self.hover_ts_arr]

        self.gyro_x_hover = [self.sensors_combined_dict["gyro_rad[0]"][i] for i, ts in enumerate(self.hover_ts_arr) if ts in self.hover_ts_arr]
        self.gyro_y_hover = [self.sensors_combined_dict["gyro_rad[1]"][i] for i, ts in enumerate(self.hover_ts_arr) if ts in self.hover_ts_arr]
        self.gyro_z_hover = [self.sensors_combined_dict["gyro_rad[2]"][i] for i, ts in enumerate(self.hover_ts_arr) if ts in self.hover_ts_arr]
                
        for data in self.accel_x_hover: 
            if data < self.log_thresholds.get_threshold("accel_noise_hover")[0] and data > self.log_thresholds.get_threshold("accel_noise_hover")[1]: 
                self.accel_noisedata_count[0] +=1 
        for data in self.accel_y_hover:
            if data < self.log_thresholds.get_threshold("accel_noise_hover")[0] and data > self.log_thresholds.get_threshold("accel_noise_hover")[1]:
                self.accel_noisedata_count[1] += 1
        for data in self.accel_z_hover: 
            if data < self.log_thresholds.get_threshold("accel_noise_hover")[0] and data > self.log_thresholds.get_threshold("accel_noise_hover")[1]:
                self.accel_noisedata_count[2] += 1

        for data in self.gyro_x_hover: 
            if data < self.log_thresholds.get_threshold("gyro_noise_hover")[0] and data > self.log_thresholds.get_threshold("gyro_noise_hover")[1]: 
                self.gyro_noisedata_count[0] +=1 
        for data in self.gyro_y_hover:
            if data < self.log_thresholds.get_threshold("gyro_noise_hover")[0] and data > self.log_thresholds.get_threshold("gyro_noise_hover")[1]:
                self.gyro_noisedata_count[1] += 1
        for data in self.gyro_z_hover: 
            if data < self.log_thresholds.get_threshold("gyro_noise_hover")[0] and data > self.log_thresholds.get_threshold("gyro_noise_hover")[1]:
                self.gyro_noisedata_count[2] += 1

        return self.accel_noisedata_count, self.gyro_noisedata_count

    def accel_gyro_check(self): 
        self.accel_noisedata_hover_count, self.gyro_noisedata_hover_count = self.check_raw_accel_gyro_data_hover()
        self.accel_noisedata_fastforward_count = self.check_raw_accel_data_fastforward()
        self.accelgyro_noise_status = {}

        for i in range(3): 
            if (self.accel_noisedata_hover_count[i] < 1 or self.gyro_noisedata_hover_count[i] < 1 or
                self.accel_noisedata_fastforward_count[i]<1): 
                self.accelgyro_noise_status["status"] = True
            else: 
                self.accelgyro_noise_status["status"] = False

        self.accelgyro_noise_status["value"] = {
            "accel_x_noise_hover_OK": self.accel_noisedata_hover_count[0]<1,
            "accel_y_noise_hover_OK": self.accel_noisedata_hover_count[1]<1,
            "accel_z_noise_hover_OK": self.accel_noisedata_hover_count[2]<1,
            "gyro_x_noise_hover_OK": self.gyro_noisedata_hover_count[0]<1,
            "gyro_y_noise_hover_OK": self.gyro_noisedata_hover_count[1]<1,
            "gyro_z_noise_hover_OK": self.gyro_noisedata_hover_count[2]<1,
            "gyro_x_noise_fastforward_OK": self.accel_noisedata_fastforward_count[0]<1,
            "gyro_y_noise_fastforward_OK": self.accel_noisedata_fastforward_count[1]<1,
            "gyro_z_noise_fastforward_OK": self.accel_noisedata_fastforward_count[2]<1
        }

        return self.accelgyro_noise_status
