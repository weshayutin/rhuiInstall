#!/bin/bash
#options rhua or cds
export server="$1"

cat > /etc/yum.repos.d/splice.repo << EOF
[splice]
name=splice_el6_x86_64
baseurl=http://ec2-23-22-86-129.compute-1.amazonaws.com/pub/el6/x86_64/
enabled=1
gpgcheck=0
EOF

yum -y install glusterfs-fuse

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