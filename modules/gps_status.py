class GpsStatus:
    def __init__(self, *args, **kwargs):
        self.ards = args
        self.gps_data_dict = kwargs.get('data')
        self.gps_status_dict = {}
        self.log_thresholds = kwargs.get('log_thresholds')

    def check_satcount(self, satcount_arr): 
        # sat count must be > 20 all the time 
        for count in satcount_arr: 
            if count < self.log_thresholds.get_threshold("gps_satellites_count_min"):
                return False
            else:
                return True

    def check_hor_acc(self, hdop_arr):
        # gps horizontal accuracy < 0.5 m
        for hdop in hdop_arr:
            if hdop > self.log_thresholds.get_threshold("gps_min_horizontal_accuracy"):
                return False
            else: 
                return True
    
    def check_jamming(self, jamming_arr):
        # gps jamming should be less than 20 and no spikes above 80
        #TODO: determine spikes in this 
        for jamming_val in jamming_arr:
            if jamming_val < self.log_thresholds.get_threshold("gps_jamming"):
                return True 
            else:
                return False

    def gps_ok(self): 
        gps_status_dict = {}

        if (self.check_satcount(self.gps_data_dict["satellites_used"]) and self.check_hor_acc(self.gps_data_dict["eph"]) and
            self.check_jamming(self.gps_data_dict["jamming_indicator"])):
            gps_status_dict["status"] = True
        else:
            gps_status_dict["status"] = False
        
        gps_status_dict["value"] = {
            "sat count OK" : self.check_satcount(self.gps_data_dict["satellites_used"]),
            "horizontal accuracy OK": self.check_hor_acc(self.gps_data_dict["hdop"]),
            "GPS jamming OK": self.check_jamming(self.gps_data_dict["jamming_indicator"])
        }

        return gps_status_dict
            
