####### Cluster options ####

# instance store options: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html
# m5d.2xlarge - will use local NVMe SSD
variable "aws_fdb_size" {
  default = "m5d.xlarge"
  description = "machine type to run FoundationDB servers"
}

variable "fdb_procs_per_machine" {
  default = 4
  description = "number of FDB processes per machine"
}
variable "aws_fdb_count" {
  default = 4
  description = "Number of machines in a cluster"
}

# Configure section for influx+grafana instance

variable "aws_influxdb_size" {
  default = "t2.medium"
  description = "machine type to run Grafana servers"
}

variable "aws_influxdb_count" {
  default = 1
  description = "Number of machine for Grafana server, this is limited to 0 or 1"
}

variable "aws_grafana_password" {
  default = "password"
  description = "Default password for admin user to login"
}

# Configure section for tester instance

variable "aws_tester_count" {
  # make sure there are enough testers so that they 
  # are not saturated (cpu < 100%) to get accurate results
  default = 1
  description = "Number of tester machines in a cluster"
}
variable "fdb_init_string" {
  default = "configure new ssd single proxies=4 resolvers=2 logs=4"
  description = "FDB initialization string"
}

####### Misc options #######

# todo maybe just use the default ssh key?
variable "public_key_path" {
  description = "Path to the SSH public key to be used for authentication."
  default = "~/.ssh/terraform.pub"
}
variable "private_key_path" {
  description = "Path to the SSH private key"
  default = "~/.ssh/terraform"
}
variable "key_name" {
   default = "terraform"
}
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_region" {
  default = "ap-northeast-1"
  description = "AWS region to launch servers."
}
variable "aws_availability_zone" {
  default = "ap-northeast-1a"
}
