variable "region" {
  description = "The region of your infrastructure"
  type = string
  default = "us-east-1"
}

variable "az-list" {
  description = "The list of AZs associated with a specific region, used for HA purpose"
  type = list(string)
  default = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "name-prefix" {
  description = "The name prefix for better resources management, format <p/s/d>:<region_code>"
  type = string
  default = "pue1"
}

### Networking variables

variable "vpc-main-cidr" {
  description = "Main CIDR for VPC"
  type = string
  default = "10.0.0.0/16"
}

variable "public-subnet-cidr" {
  description = "CIDR for public subnets based on VPC's CIDR"
  type = list(string)
  default = ["10.0.10.0/24", "10.0.10.20.0/24", "10.0.30.0/24"]
}

variable "private-subnet-cidr" {
  description = "CIDR for private subnets based on VPC's CIDR"
  type = list(string)
  default = ["10.0.11.0/24", "10.0.21.0/24", "10.0.31.0/24"]
}

variable "database-subnet-cidr" {
  description = "CIDR for database resouces based on VPC's CIDR"
  type = list(string)
  default = ["10.0.12.0/24", "10.0.22.0/24", "10.0.32.0/24"]
}
