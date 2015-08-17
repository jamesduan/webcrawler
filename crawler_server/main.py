
import sys

from server_ctl import create_server

def main():
    create_server()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt, e:
        print "cancelled by user type Ctrl+C",e
        sys.exit(1)

