# networking
variable "public_subnet_1_cidr" {
  description = "CIDR Block for Public Subnet 1"
  default     = "10.0.1.0/24"
}
variable "public_subnet_2_cidr" {
  description = "CIDR Block for Public Subnet 2"
  default     = "10.0.2.0/24"
}
variable "private_subnet_1_cidr" {
  description = "CIDR Block for Private Subnet 1"
  default     = "10.0.3.0/24"
}
variable "private_subnet_2_cidr" {
  description = "CIDR Block for Private Subnet 2"
  default     = "10.0.4.0/24"
}
variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["eu-central-1a", "eu-central-1b"]
}

######## load balancer ###########
############################
variable "vpc_id" {
  description = "ID od VPC"
  type = string
}

variable "environment_name" {
  description = "Name of app environment. Must be unique."
  type = string
}

variable "load_balancer_security_group_id" {
  description = "ID of ALB security group"
  type = string
}

variable "public_subnet_1_id" {
  description = "Id of first public subnet"
  type = string
}

variable "public_subnet_2_id" {
  description = "Id of second public subnet"
  type = string
}