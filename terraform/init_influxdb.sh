#!/bin/bash
set -e

VM_TYPE=$1
SELF_IP=$2
SEED_IP=$3
FDB_CLUSTER=$4
FDB_INIT_STRING=$5
GRAFANA_PASSWORD=$6

update_password_data()
{
  cat <<EOF
{
  "oldPassword": "admin",
  "newPassword": "${GRAFANA_PASSWORD}",
  "confirmNew": "${GRAFANA_PASSWORD}"
}
EOF
}

echo "./init.sh $@"

# resolve IP address as host name
echo "$SELF_IP $(hostname)" >> /etc/hosts

# make 1st node the coordinator
echo "$FDB_CLUSTER" > /etc/foundationdb/fdb.cluster

# ensure the correct permissions
chown -R foundationdb:foundationdb /etc/foundationdb
chmod -R ug+w /etc/foundationdb

# make sure the cluster file is writeable by everybody
chmod o+w /etc/foundationdb/fdb.cluster

# Start influxdb service
service influxdb start

# Start grafana service
service grafana-server start

sleep 4 # make sure the service has started

# Change default user name and password
curl -X PUT -H "Content-Type: application/json" -d "$(update_password_data)" http://admin:admin@localhost:3000/api/user/password

# Add default data source of influxdb for grafana

curl "http://admin:${GRAFANA_PASSWORD}@localhost:3000/api/datasources" -X POST -H 'Content-Type: application/json;charset=UTF-8' --data-binary '{"name":"FoundationdbCluster","type":"influxdb","url":"http://localhost:8086","access":"proxy","isDefault":true,"database":"telegraf"}'

# Add dashboard for foundationdb cluster
cp /tmp/dashboards.yaml /etc/grafana/provisioning/dashboards/dashboards.yaml
mkdir /var/lib/grafana/dashboards
# Add dashboard file into dashboard folder
cp /tmp/dashboard_template.json /var/lib/grafana/dashboards/dashboard_template.json


# Copy status converter to user folder
cp /tmp/status_converter.py /etc/telegraf/status_converter.py
chmod +x /etc/telegraf/status_converter.py

# Copy telegraf config file to /etc folder and restart
cp /tmp/telegraf.conf /etc/telegraf/telegraf.conf
service telegraf restart

# Restart grafana server
service grafana-server restart
