#!/usr/bin/python -tt

import os
import sys
import optparse
import getpass
import time
from iniparse import INIConfig
sys.path.append('ec2')
from ec2lib import ec2h
from fabric.api import env, run, put, settings


parser = optparse.OptionParser()
parser.add_option('-n', '--name', help='name the environment')
parser.add_option('-e', '--install_env', help='pick environment: ec2,local',
     dest='install_env', type='string')


(opts, args) = parser.parse_args()

# Making sure all mandatory options appeared.
if not opts.install_env:
    print "requires an environment"
    parser.print_help()
    exit(-1)

cfg = INIConfig(open('config'))


if __name__ == '__main__':
    print(opts.install_env)
    if opts.install_env == 'ec2':
        ## start an instance
        e = ec2h(cfg.EC2.region, cfg.EC2.username, cfg.EC2.password)
        myConn = e.getConnection()
        dict = {}
        #rhui = ['rhua', 'cds1', 'cds2', 'proxy', 'client']
        rhui = ['rhua', 'cds1']
        for i in rhui:
            thisInstance = e.startInstance(cfg.EC2.ami_id, cfg.EC2.east_keyName,
                myConn, 'm1.large')
            instanceDetails = thisInstance.__dict__
            this_hostname = instanceDetails['public_dns_name']
            print(this_hostname)
            dict[i] = thisInstance

        ## wait for instance and check ssh
        print dict.keys()
        print('wait for instances to boot for 130 seconds')
        time.sleep(130)
        print('done waiting for instances to boot')
        for i in dict.keys():
            instance = dict[i].__dict__
            hostname = instance['public_dns_name'].encode('ascii')
            env.host_string = hostname
            env.user = 'root'
            env.key_filename = cfg.EC2.east_key
            run('hostname')

    elif opts.install_env == 'local':
        print('in local')



