resource "aws_lb" "load_balancer" {
  name               = "production-alb"
  load_balancer_type = "application"
  internal           = false
#  security_groups    = [var.load_balancer_security_group_id]
  security_groups    = [aws_security_group.load-balancer.id]
  subnets            = [aws_subnet.public-subnet-1.id, aws_subnet.public-subnet-2.id]
}

# Target group client
resource "aws_alb_target_group" "default-target-group" {
  name     = "production-client-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.eMicroservices-vpc.id
  depends_on = [aws_lb.load_balancer]

#  health_check {
#    path                = "/health-check/"
#    port                = "traffic-port"
#    healthy_threshold   = 2
#    unhealthy_threshold = 2
#    timeout             = 2
#    interval            = 5
#    matcher             = "200"
#  }
}