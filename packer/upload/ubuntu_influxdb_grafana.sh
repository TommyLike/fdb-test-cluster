#!/bin/bash
set -e
set -x

# from http://unix.stackexchange.com/a/28793
# if we aren't root - elevate. This is useful for AMI
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

export DEBIAN_FRONTEND=noninteractive

# set timezone to UTC
dpkg-reconfigure tzdata

# https://groups.google.com/forum/#!msg/foundationdb-user/BtJf-1Mlx4I/fxXZClLpnOUJ
# sources: https://github.com/ripple/docker-fdb-server/blob/master/Dockerfile
# https://hub.docker.com/r/arypurnomoz/fdb-server/~/dockerfile/

# linux-aws - https://forums.aws.amazon.com/thread.jspa?messageID=769521&tstart=0

# need to clean since images could have stale metadata
apt-get clean && apt-get update
apt-get install -y -qq build-essential python linux-aws sysstat iftop htop iotop ne

######### install influxdb

cd /tmp
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.0_amd64.deb
dpkg -i influxdb_1.7.0_amd64.deb


######### install grafana
echo "Install Grafana"
apt-get install -y adduser libfontconfig
wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_5.3.2_amd64.deb
dpkg -i grafana_5.3.2_amd64.deb

######### Install telegrapf
wget https://dl.influxdata.com/telegraf/releases/telegraf_1.8.3-1_amd64.deb
dpkg -i telegraf_1.8.3-1_amd64.deb

######### Install FDB client

# download the dependencies
wget https://www.foundationdb.org/downloads/5.2.5/ubuntu/installers/foundationdb-clients_5.2.5-1_amd64.deb

# server depends on the client packages
dpkg -i foundationdb-clients_5.2.5-1_amd64.deb

######### Cleanup

apt-get clean
rm -rf /var/lib/apt/lists/*
rm -rf /tmp/*
