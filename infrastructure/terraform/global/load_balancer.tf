resource "aws_lb" "load_balancer" {
  name               = "${var.environment_name}-alb"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [aws_security_group.load-balancer.id]
  subnets            = [aws_subnet.public-subnet-1, aws_subnet.public-subnet-2]
}
