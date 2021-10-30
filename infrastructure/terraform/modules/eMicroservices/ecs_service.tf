resource "aws_ecs_task_definition" "app" {
  family                = "${var.environment_name}-app"
  container_definitions = <<EOF
[
   {
      "name":"leonardo",
      "image":"nirooma/leonardo:latest",
      "cpu":500,
      "command":[
         "daphne",
         "--bind",
         "0.0.0.0",
         "--port",
         "8002",
         "core.asgi:application"
      ],
      "memory":500,
      "links":[],
      "essential":true,
      "environment":[
         {
            "name":"SQL_ENGINE",
            "value":"django.db.backends.postgresql"
         },
         {
            "name":"SQL_DATABASE",
            "value":"fastapi"
         },
         {
            "name":"SQL_USER",
            "value":"postgres"
         },
         {
            "name":"SQL_PASSWORD",
            "value":"postgres"
         },
         {
            "name":"SQL_HOST",
            "value":"leonardo-db"
         },
         {
            "name":"SQL_PORT",
            "value":"5432"
         }
      ],
      "portMappings":[
         {
            "containerPort":8002
         }
      ],
      "logConfiguration":{
         "logDriver":"awslogs",
         "options":{
            "awslogs-group":"${aws_cloudwatch_log_group.gen-log-group.name}",
            "awslogs-region":"eu-central-1",
            "awslogs-stream-prefix":"${aws_cloudwatch_log_stream.leonardo-log-stream.name}"
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
  name                               = var.environment_name
  cluster                            = aws_ecs_cluster.eMicroservices-cluster.name
  task_definition                    = aws_ecs_task_definition.app.family
  iam_role                           = aws_iam_role.ecs-service-role.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 50

  load_balancer {
    target_group_arn = var.aws_alb_target_group_arn
    container_name   = "leonardo" # Change back to nginx
    container_port   = 8002 # Change back to 80
  }
  depends_on = [var.ecs_alb_http_listener]

  lifecycle {
    ignore_changes = [task_definition]
  }
}