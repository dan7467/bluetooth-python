import bluetooth as bt
from .obex_file_transfer_handler import send_file_via_obex
from .av_remote_control import AVRemoteControlTarget

class RFCOMMClient:
    
    def __init__(self, name):
        
        self.client_name = name
        self.nearby_devices = bt.discover_devices(lookup_names = True, flush_cache = True)  # e.g. [('28:FA:19:09:5C:1F', 'JBL Flip 5'), ...]
        self.num_of_devices_nearby = len(self.nearby_devices)
        self.name_of_addr = {}
        
        for device in self.nearby_devices:
            addr = device[0]
            self.name_of_addr[addr] = device[1]
        
        self.client_socket=bt.BluetoothSocket( bt.RFCOMM )
        print(f'\nInitialized client {self.client_name}.')
        self.choose_connection_from_nearby_devices()
    
    
    def choose_connection_from_nearby_devices(self):
        print(f'\n\n Found {self.num_of_devices_nearby} devices. Choose one from below:')
        for i in range(self.num_of_devices_nearby):
            print(f'\n \t {i} \t\t {self.nearby_devices[i][1]} \t\t (address: {self.nearby_devices[i][0]})')
            
        selection = int(input('\n\nInsert number of device and press enter: \n\n'))
        
        if selection in range(self.num_of_devices_nearby):
            selected_addr = self.nearby_devices[selection][0]
            self.connect_to_service(target_address = selected_addr)
            
        else:
            print(f'\n [!] Error: you need to choose a number from the list above ({selection} is not in [0,...,{len(self.nearby_devices) - 1}]...)')
            return self.termination_prompt(-1)
        
    def connect_to_service(self, target_address):
        try:
            menu = {}
            print(f'\n Loading services available for device "{self.name_of_addr[target_address]}"...\n')
            
            for services in sorted(bt.find_service(address = target_address), key= lambda x: int(x["port"])):
                if len(services["description"]) > 1:
                    print(f'\n \t Service: {services["name"]} ({services["description"]})')
                else:
                    print(f'\n \t Service: {services["name"]}')
                print(f' \t Protocol: {services["protocol"]}')
                print(f' \t Port: {services["port"]}')
                
                if services["name"] is not None and len(services["name"]) > 1:
                    menu[services["port"]] = menu.get(services["port"], []) + [services["name"]]    
                        
            target_port = int(input('\n\n Enter port of wanted service (from the list above): \n\n'))
            if target_port not in menu.keys():
                print(f'\n [!] Error: you need to choose a number from the list above ({target_port} is not in {list(menu.keys())})')
                return self.termination_prompt(-1)
            
            self.client_socket = bt.BluetoothSocket(bt.RFCOMM)
            
            if target_port == 7:  # Nearby Sharing
                # not yet implemented
                pass
            
            elif target_port == 8:  # SMS / MMS
                message = input(f'\n\n Write message to send to {self.name_of_addr[target_address]}: \n\n')
                print(f"\n Connecting to {self.name_of_addr[target_address]} (address = {target_address}, port = {target_port})...")
                self.client_socket.connect((target_address, target_port))
                print(f"\n Connected successfully to {self.name_of_addr[target_address]}!")
                self.client_socket.send(message)
                print(f"\n Sent message: {message}")
                self.close_connection()
            
            elif target_port == 12:  # OBEX Object Push
                filename_and_path = input(f'\n\n Enter path + filename you want to send to {self.name_of_addr[target_address]}: \n\n')
                send_file_via_obex(target_address, target_port, filename_and_path)
                
            elif target_port == 23: # AV Remote Control
                av_remote_control = AVRemoteControlTarget(target_address = target_address, port = target_port)
                av_remote_control.operate()
                            
            elif target_port == 25: # Advanced Audio Source
                pass
                
            else:
                print("\n Not yet implemented.")
                
        except Exception as e:
            print(f"\n [!] Error: {e}")  # C:\Users\Dan\Desktop\bluetooth-python\test_file.png
            
        finally:
            return self.termination_prompt(0)
        
        
    def close_connection(self):
        self.client_socket.close()
        print(f"\n Closed client {self.client_name}'s socket.")
        
        
    def termination_prompt(self, code):
        print(f'\n [{code}] Ending session. \n\n')
        return code