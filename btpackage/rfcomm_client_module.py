import bluetooth as bt
from .obex_file_transfer_handler import send_file_via_obex

class RFCOMMClient:
    
    def __init__(self, name):
        
        self.client_name = name
        self.nearby_devices = bt.discover_devices(lookup_names = True, flush_cache = True)  # e.g. [('28:FA:19:09:5C:1F', 'JBL Flip 5'), ...]
        self.name_of_addr = {}
        
        for device in self.nearby_devices:
            addr = device[0]
            self.name_of_addr[addr] = device[1]
        
        self.client_socket=bt.BluetoothSocket( bt.RFCOMM )
        print(f'\nInitialized client {self.client_name}.')
        self.choose_connection_from_nearby_devices()
    
    
    def choose_connection_from_nearby_devices(self):
        print('\n\n Choose device from list:')
        for i in range(len(self.nearby_devices)):
            print(f'\n \t {i} \t\t {self.nearby_devices[i][1]} \t\t (address: {self.nearby_devices[i][0]})')
            
        selection = int(input('\n\nInsert number of device and press enter: \n\n'))
        
        if selection in range(len(self.nearby_devices)):
            selected_addr = self.nearby_devices[selection][0]
            self.connect_to_service(target_address = selected_addr)
            
        else:
            print(f'\n [!] Error: you need to choose a number from the list above ({selection} is not in [0,...,{len(self.nearby_devices) - 1}]...)')
            return self.termination_prompt(-1)
        
    def connect_to_service(self, target_address):
        try:
            print('\nServices available:')
            menu = [(7, 'Nearby Sharing'), [8, 'SMS & MMS'], [12, 'OBEX Object Push']]
            
            for item in menu:
                print(f'\n \t {item[0]} \t {item[1]} ')
            
            target_port = int(input('\n\n Choose number from the list (above): \n\n'))
            if target_port not in [7, 8, 12]:
                print(f'\n [!] Error: you need to choose a number from the list above ({target_port} is not in {[x[0] for x in menu]})')
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
            
            elif target_port == 12:  # OBEX Object Push
                filename_and_path = input(f'\n\n Enter path + filename you want to send to {self.name_of_addr[target_address]}: \n\n')
                send_file_via_obex(target_address, target_port, filename_and_path)
                
        except Exception as e:
            print(f"\n [!] Error: {e}")  # C:\Users\Dan\Desktop\bluetooth-python\test_file.png
            
        finally:
            self.close_connection()
            print("\n Connection closed.")
            
        return self.termination_prompt(0)
        
        
    def close_connection(self):
        self.client_socket.close()
        print(f"\nTerminated client {self.client_name}'s socket.")
        
        
    def termination_prompt(self, code):
        print(f'\n [{code}] Ending session. \n\n')
        return code