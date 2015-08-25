
# encoding:utf8
import datetime
import sys

import paramiko

def echo_slam(hostname='', username='',password='', port=22,
                logfile='/tmp' + str(datetime.date.today()) + "echo_slam.log",
                command='')
        '''dota2 earthshaker the fouth skill,
        exec command on linux or unix use paramiko. 
        '''
    try:
        paramiko.util.log_to_file(logfile)
        sshclient = paramiko.SSHClient()
        sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshclient.connect(hostname=hostname, username=username,
                            port=port, password=password)
        return sshclient.exec_command(command)

    except SSHException, sshe:
        print "ssh error: " , sshe
        sys.exit(1)
    except BadHostKeyException, bhe:
        print "host key error: ", bhe
        sys.exit(2)
    except AuthenticationException, authe:
        print "authentication error: ", authe
        sys.exit(3)

