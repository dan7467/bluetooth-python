import bluetooth as bt

def log(val, name):
    print(f'\n {name} = {val}\n')

nearby_devices = bt.discover_devices()

log(nearby_devices, 'nearby_devices')

for addr in nearby_devices:
    log(bt.lookup_name(addr), 'bt.lookup_name(addr)')