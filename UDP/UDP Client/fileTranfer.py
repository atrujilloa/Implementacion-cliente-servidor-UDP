import socket                   # Import socket module
import hashlib
import logging
import time

logger = logging.getLogger('log_udp_client')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('log_udp_client.log')
fh.setLevel(logging.INFO)
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)



def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 60000                    # Reserve a port for your service.

message = b"fkl"

try:
    sent = s.sendto(message, (host, port))

    # Receive response
    print('waiting to receive')
    data, server = s.recvfrom(1024)
    print(data.decode())

    eleccion = input("Escoja un archivo: ")

    s.sendto(eleccion.encode(), (host, port))

    dataHash = s.recv(1024).decode()
    print(dataHash)
    time1 = time.time()
    buf=1024
    f = open('video.mp4','wb')
    data,addr = s.recvfrom(buf)
    time1 = time.time()
    try:
        while(data):
            f.write(data)
            s.settimeout(2)
            data,addr = s.recvfrom(buf)
    except timeout:
        f.close()
        s.close()
        print("File Downloaded")
        time2 = time.time()
        logger.info("Transferencia finalizada en {:.3f} ms".format((time2-time1)*1000.0))

finally:
    print('closing socket')
    s.close()