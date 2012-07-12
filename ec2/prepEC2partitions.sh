#!/bin/bash
#options rhua or cds
export server="$1"
#options /dev/$someDevice
export device="$2"
export partition=1

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

 mkfs.ext4 /dev/$device$partition
 yum -y install httpd
 mkdir -p $pulp_dir
 chown apache:apache $pulp_dir
 chmod g+ws,o+t $pulp_dir

 echo "/dev/$device$partition $pulp_dir ext4 defaults 1 1" >> /etc/fstab
 mount $pulp_dir
set +x
set +e

ls -d $pulp_dir
mount



