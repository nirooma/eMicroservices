resource "aws_lb" "load_balancer" {
  name               = "${var.environment_name}-alb"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [aws_security_group.load-balancer.id]
  subnets            = [aws_subnet.public-subnet-1.id, aws_subnet.public-subnet-2.id]
}

resource "aws_alb_target_group" "default-target-group" {
  name       = "${var.environment_name}-nginx-tg"
  port       = 80
  protocol   = "HTTP"
  vpc_id     = aws_vpc.eMicroservices-vpc.id
  depends_on = [aws_lb.load_balancer]
}

# Listener (redirects traffic from the load balancer to the target group)
resource "aws_alb_listener" "ecs-alb-http-listener" {
  load_balancer_arn = aws_lb.load_balancer.id
  port              = "80"
  protocol          = "HTTP"
  depends_on        = [aws_alb_target_group.default-target-group]

  default_action {
    type             = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_alb_listener" "ecs-alb-https-listener" {
  load_balancer_arn = aws_lb.load_balancer.id
  port              = "443"
  protocol          = "HTTPS"
  depends_on        = [aws_alb_target_group.default-target-group]

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.default-target-group.arn
  }
  certificate_arn = "arn:aws:acm:eu-central-1:096061951195:certificate/c5060715-587d-4045-bd0d-b438b9551801"
}