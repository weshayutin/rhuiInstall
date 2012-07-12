#!/usr/bin/python -tt


import time
#from boto import ec2
from boto import ec2
from boto.ec2.blockdevicemapping import EBSBlockDeviceType, BlockDeviceMapping



class ec2h:
    # Define hwp
    m1Small = {"name":"m1.small", "memory":"1700000", "cpu":"1", "arch":"i386"}
    m1Large = {"name": "m1.large","memory":"7500000","cpu":"2","arch":"x86_64"}
    m1Xlarge = {"name": "m1.xlarge","memory":"15000000","cpu":"4","arch":"x86_64"}
    t1Micro = {"name":"t1.micro","memory":"600000","cpu":"1","arch":"both"}
    m2Xlarge = {"name":"m2.2xlarge","memory":"17100000","cpu":"2","arch":"x86_64"}
    m22Xlarge = {"name":"m2.2xlarge","memory":"34200000","cpu":"4","arch":"x86_64"}
    m24Xlarge = {"name":"m2.4xlarge","memory":"68400000","cpu":"8","arch":"x86_64"}
    c1Medium = {"name":"c1.medium","memory":"1700000","cpu":"2","arch":"i386"}
    c1Xlarge = {"name":"c1.xlarge","memory":"7000000","cpu":"8","arch":"x86_64"}

    #Use all hwp types for ec2 memory tests, other hwp tests
    #hwp_i386 = [c1Medium, t1Micro , m1Small ]
    #hwp_x86_64 = [m1Xlarge, t1Micro , m1Large , m24Xlarge , c1Xlarge]
    #hwp_x86_64 = [m1Large , m1Xlarge]


    #Use just one hwp for os tests
    hwp_i386 = [c1Medium]
    hwp_x86_64 = [m1Large]


    def __init__(self,region_name, key, secret):
        """establish a connection with ec2"""
        self.region_name = region_name
        self.key = key
        self.secret = secret
        self.region = ec2.get_region(self.region_name, aws_access_key_id=self.key,
            aws_secret_access_key=self.secret)
        self.connection = self.region.connect(aws_access_key_id=self.key,
            aws_secret_access_key=self.secret)
        
    def getConnection(self):
        return self.connection

    '''starts instance, returns ec2 instances object'''
    def startInstance(self, ami, ec2_keyName, sec_group):
        map = BlockDeviceMapping()
        t = EBSBlockDeviceType()
        t.size = '15'
        #map = {'DeviceName':'/dev/sda','VolumeSize':'15'}
        map['/dev/sda1'] = t
        reservation = self.connection.run_instances(ami,
             instance_type='m1.large', key_name=ec2_keyName,
             security_groups=sec_group, block_device_map=map)

        myinstance = reservation.instances[0]

        time.sleep(5)
        while(not myinstance.update() == 'running'):
            time.sleep(5)
            print myinstance.update()

        #pprint(instanceDetails)
        return myinstance



'''
thisInstance = startInstance(myConn, 'm1.large')
instanceDetails = thisInstance.__dict__
this_hostname = instanceDetails['public_dns_name']

print "sleep for 130 seconds"
time.sleep(130)
print(this_hostname)
'''
