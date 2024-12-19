import bluetooth as bt

class AVRemoteControlTarget:
    def __init__(self, target_address, port=23):
        self.target_address = target_address
        self.port = port
        self.client_socket = bt.BluetoothSocket(bt.RFCOMM)
        self.commands = {
            "play": b"\x01",
            "pause": b"\x02",
            "volume_up": b"\x03",
            "volume_down": b"\x04",
            "exit": 0
        }
        self.connect()

    def connect(self):
        try:
            print(f"\n Connecting to AV Remote Control Target ({self.target_address}) on port {self.port}...")
            self.client_socket.connect((self.target_address, self.port))
            print("\n Connected!")
        except bt.BluetoothError as e:
            print(f"BluetoothError: {e}")
        except OSError as e:
            print(f"OSError: {e}")
        except Exception as e:
            print(f"General Error: {e}")

    def operate(self):
        print("\n Welcome to AV Remote Control!")
        print("\n Choose action:")
        for command in self.commands:
            print(f"\n \t {command}")
        while True:
            command = input('\n Choose action from above:')
            if command not in self.commands:
                print(f"Invalid command. Available commands: {list(self.commands.keys())}")
                continue
            elif command == "exit":
                self.disconnect()
                print(f"\n Disconnected AV Remote Control.")
                return
            self.client_socket.send(self.commands[command])
            print(f"Sent command: {command}")

    def disconnect(self):
        self.client_socket.close()
        print("Disconnected.")
