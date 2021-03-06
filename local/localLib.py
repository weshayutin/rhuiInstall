#!/usr/bin/python -tt

import os
import re
import  urllib
from urlparse import urlparse
from fabric.api import env, run  # , put, settings
#also considering rpyc


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
        mySplit = i.split("::")
        o.write(re.sub(mySplit[0], mySplit[1], data))
        o.close()

class lc:
    
    @staticmethod
    def prepInstall(myRHUIEnv, clientEnv, cfg):
        dvdURL = cfg.MAIN.dvd
        ec2Key = cfg.EC2.east_key
        partition_prep = ""
        if cfg.STORAGE.gluster == "True":
                gluster = True
                partition_prep = "prepEC2gluster.sh"
        else:
                gluster = False
                partition_prep = "prepEC2partitions.sh"
                
        rhuiVersion = dvdURL.split('/')[-1].split('-')[3]
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
                #update config
                private_hostname = e['private_dns_name'].encode('ascii')
                origTxt = 'export my_rhua=host.internal'
                newTxt = 'export my_rhua=' + private_hostname
                stringToChange.append(origTxt + "::" + newTxt)
                #version
                origTxt = 'export version=change_me'
                newTxt = 'export version=' + rhuiVersion
                stringToChange.append(origTxt + "::" + newTxt)
                #scp iso
                conn = myRHUIEnv['rhuaCMD']
                public_hostname = e['public_dns_name'].encode('ascii')
                print('scp ' + dvd + ' to ' + public_hostname)
                conn.scp_put('/tmp/' + dvd, '/root')
                #scp key
                print('scp ' + 'ec2_key ' + ' to ' + public_hostname)
                conn.scp_put(ec2Key, '/root')
                conn.scp_put('ec2/' + partition_prep, '/root')
                conn.scp_put(e['ent_cert'], '/root')
    
            if i == 'cds1':
                #update config
                private_hostname = e['private_dns_name'].encode('ascii')
                origTxt = 'export my_cds1=host.internal'
                newTxt = 'export my_cds1=' + private_hostname
                stringToChange.append(origTxt + "::" + newTxt)
                #scp iso
                conn = myRHUIEnv['cds1CMD']
                public_hostname = e['public_dns_name'].encode('ascii')
                print('scp ' + dvd + ' to ' + public_hostname)
                conn.scp_put('/tmp/' + dvd, '/root')
                conn.scp_put('ec2/' + partition_prep, '/root')
    
            if i == 'cds2':
                #update config
                private_hostname = e['private_dns_name'].encode('ascii')
                origTxt = 'export my_cds2=host.internal'
                newTxt = 'export my_cds2=' + private_hostname
                stringToChange.append(origTxt + "::" + newTxt)
                #scp iso
                conn = myRHUIEnv['cds2CMD']
                public_hostname = e['public_dns_name'].encode('ascii')
                print('scp ' + dvd + ' to ' + public_hostname)
                conn.scp_put('/tmp/' + dvd, '/root')
                conn.scp_put('ec2/' + partition_prep, '/root')
                
            if i == 'cds3':
                #update config
                private_hostname = e['private_dns_name'].encode('ascii')
                origTxt = 'export my_cds3=host.internal'
                newTxt = 'export my_cds3=' + private_hostname
                stringToChange.append(origTxt + "::" + newTxt)
                #scp iso
                conn = myRHUIEnv['cds3CMD']
                public_hostname = e['public_dns_name'].encode('ascii')
                print('scp ' + dvd + ' to ' + public_hostname)
                conn.scp_put('/tmp/' + dvd, '/root')
                conn.scp_put('ec2/' + partition_prep, '/root')
        
                for i in clientEnv.keys():
                    e = clientEnv[i]
                    if i == 'proxy':
                        private_hostname = e['private_dns_name'].encode('ascii')
                        origTxt = '#export my_proxy=host.internal'
                        newTxt = 'export my_proxy=' + private_hostname
                        stringToChange.append(origTxt + "::" + newTxt)
                        
                        origTxt = '# proxy_server_host: proxy.example.com'
                        newTxt = 'proxy_server_host: ' + '$my_proxy'
                        stringToChange.append(origTxt + "::" + newTxt)
                        
                        origTxt = '# proxy_server_port: 443'
                        newTxt = 'proxy_server_port: 3128'
                        stringToChange.append(origTxt + "::" + newTxt)
                        
        keyName = ec2Key.split('/')[-1]
        stringToChange.append('export ec2pem=key::export ec2pem=/root/'
            + keyName)
        sedFile('shell/installRHUI.sh', '/tmp/installRHUI.sh', stringToChange)
    
        e = myRHUIEnv['rhua']
        conn = myRHUIEnv['rhuaCMD']
        public_hostname = e['public_dns_name'].encode('ascii')
        print('scp  script ' + ' to ' + public_hostname)
        conn.scp_put('/tmp/installRHUI.sh', '/root')
        print('rhuiVersion =', rhuiVersion)
        if rhuiVersion > "1.2":
            part = conn.rc('parted -l  | grep Disk  | sed -n 2p')[0][10:14]
        elif rhuiVersion == "1.2":
            part = conn.rc('fdisk -l  | grep Disk  | sed -n 2p')[0][10:13]
        dict = myRHUIEnv['rhua']
        dict['partition'] = part
        #conn.rc('bash /root/installRHUI.sh rhua '+ part)

    @staticmethod
    def runInstall(myRHUIEnv, ec2Key, rhui_version, cfg):
        rhua = myRHUIEnv['rhua']
        conn = myRHUIEnv['rhuaCMD']
        public_hostname = rhua['public_dns_name'].encode('ascii')        
        if cfg.STORAGE.gluster == "True":
            gluster = True
            partition_prep = "prepEC2gluster.sh"
        else:
            gluster = False
            partition_prep = "prepEC2partitions.sh" 
            part = rhua['partition']

        env.host_string = public_hostname
        env.user = 'root'
        env.key_filename = ec2Key
        if gluster:
            run('bash /root/' + partition_prep + ' rhua ')
        else:
            if rhui_version[0:3] == '1.2':
                run('bash /root/' + partition_prep + ' rhua ' + part + ' ext3')
            else:
                run('bash /root/' + partition_prep + ' rhua ' + part)
        run('bash /root/installRHUI.sh rhua ')
        if rhui_version[0:3] == '2.0':
            run('rhui-installer /root/answers20x.txt')
        else:
            run('rhui-installer /root/answers21x.txt')
        run('tar -cvf /root/rhuiCFG.tar /tmp/rhui')

        conn.scp_get('/root/rhuiCFG.tar', '/tmp')
        run('rpm -Uvh /tmp/rhui/rh-rhua-config-1.0-2.el6.noarch.rpm')

    @staticmethod
    def installCDS(configEnv, myRHUIEnv, cfg):
        if 'CDS1' in configEnv:
            cds1 = myRHUIEnv['cds1']
            conn = myRHUIEnv['cds1CMD']
            conn.scp_put('/tmp/rhuiCFG.tar', '/root/')
            conn.scp_put('/tmp/installRHUI.sh', '/root')
            public_hostname = cds1['public_dns_name'].encode('ascii')
            env.host_string = public_hostname
            if cfg.STORAGE.gluster == "True":
                gluster = True
                partition_prep = "prepEC2gluster.sh"
            else:
                gluster = False
                partition_prep = "prepEC2partitions.sh" 
                part = rhua['partition']            

            run('tar -xvf /root/rhuiCFG.tar')
            run('cp -Rv /root/tmp/rhui /tmp')

            rhua = myRHUIEnv['rhua']
            part = rhua['partition']
            if gluster:
                run('bash /root/' + partition_prep + ' cds1')
            else:
                run('bash /root/' + partition_prep + ' cds1 ' + part)
            run('bash /root/installRHUI.sh cds1')
            run('rpm -Uvh /root/tmp/rhui/rh-cds1-config-1.0-2.el6.noarch.rpm')

        if 'CDS2' in configEnv:
            cds2 = myRHUIEnv['cds2']
            conn = myRHUIEnv['cds2CMD']
            conn.scp_put('/tmp/rhuiCFG.tar', '/root/')
            conn.scp_put('/tmp/installRHUI.sh', '/root')
            public_hostname = cds2['public_dns_name'].encode('ascii')
            env.host_string = public_hostname

            run('tar -xvf /root/rhuiCFG.tar')
            run('cp -Rv /root/tmp/rhui /tmp')

            rhua = myRHUIEnv['rhua']
            part = rhua['partition']
            run('bash /root/prepEC2partitions.sh cds2 ' + part)
            run('bash /root/installRHUI.sh cds2')
            run('rpm -Uvh /root/tmp/rhui/rh-cds1-config-1.0-2.el6.noarch.rpm')
            
        if 'CDS3' in configEnv:
            cds3 = myRHUIEnv['cds3']
            conn = myRHUIEnv['cds3CMD']
            conn.scp_put('/tmp/rhuiCFG.tar', '/root/')
            conn.scp_put('/tmp/installRHUI.sh', '/root')
            public_hostname = cds3['public_dns_name'].encode('ascii')
            env.host_string = public_hostname

            run('tar -xvf /root/rhuiCFG.tar')
            run('cp -Rv /root/tmp/rhui /tmp')
            rhua = myRHUIEnv['rhua']
            part = rhua['partition']
            run('bash /root/prepEC2partitions.sh cds3 ' + part)
            run('bash /root/installRHUI.sh cds3')
            run('rpm -Uvh /root/tmp/rhui/rh-cds3-config-1.0-2.el6.noarch.rpm')
            
    @staticmethod
    def installSquidProxy(clientEnv, myRHUIEnv):
        prxy = clientEnv['proxy']
        conn = clientEnv['proxyCMD']
        proxy_hostname = prxy['private_dns_name'].encode('ascii')
        
        rhua = myRHUIEnv['rhua']
        rhuaCMD = myRHUIEnv['rhuaCMD']
        
        conn.rc('yum -y install squid')
        conn.rc('iptables -F')
        conn.rc('iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT')
        conn.rc('iptables -A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT')
        conn.rc('iptables  -A INPUT -p tcp --dport 3128 -m state --state NEW,ESTABLISHED -j ACCEPT')
        conn.rc('service iptables save')
        conn.rc('service iptables restart')
        
        orig = 'proxy_url = https://' + proxy_hostname + '/'
        change = 'proxy_url = http://' + proxy_hostname
        cmd = 'sed -i "s@'+ orig + '@' + change + '@g" /etc/pulp/pulp.conf'
        print(cmd)
        rhuaCMD.rc(cmd)
        rhuaCMD.rc('cat /etc/pulp/pulp.conf | grep proxy')
        rhuaCMD.rc('service pulp-server restart')
                
        if prxy['proxyAuth'] == 'True':
            print('adding proxy settings for user auth')
        else:
            print('no authentication')
        
        conn.rc('service squid restart')
        
        '''
        test proxy w/
        ~/.elinks/elinks.conf: 
        set protocol.http.proxy.host = "foo.bar.com:8080" 
        set protocol.http.proxy.user = "johndoe" 
        set protocol.http.proxy.passwd = "123456"
        '''






