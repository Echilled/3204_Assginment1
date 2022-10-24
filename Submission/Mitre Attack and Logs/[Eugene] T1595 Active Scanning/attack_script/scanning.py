
import socket
import subprocess
import sys
from datetime import datetime


IP_ADDRESS = "20.248.199.150"

common_ports = [21, 22, 25, 80, 443]


def main():
    print("hi")
    # target = socket.gethostbyname(sys.argv[1])
    target = IP_ADDRESS
    try:
    # will scan ports between 1 to 65,535
        for port in common_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            # returns an error indicator
            result = s.connect_ex((target, port))
            if result == 0:
                print("Port {} is open".format(port))
            s.close()

    except KeyboardInterrupt:
            print("\n Exiting Program !!!!")
            sys.exit()
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
    except socket.error:
        print("\ Server not responding !!!!")
    sys.exit()


if __name__ == "__main__":
    main()
