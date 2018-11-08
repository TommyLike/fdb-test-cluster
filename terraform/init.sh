#!/bin/bash
set -e

VM_TYPE=$1
SELF_IP=$2
SEED_IP=$3
FDB_CLUSTER=$4
FDB_INIT_STRING=$5

echo "./init.sh $@"

# avoid confusing FoundationDB
service foundationdb stop

# resolve IP address as host name
echo "$SELF_IP $(hostname)" >> /etc/hosts

# wipe the data from the image
rm -rf /var/lib/foundationdb/data/4500/

# make 1st node the coordinator
echo "$FDB_CLUSTER" > /etc/foundationdb/fdb.cluster

# ensure the correct permissions
chown -R foundationdb:foundationdb /etc/foundationdb
chmod -R ug+w /etc/foundationdb

# make sure the cluster file is writeable by everybody
chmod o+w /etc/foundationdb/fdb.cluster

# NVME disks aren't formatted. Mounting them in fstab - no good
# mounting NVME disk: https://stackoverflow.com/questions/45167717/mounting-a-nvme-disk-on-aws-ec2
case $VM_TYPE in
"m3.large" | "m3.medium")
    echo use local instance store
    mount /dev/xvdb /var/lib/foundationdb
    echo /dev/xvdb  /var/lib/foundationdb ext3 defaults,nofail 0 2 >> /etc/fstab
    mkdir -p /var/lib/foundationdb/data
    chown -R foundationdb:foundationdb /var/lib/foundationdb
    ;;
"i3.large" | "m5d.xlarge" | "m5d.2xlarge")
    echo SSD optimized
    mkfs.ext4 -E nodiscard /dev/nvme1n1
    # ext4 filesystems should be mounted with mount options default,noatime,discard
    mount /dev/nvme1n1 /var/lib/foundationdb
    mkdir -p /var/lib/foundationdb/data
    chown -R foundationdb:foundationdb /var/lib/foundationdb
    ;;
"i3.xlarge" )
    echo SSD optimized
    mkfs.ext4 -E nodiscard /dev/nvme0n1
    # ext4 filesystems should be mounted with mount options default,noatime,discard
    mount /dev/nvme0n1 /var/lib/foundationdb
    mkdir -p /var/lib/foundationdb/data
    chown -R foundationdb:foundationdb /var/lib/foundationdb
    ;;
"i3.4xlarge")
    mkdir -p /var/lib/foundationdb1
    mkdir -p /var/lib/foundationdb2
    echo SSD optimized
    mkfs.ext4 -E nodiscard /dev/nvme0n1
    mkfs.ext4 -E nodiscard /dev/nvme1n1
    # ext4 filesystems should be mounted with mount options default,noatime,discard
    mount /dev/nvme0n1 /var/lib/foundationdb1
    mount /dev/nvme1n1 /var/lib/foundationdb2
    mkdir -p /var/lib/foundationdb1/data
    mkdir -p /var/lib/foundationdb2/data
    chown -R foundationdb:foundationdb /var/lib/foundationdb1
    chown -R foundationdb:foundationdb /var/lib/foundationdb2
    ;;
"m5d.4xlarge" )
    mkdir -p /var/lib/foundationdb1
    mkdir -p /var/lib/foundationdb2
    echo SSD optimized
    mkfs.ext4 -E nodiscard /dev/nvme1n1
    mkfs.ext4 -E nodiscard /dev/nvme2n1
    # ext4 filesystems should be mounted with mount options default,noatime,discard
    mount /dev/nvme1n1 /var/lib/foundationdb1
    mount /dev/nvme2n1 /var/lib/foundationdb2
    mkdir -p /var/lib/foundationdb1/data
    mkdir -p /var/lib/foundationdb2/data
    chown -R foundationdb:foundationdb /var/lib/foundationdb1
    chown -R foundationdb:foundationdb /var/lib/foundationdb2
    ;;
esac

service foundationdb start

if [ "$SELF_IP" == "$SEED_IP" ]; then
    echo "Seed setup"
    sleep 5 # make sure the service has started
    fdbcli --exec "$FDB_INIT_STRING" --timeout 60
    fdbcli --exec "coordinators auto; status" --timeout 60
fi