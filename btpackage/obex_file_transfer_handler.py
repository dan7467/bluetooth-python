from bluetooth import BluetoothSocket, RFCOMM
from PyOBEX.client import Client

def send_file_via_obex(target_address, target_port, file_path):
    try:
        print(f"\n [OBEX] Connecting to {target_address} on port {target_port}...")
        obex_client = Client(target_address, target_port)
        obex_client.connect()
        
        print("\n [OBEX] Connected successfully!")
        with open(file_path, "rb") as file:
            file_name = file_path.split("/")[-1]
            file_data = file.read()
            print(f"\n [OBEX] Sending file: {file_name} ({len(file_data)} bytes)...")
            response = obex_client.put(file_name, file_data)
            print(f"\n [OBEX] Response: {response}")
        
        print("\n [OBEX] File sent successfully!")
        
    except Exception as e:
        print(f"\n [OBEX] Error: {e}")
        
    finally:
        obex_client.disconnect()
        print("\n [OBEX] Connection closed.")