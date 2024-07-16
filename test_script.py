from pyulog import ULog

def main_function():

    
    
    # default_log_file = request.files['defaultLog']
    data_dict = {}
    customer_ulg_file = ULog('08_19_51.ulg')
    # default_ulg_file = ULog(default_log_file.stream)

    # get all the contents from ulg file in form of dict
    for data in customer_ulg_file.data_list:
        if "actuator_outputs" in data.name: 
            print(data.name)
            print(data.data['noutputs'])
        data_dict[data.name] = data.data
    
    # with open('output_keys.txt', 'w') as file:
    #     for key in data_dict.keys():
    #         file.write(f'{key}\n')

    
    bat_status = data_dict['battery_status'] 
    print(type(data_dict['battery_status']))
    for keys in bat_status.keys():
        # print(keys) 
        pass

if __name__ == '__main__':
    main_function()