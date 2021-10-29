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
        },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "${aws_cloudwatch_log_group.nginx-log-group.name}",
          "awslogs-region": "eu-central-1",
          "awslogs-stream-prefix": "${aws_cloudwatch_log_stream.nginx-log-stream.name}"
        }
      }
    }
]
EOF
  lifecycle {
    ignore_changes = all
  }
}

resource "aws_ecs_service" "eMicroservices-service" {
  name            = var.environment_name
  cluster         = aws_ecs_cluster.eMicroservices-cluster.name
  task_definition = aws_ecs_task_definition.nginx.family
  iam_role        = aws_iam_role.ecs-service-role.arn
  desired_count   = 1
  deployment_minimum_healthy_percent = 50

  load_balancer {
    target_group_arn = var.aws_alb_target_group_arn
    container_name   = "nginx"
    container_port   = 80
  }
  depends_on = [var.ecs_alb_http_listener]

  lifecycle {
    ignore_changes = [task_definition]
  }
}