!#/bin/bash
#options rhua or cds
export server="$1"
#options /dev/$someDevice
export device="$2"

if [ "$server" == "rhua" ]; then
 echo "RHUI Selected"
 mkdir /var/lib/pulp
 chown apache:apache /var/lib/pulp
 ls /var/lib/pulp
 hostname -v $my_rhua
fi
if [[ "$server" == "cds1" ]] || [[ "$server" == "cds2" ]]; then
 echo "CDS Selected"
 mkdir /var/lib/pulp-cds
 chown apache:apache /var/lib/pulp-cds
 ls /var/lib/pulp-cds
fi

fdisk /dev/$device << EOF
n
p
1
1

p
w
EOF

export partition=1
mkfs.ext4 /dev/$device$partition

if [ "$server" == "rhua" ]; then
 echo "/dev/$device$partition /var/lib/pulp ext4 defaults 1 1" >> /etc/fstab
 mount -a 
 mount 
fi
if [[ "$server" == "cds1" ]] || [[ "$server" == "cds2" ]]; then
 echo "/dev/$device$partition /var/lib/pulp-cds ext4 defaults 1 1" >> /etc/fstab
 mount -a
 mount
fi


