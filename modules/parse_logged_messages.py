class LoggedMessages:

    def __init__(self, *args, **kwargs):
        self.ulog_object = kwargs.get("ulog_object")
    
    def check_errors_in_logged_messages(self): 
        logged_messages = [(m.timestamp, m.log_level_str(), m.message) for m in self.ulog_object.logged_messages]
        
        fault_counter=0
        for i in logged_messages:
            if i[1] == "ERROR":
                fault_counter+=1
        
        if fault_counter > 1: 
            return False
        else: 
            return True

    def check_logged_messages(self): 
        logged_messages_status = {}

        logged_messages_check = None 
        logged_messages_ok = False

        logged_messages_ok = self.check_errors_in_logged_messages()

        logged_messages_status["status"] = logged_messages_ok

        if not logged_messages_ok: 
            logged_messages_status["value"] = "Review logged messages"
        else: 
            logged_messages_status["value"] = "No errors in logged messages"

        return logged_messages_status
