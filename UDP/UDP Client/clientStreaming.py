import socket
import struct
import numpy as np
import cv2

MAX_DGRAM = 2 ** 16


def dump_buffer(s):
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        print(seg[0])
        if struct.unpack("B", seg[0:1])[0] == 1:
            print("finish emptying buffer")
            break


def main():
    multicast_group = '224.3.29.71'
    server_address = ('', 5005)
    timeout = 5
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    dat = b''
    dump_buffer(sock)
    while True:
        print('\nRecibiendo video...')
        data, address = sock.recvfrom(MAX_DGRAM)

        if struct.unpack("B", data[0:1])[0] > 1:
            dat += data[1:]
        else:
            dat += data[1:]
            img = cv2.imdecode(np.fromstring(dat, dtype=np.uint8), 1)
            cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            dat = b''

    cv2.destroyAllWindows()
    sock.close()


if __name__ == "__main__":
    main()