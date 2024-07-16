class ParamsFromLog: 
    def __init__(self, *args, **kwargs):
        self.customer_ulg = kwargs.get("customer_ulg")
    
    def get(self, key_name):
        # Extract parameters
        params = self.customer_ulg.initial_parameters
        return params[key_name]
