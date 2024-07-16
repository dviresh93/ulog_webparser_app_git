import yaml

class ThreshHoldValuesLog:
    def __init__(self, fw_version):
        self.fw_version = fw_version
        self.config = self.load_thresholds()

    def load_thresholds(self):
        fw_map = {
            "v1.4.0": "altax_black",
            "v1.3.6": "altax_black",
            "v1.5.18": "astro_black",
            "v1.4.16": "astro_black"
        }
        drone_type = fw_map[self.fw_version]
        thr_file_location = f"thresholds/{drone_type}.yaml"
        
        with open(thr_file_location, 'r') as file:
            return yaml.safe_load(file)

    def get_threshold(self, key):
        return self.config.get(key)
