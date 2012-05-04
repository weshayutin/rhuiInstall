#!/usr/bin/python -tt

import os
import sys
import optparse
import getpass
import time
from iniparse import INIConfig
sys.path.append('ec2')
sys.path.append('shell')
from ec2lib import ec2h
from commandRunner import execute
from fabric.api import env, run, put, settings


parser = optparse.OptionParser()
parser.add_option('-n', '--name', help='name the environment')
parser.add_option('-e', '--install_env', help='pick environment: ec2,local',
     dest='install_env', type='string')


(opts, args) = parser.parse_args()
cfg = INIConfig(open('config'))
myenv = INIConfig(open('environment'))


def checkEnvState(thisDict):
    for i in thisDict.keys():
            instance = thisDict[i].__dict__
            hostname = instance['public_dns_name'].encode('ascii')
            #quick check to make sure everything is up and running
            x = execute(i, hostname, 'root', cfg.EC2.east_key,
                 cfg.EC2.east_keyName)
            if not x.connectionSuccessful:
                exit(-1)
            print(x.rc('hostname'))


def startInstances(rhuiEnv):
    ## start an instance
    e = ec2h(cfg.EC2.region, cfg.EC2.username, cfg.EC2.password)
    myConn = e.getConnection()
    dict = {}

    for i in rhuiEnv:
        thisInstance = e.startInstance(cfg.EC2.ami_id, cfg.EC2.east_keyName,
            myConn, cfg.EC2.hwp)
        instanceDetails = thisInstance.__dict__
        this_hostname = instanceDetails['public_dns_name']
        print(this_hostname)
        dict[i] = thisInstance
    return dict


if __name__ == '__main__':
    if cfg.MAIN.environment == 'ec2':
        rhui = list(myenv)
        dict = startInstances(rhui)
        ## wait for instance and check ssh
        print('wait for instances to boot for 130 seconds')
        time.sleep(130)
        print('done waiting for instances to boot')
        checkEnvState(dict)

        if 'RHUA' in rhui:
            rhua = dict['RHUA'].__dict__
            rhuaCMD = execute('RHUA', rhua['public_dns_name'].encode('ascii'),
                'root', cfg.EC2.east_key, cfg.EC2.east_keyName)

        if 'CDS1' in rhui:
            cds1 = dict['CDS1'].__dict__
            cds1CMD = execute('CDS1', cds1['public_dns_name'].encode('ascii'),
                'root', cfg.EC2.east_key, cfg.EC2.east_keyName)

        if 'CDS2' in rhui:
            cds2 = dict['CDS2'].__dict__
            cds2CMD = execute('CDS2', cds2['public_dns_name'].encode('ascii'),
                'root', cfg.EC2.east_key, cfg.EC2.east_keyName)

        if 'CLIENT1' in rhui:
            client1 = dict['CLIENT1'].__dict__
            client1CMD = execute('CLIENT1',
                client1['public_dns_name'].encode('ascii'), 'root',
                cfg.EC2.east_key, cfg.EC2.east_keyName)

        if 'CLIENT2' in rhui:
            client2 = dict['CLIENT2'].__dict__
            client2CMD = execute('CLIENT2',
                client2['public_dns_name'].encode('ascii'),
                'root', cfg.EC2.east_key, cfg.EC2.east_keyName)

        if 'PROXY' in rhui:
            proxy = dict['PROXY'].__dict__
            proxyCMD = execute('PROXY',
            proxy['public_dns_name'].encode('ascii'),
            'root', cfg.EC2.east_key, cfg.EC2.east_keyName)

        rhuaCMD.rc('hostname')
        cds1CMD.rc('cat /etc/redhat-release')

    elif cfg.MAIN.environment == 'local':
        print('in local')







            #env.host_string = hostname
            #env.user = 'root'
            #env.key_filename = cfg.EC2.east_key
            #run('hostname')
