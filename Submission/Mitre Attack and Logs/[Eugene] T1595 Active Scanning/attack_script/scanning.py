
import socket
import subprocess
import sys
from datetime import datetime
import random

IP_ADDRESS = "192.168.91.1"

def main():
    print("scanning started")
    # target = socket.gethostbyname(sys.argv[1])
    target = IP_ADDRESS
    try:
    # will scan ports between 1 to 65,535
        for dst_port in range(1, 65535):
            src_port = random.randint(1, 65535)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.bind("192.168.91.2")
            socket.setdefaulttimeout(1)
            # returns an error indicator
            s.bind(("192.168.91.128", src_port))
            result = s.connect_ex((target, dst_port))
            print("Scanning port:" + str(dst_port) + "\n")
            if result == 0:
                print("Port {} is open".format(dst_port))
            s.close()

    except KeyboardInterrupt:
            print("\n Exiting Program !!!!")
            sys.exit()
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
    except socket.error as e:
        print(e)
        print("\ Server not responding !!!!")
    sys.exit()


if __name__ == "__main__":
    main()
