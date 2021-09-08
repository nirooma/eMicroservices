variable "prefix" {
  default = "genesis"
}

variable "project" {
  default = "genesis-project"
}

variable "contact" {
  default = "nirooma@icloud.com"
}

variable "phone" {
  default = "+9725094111171"
}



variable "region" {
  description = "The AWS region to create resources in."
  default     = "eu-central-1"
}

variable "vpc_state_username" {
  type = string
  description = "Username to access VPC's terraform state"
}
variable "vpc_state_password" {
  type = string
  sensitive = true
  description = "Password to access VPC's terraform state"
}