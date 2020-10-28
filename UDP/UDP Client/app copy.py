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

s.connect((host, port))
s.send(b"Conectado!")
logger.info("UDP Cliente conectado al servidor")
data = s.recv(1024)

print(data.decode())

eleccion = input("Escoja un archivo: ")

s.send(eleccion.encode())

dataHash = s.recv(1024).decode()

logger.info("Comenzando transferencia")
time1 = time.time()
with open('video.mp4', 'wb') as f:
    print('receiving data...')
    while True:
        data = s.recv(1024)
        if not data:
            break
        # write data to a file
        f.write(data)
time2 = time.time()
logger.info("Transferencia finalizada en {:.3f} ms".format((time2-time1)*1000.0))

data = s.recv(1024).decode()

hashL = md5('video.mp4')
if(str(dataHash) == str(hashL)):
    logger.info("Los hashes coinciden")

s.close()
print('connection closed')