#!/usr/bin/python -tt

import os
import re
import  urllib
from urlparse import urlparse


#local commands

def sedFile(origFile, newFile, listOfChanges):
        outfile = newFile
        o = open(outfile, "w")
        data = open(origFile).read()
        o.write(data)
        o.close()
        for i in listOfChanges:
            data = open(outfile).read()
            o = open(outfile, "w")
            mySplit = i.split(":")
            o.write(re.sub(mySplit[0], mySplit[1], data))
            o.close()

class lc:

#    #rewrites file to /tmp
#    @classmethod
#    def sedFile(origFile, origTxt, newTxt):
#        outfile = "/tmp/" + file
#        o = open(outfile, "w")
#        data = open(origFile).read()
#        o.write(re.sub(origTxt, newTxt, data))
#        o.close()

    @staticmethod
    def prepInstall(myRHUIEnv, dvdURL, ec2Key):
        current = os.getcwd()
        os.chdir('/tmp')
        s = urlparse(dvdURL)
        dvd = s.path.split('/')[-1]
        urllib.urlretrieve(dvdURL, filename=dvd, reporthook=None, data=None)
        os.chdir(current)
        stringToChange = []

        for i in myRHUIEnv.keys():
            e = myRHUIEnv[i]
            if i == 'rhua':
                private_hostname = e['private_dns_name'].encode('ascii')
                origTxt = 'export my_rhua=host.internal'
                newTxt = 'export my_rhua=' + private_hostname
                stringToChange.append(origTxt + ":" + newTxt)

            if i == 'cds1':
                private_hostname = e['private_dns_name'].encode('ascii')
                origTxt = 'export my_cds1=host.internal'
                newTxt = 'export my_cds1=' + private_hostname
                stringToChange.append(origTxt + ":" + newTxt)

            if i == 'cds2':
                private_hostname = e['private_dns_name'].encode('ascii')
                origTxt = 'export my_cds2=host.internal'
                newTxt = 'export my_cds2=' + private_hostname
                stringToChange.append(origTxt + ":" + newTxt)
        stringToChange.append('export ec2pem=key:export ec2pem=' + ec2Key)
        sedFile('shell/installRHUI.sh', '/tmp/installRHUI.sh', stringToChange)

        for i in myRHUIEnv.keys():
            e = myRHUIEnv[i]
            if i == 'rhua':
                conn = myRHUIEnv['rhuaCMD']
                public_hostname = e['public_dns_name'].encode('ascii')
                print('scp ' + dvd + ' to ' + public_hostname)
                conn.scp_put('/tmp/' + dvd, '/root')
                print('scp ' + 'ec2_key ' + ' to ' + public_hostname)
                conn.scp_put(ec2Key, '/root')
                print('scp  script ' + ' to ' + public_hostname)
                conn.scp_put('/tmp/installRHUI.sh', '/root')
                part = conn.rc('parted -l  | grep Disk  | sed -n 2p')[0][10:14]
                dict = myRHUIEnv['rhua']
                dict['partition'] = part

