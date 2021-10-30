variable "environment_name" {
  description = "Name of app environment. Must be unique."
  type        = string
}
variable "ecs_security_group_id" {
  type = string
}
variable "instance_type" {
  type    = string
  default = "t2.2xlarge"
}
variable "autoscaling_min" {
  default = 1
}
variable "autoscaling_max" {
  default = 3
}
variable "autoscaling_desired" {
  default = 1
}
variable "private_subnet_1_id" {
  type = string
}
variable "private_subnet_2_id" {
  type = string
}
variable "aws_alb_target_group_arn" {
  type = string
}
variable "ecs_alb_http_listener" {}