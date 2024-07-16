class cpuLoadStatus:
    def __init__(self,*args,**kwargs):
        self.cpuload_dict = kwargs.get("sensor_data")
        self.vehicle_local_position = kwargs.get("vehicle_local_position")
        self.vehicle_status = kwargs.get("vehicle_status")
        self.vehicle_land_detected_dict = kwargs.get("vehicle_land_detected_dict")
        self.log_thresholds = kwargs.get("log_thresholds")
    
    def cpuload_check(self): 
        fault_counter = 0
        for value in self.cpuload_dict["load"]: 
            if value > self.log_thresholds.get_threshold("cpu_max_load"): 
                fault_counter += 1
        
        if fault_counter > 1: 
            return False
        else: 
            return True
    
    def ram_health_check(self): 
        fault_counter = 0
        for value in self.cpuload_dict["ram_usage"]:
            if value > self.log_thresholds.get_threshold("ram_max_usage"):  
                fault_counter += 1
        
        if fault_counter > 1: 
            return False
        else: 
            return True
    
    def cpuload_OK(self):
        cpuload_status = {}
        cpuload_health = None

        cpuload_health = self.cpuload_check()
        ram_health = self.ram_health_check()

        cpuload_status["status"] = (cpuload_health and ram_health)
        cpuload_status["value"] = cpuload_health

        return cpuload_status 