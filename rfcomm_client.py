import bluetooth as bt

class RFCOMMClient:
    
    def __init__(self, name):
        
        self.client_name = name
        
        self.nearby_devices = bt.discover_devices()
        
        self.name_of_addr = {}
        
        for addr in self.nearby_devices:
            
            self.name_of_addr[addr] = bt.lookup_name(addr)
        
        self.client_socket=bt.BluetoothSocket( bt.RFCOMM )
        
        print(f'\n# Initialized client {self.client_name}.')
    
    
    def choose_connection_from_nearby_devices(self):
        
        print('\n\n Choose device from list:')
        
        for i in range(len(self.nearby_devices)):
            
            addr = self.nearby_devices[i]
            
            print(f'\n# {i} {self.name_of_addr[addr]} (address: {addr})')
            
        selection = int(input('\n\n Insert number of device and press enter: \n\n'))
        
        if selection in range(len(self.nearby_devices)):
            
            selected_addr = self.nearby_devices[selection]
            
            print(f'\n # Connecting to {self.name_of_addr[addr]}...')
            
            self.connect_to(selected_addr)
            
        else:
            
            print(f'\n [!] Error: you need to choose a number from the list above ({selection} is not in {range(len(self.nearby_devices))}...)')
            
            print('\n # Ending session. \n\n')
            
            return
        
        
    def connect_to(self, addr, port = 1):
        
        self.client_socket.connect((addr, port))
        
        print(f'\n # Connected to {self.name_of_addr[addr]}!')

        self.client_socket.send("hello!!")
        
        print(f'Sent "hello!!" to {self.name_of_addr[addr]}')
        
        self.close_all_connections()
        
        
    def close_all_connections(self):

        self.client_socket.close()
            
    
    
client = RFCOMMClient('Client1')

client.choose_connection_from_nearby_devices()