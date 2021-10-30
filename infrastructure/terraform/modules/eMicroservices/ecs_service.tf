resource "aws_ecs_task_definition" "app" {
  family = "${var.environment_name}-app"
  container_definitions = <<EOF
[
   {
      "name":"leonardo",
      "image":"nirooma/leonardo:latest",
      "cpu":10,
      "command":[
         "daphne",
         "--bind",
         "0.0.0.0",
         "--port",
         "8002",
         "core.asgi:application"
      ],
      "memory":512,
      "links":[
         "leonardo-db",
         "rabbitmq"
      ],
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
      "mountPoints":[
         {
            "containerPath":"/opt/leonardo/staticfiles",
            "sourceVolume":"static_volume"
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
   },
   {
      "name":"leonardo-db",
      "image":"postgres:13.4-alpine",
      "cpu":10,
      "memory":256,
      "essential":true,
      "environment":[
         {
            "name":"POSTGRES_DB",
            "value":"fastapi"
         },
         {
            "name":"POSTGRES_USER",
            "value":"postgres"
         },
         {
            "name":"POSTGRES_PASSWORD",
            "value":"postgres"
         }
      ],
      "logConfiguration":{
         "logDriver":"awslogs",
         "options":{
            "awslogs-group":"${aws_cloudwatch_log_group.gen-log-group.name}",
            "awslogs-region":"eu-central-1",
            "awslogs-stream-prefix":"${aws_cloudwatch_log_stream.leonardo-db-log-stream.name}"
         }
      }
   },
   {
      "name":"rabbitmq",
      "image":"rabbitmq:3.9.4-management",
      "cpu":10,
      "memory":256,
      "essential":true,
      "environment":[

      ],
      "logConfiguration":{
         "logDriver":"awslogs",
         "options":{
            "awslogs-group":"${aws_cloudwatch_log_group.gen-log-group.name}",
            "awslogs-region":"eu-central-1",
            "awslogs-stream-prefix":"${aws_cloudwatch_log_stream.rabbitmq-log-stream.name}"
         }
      }
   },
   {
      "name":"splinter",
      "image":"nirooma/splinter:latest",
      "cpu":10,
      "command":[
         "yarn",
         "start"
      ],
      "memory":128,
      "essential":true,
      "environment":[

      ],
      "portMappings":[
         {
            "containerPort":3000
         }
      ],
      "logConfiguration":{
         "logDriver":"awslogs",
         "options":{
            "awslogs-group":"${aws_cloudwatch_log_group.gen-log-group.name}",
            "awslogs-region":"eu-central-1",
            "awslogs-stream-prefix":"${aws_cloudwatch_log_stream.splinter-log-stream.name}"
         }
      }
   },
   {
      "name":"nginx",
      "image":"nirooma/nginx:latest",
      "cpu":10,
      "memory":128,
      "links":[
         "splinter",
         "leonardo",
         "rabbitmq"
      ],
      "essential":true,
      "environment":[

      ],
      "portMappings":[
         {
            "containerPort":80
         },
         {
            "containerPort":15672
         }
      ],
      "mountPoints":[
         {
            "containerPath":"/opt/leonardo/staticfiles",
            "sourceVolume":"static_volume"
         }
      ],
      "logConfiguration":{
         "logDriver":"awslogs",
         "options":{
            "awslogs-group":"${aws_cloudwatch_log_group.gen-log-group.name}",
            "awslogs-region":"eu-central-1",
            "awslogs-stream-prefix":"${aws_cloudwatch_log_stream.nginx-log-stream.name}"
         }
      }
   }
]
EOF
  volume {
    name      = "static_volume"
    host_path = "/opt/leonardo/staticfiles/"
  }
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
    container_name   = "nginx"
    container_port   = 80
  }
  depends_on = [var.ecs_alb_http_listener]

  lifecycle {
    ignore_changes = [task_definition]
  }
}