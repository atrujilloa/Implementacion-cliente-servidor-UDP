import socket
import struct
import time
import cv2
import math
import numpy as np


class FrameSegment(object):
    MAX_DGRAM = 2 ** 16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64  # Extrae 64 bytes si el frame hace overflow
    def __init__(self, sock, port, addr="224.3.29.71"):
        self.s = sock
        self.port = port
        self.addr = addr
    def udp_frame(self, img):
        """
        Compress image and Break down
        into data segments
        """
        if img is not None:
            impC = cv2.imencode('.jpg', img)[1]
            dat = impC.tobytes()
            size = len(dat)
            count = math.ceil(size / self.MAX_IMAGE_DGRAM)
            array_pos_start = 0
            while count:
                array_pos_end = min(size, array_pos_start + self.MAX_IMAGE_DGRAM)
                self.s.sendto(struct.pack("B", count) +
                            dat[array_pos_start:array_pos_end],
                            (self.addr, self.port)
                            )
                array_pos_start = array_pos_end
                count -= 1


def main():
    port = 5005
    multicastIp = "224.3.29.71"
    videoToStream = ""
    bufferSize = 1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.2)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    fs = FrameSegment(sock, port, multicastIp)
    try:
        print(" (1) video1.mp4")
        print(" (2) video2.mp4")
        print("///////////////////////////////////")
        video = int(input("Ingrese al vídeo que desea ver (1 o 2): "))
        multicast_group = (multicastIp, port)
        videoToStream = "./archivo"+str(video)+".mp4"
        print(videoToStream)
        cap = cv2.VideoCapture(videoToStream)
        print('Stremeando video%s' % (str(video) + ".mp4"))
        while cap.isOpened():
            ret, frame = cap.read()
            fs.udp_frame(frame)
        while True:
            print('waiting to receive')
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                print('timed out, no more responses')
                break
            else:
                print('received "%s" from %s' % (data, server))
        cap.release()
        cv2.destroyAllWindows()
    finally:
        print('closing socket')
        sock.close()


if __name__ == "__main__":
    main()