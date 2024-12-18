import bluetooth as bt

class RFCOMMClient:
    
    def __init__(self, name):
        
        self.client_name = name
        
        self.nearby_devices = bt.discover_devices()
        
        print(f'\n# Init client {self.client_name}')
    
    
    def get_nearby_devices(self):
        
        print(f'\n# Nearby Devices = {self.nearby_devices}')
        
        for addr in self.nearby_devices:
            
            print(f'\n# Name of address ({addr}) = {bt.lookup_name(addr)}')
            
    