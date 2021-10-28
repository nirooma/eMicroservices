resource "aws_lb" "load_balancer" {
  name               = "production-alb"
  load_balancer_type = "application"
  internal           = false
#  security_groups    = [var.load_balancer_security_group_id]
  security_groups    = [aws_security_group.load-balancer.id]
  subnets            = [aws_subnet.public-subnet-1.id, aws_subnet.public-subnet-2.id]
}

