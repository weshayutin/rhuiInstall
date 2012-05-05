#!/usr/bin/python -tt

from fabric.api import env, run, put, settings
import paramiko
import pprint
import sys
from scp import SCPClient


class execute:

    def __init__(self, nickName, hostname, user, keyfile, keyfileName):
        self.hostname = hostname
        self.user = user
        self.keyfile = keyfile
        self.nickName = nickName
        self.connectionSuccessful = False

        #mykey = paramiko.RSAKey.from_private_key_file(keyfile)
        #public_host_key = paramiko.RSAKey(data=str(mykey))
        #self.ssh.get_host_keys().add(hostname, 'ssh-rsa', public_host_key)

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(hostname,
            username=user, key_filename=keyfile)
            self.connectionSuccessful = True
        except:
            print('ssh connection error, may need to raise timeout/sleep' +
                 ' values check settings')
            self.connectionSuccessful = False

        self.scp = SCPClient(self.ssh.get_transport())

    def rc(self, command):
        stdin, stdout, stderr  = self.ssh.exec_command(command)
        for line in stdout.read().splitlines():
            print '%s: %s' % (self.nickName, line)
        if stderr:
            for line in stderr.read().splitlines():
                print 'ERROR %s: %s' % (self.nickName, line)

    def scp_get(self, filepath, localpath):
        self.scp.get(filepath, localpath)

    def scp_put(self, filepath, localpath):
        self.scp.put(filepath, localpath)
