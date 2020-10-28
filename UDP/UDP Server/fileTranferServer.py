import socket                   # Import socket module
import hashlib
import logging
import time

port = 60000                    # Reserve a port for your service.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))                # Now wait for client connection.

logger = logging.getLogger('log_udp_server')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('log_udp_server.log')
fh.setLevel(logging.INFO)
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

buf = 1024

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

while True:
    print('\nwaiting to receive message')
    data, address = s.recvfrom(1024)

    if data:
        menu = b"""
        1. Archivo 1 (100 Mb)
        2. Archivo 2 (250 Mb)
        """
        sent = s.sendto(menu, address)

        data, address = s.recvfrom(1024)

        elec = int(data)

        if(elec == 1):
            logger.info("El cliente pidió el archivo 1")

            result = md5('archivo2.mp4')
            sent = s.sendto(result.encode(), address)
            print(result)

            filename='archivo2.mp4'
            f = open(filename,'rb')
            
            logger.info("Comenzó la transferencia del archivo")
            time1 = time.time()
            data = f.read(buf)
            while (data):
                if(s.sendto(data,address)):
                    print("sending ...")
                    data = f.read(buf)
            f.close()
            time2 = time.time()
            logger.info("Finalizó la transferencia del archivo en  {:.3f}".format((time2-time1)*1000.0))
            s.close()
        else:
            pass