resource "aws_lb" "load_balancer" {
  name               = "${var.environment_name}-alb"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [var.load_balancer_security_group_id]
  subnets            = [var.public_subnet_1_id, var.public_subnet_2_id]
}

