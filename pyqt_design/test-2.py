import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"5453034661"


sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))