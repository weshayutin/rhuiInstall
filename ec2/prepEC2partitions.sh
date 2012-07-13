#!/bin/bash
#options rhua or cds
export server="$1"
#options /dev/$someDevice
export device="$2"
export partition=1
#options file_filesystem ext3 or ext4
export file_system="$3"
if [ -z "$file_system" ]; then
 export file_system=ext4
fi


case "$server" in
 rhua)
  pulp_dir=/var/lib/pulp
 ;;
 cds*)
  pulp_dir=/var/lib/pulp-cds
 ;;
 *)
  echo "unsupported server: $server" >&2
  exit 1
 ;;
esac

echo selected $server

set -x
set -e
 fdisk /dev/$device << FDISK_SCRIPT
n
p
1
1

p
w
FDISK_SCRIPT

 mkfs.$file_system /dev/$device$partition
 yum -y install httpd
 mkdir -p $pulp_dir
 chown apache:apache $pulp_dir
 chmod g+ws,o+t $pulp_dir

 echo "/dev/$device$partition $pulp_dir $file_system defaults 1 1" >> /etc/fstab
 mount $pulp_dir
set +x
set +e

ls -d $pulp_dir
mount



