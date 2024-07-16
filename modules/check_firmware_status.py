from thresholds.FirmwareConfig import FirmwareVerMap

class FirmwareInfo: 
    def __init__(self, *args, **kwargs):
        self.ards = args
        self.kwargs = kwargs 
        self.ulog_file_object = kwargs.get('ulog_file_object')
        self.log_thresholds = kwargs.get('log_thresholds')
        self.fw_dict = {}
    def check_fw(self):
        version = self.ulog_file_object.get_version_info_str()
        
        if version in self.log_thresholds.get_threshold("fw_version"): 
            return True, version
        else: 
            return False, version

    def get_ver(self): 
        return self.ulog_file_object.get_version_info_str()
    
    def fw_ok(self):
        status, value = self.check_fw()
        self.fw_dict["status"] = status
        self.fw_dict["value"] = {"fw ver":value}
        return self.fw_dict
    