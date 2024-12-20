import bluetooth as bt

class AdvancedAudioSource:
    def __init__(self, target_address, port=25):
        self.target_address = target_address
        self.port = port
        self.client_socket = bt.BluetoothSocket(bt.RFCOMM)
        self.connect()

    def connect(self):
        print(f"\nConnecting to Advanced Audio Source ({self.target_address}) on port {self.port}...")
        self.client_socket.connect((self.target_address, self.port))
        print("\nConnected!")

    def stream_audio(self, audio_file_path):
        try:
            print(f"\nStreaming audio from {audio_file_path}...")
            with open(audio_file_path, "rb") as audio_file:
                chunk = audio_file.read(1024)
                while chunk:
                    self.client_socket.send(chunk)
                    chunk = audio_file.read(1024)
            print("\nAudio stream complete!")
        except Exception as e:
            print(f"\nError streaming audio: {e}")
        self.disconnect()

    def disconnect(self):
        self.client_socket.close()
        print("\nDisconnected.")
