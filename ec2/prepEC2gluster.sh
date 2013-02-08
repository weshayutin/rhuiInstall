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

 echo "ec2-54-234-187-220.compute-1.amazonaws.com:/volume1  $pulp_dir glusterfs rw,defaults, 0 0" >> /etc/fstab
 mount $pulp_dir
 chown apache:apache $pulp_dir
 chmod g+ws,o+t $pulp_dir
 
set +x
set +e
ls -d $pulp_dir
mount