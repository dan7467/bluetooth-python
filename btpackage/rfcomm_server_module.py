import bluetooth as bt

# class RFCOMMServer:
    
#     def __init__(self, port = 1):
    
#         self.socket=bt.BluetoothSocket( bt.RFCOMM )
        
#         self.port = port
        
#         self.socket.bind(("",port))
        
#         self.socket.listen(1)

#         print(f'\n# -------------------------------- Server started (port={self.port}) --------------------------------')
        
        
#     def accept_connection(self):
        
#         self.client_socket, self.address = self.socket.accept()
        
#         print(f"\n#Accepted connection from {self.address}")
        
        
#     def receive_data(self, length_in_bytes=1024):
        
#         data = self.socket.recv(length_in_bytes)
        
#         print (f"\n# Received [%s]" % data)
        
        
#     def close_socket(self):
        
#         self.client_socket.close()
        
#         self.socket.close()

#         print(f'\n# ---------------------------------------- Server closed ----------------------------------------')
        


# server = RFCOMMServer()

print("looking for nearby devices...")
nearby_devices = bt.discover_devices(lookup_names = True, flush_cache = True, duration = 20)
print("found %d devices" % len(nearby_devices))
for addr, name in nearby_devices:
    print(" %s - %s" % (addr, name))
    for services in bt.find_service(address = addr):
        print(" Name: %s" % (services["name"]))
        print(" Description: %s" % (services["description"]))
        print(" Protocol: %s" % (services["protocol"]))
        print(" Port: %s" % (services["port"]))