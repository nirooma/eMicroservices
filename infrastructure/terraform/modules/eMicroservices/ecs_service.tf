resource "aws_ecs_task_definition" "nginx" {
  family                = "${var.environment_name}-nginx"
  container_definitions = <<EOF
[
    {
      "name": "nginx",
      "image": "nirooma/nginx:latest",
      "cpu": 1000,
      "memory": 950,
      "essential": true,
      "environment": [],
      "portMappings": [
        {
          "containerPort": 80
        }
      ]
    }
]
EOF
  lifecycle {
    ignore_changes = all
  }
}

#resource "aws_ecs_service" "talk-booking-service" {
#  name            = var.environment_name
#  cluster         = aws_ecs_cluster.eMicroservices-cluster.name
#  task_definition = aws_ecs_task_definition.tommy.family
#  iam_role        = aws_iam_role.ecs-service-role.arn
#  desired_count   = 1
#  deployment_minimum_healthy_percent = 50
#
#  load_balancer {
#    target_group_arn = aws_alb_target_group.default-target-group.arn
#    container_name   = "talk-booking-app"
#    container_port   = var.container_port
#  }
#  depends_on = [aws_alb_listener.ecs-alb-http-listener]
#
#  lifecycle {
#    ignore_changes = [task_definition]
#  }
#}