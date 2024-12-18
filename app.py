import bluetooth as bt

def log(val, name):
    print(f'\n {name} = {val}\n')

target_name = "S23 Dan"
target_address = None

nearby_devices = bt.discover_devices()

log(nearby_devices, 'nearby_devices')

for addr in nearby_devices:
    log(bt.lookup_name(str(addr), 30), 'bt.lookup_name(str(addr), 30)')