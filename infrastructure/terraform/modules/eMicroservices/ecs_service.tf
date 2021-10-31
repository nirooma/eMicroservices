data "template_file" "app" {
  template = file("modules/eMicroservices/containers.json.tpl")
  vars = {
    aws_cloudwatch_log_group              = aws_cloudwatch_log_group.gen-log-group.name
    aws_cloudwatch_log_stream_nginx       = aws_cloudwatch_log_stream.nginx-log-stream.name
    aws_cloudwatch_log_stream_splinter    = aws_cloudwatch_log_stream.splinter-log-stream.name
    aws_cloudwatch_log_stream_rabbitmq    = aws_cloudwatch_log_stream.rabbitmq-log-stream.name
    aws_cloudwatch_log_stream_leonardo-db = aws_cloudwatch_log_stream.leonardo-db-log-stream.name
    aws_cloudwatch_log_stream_leonardo    = aws_cloudwatch_log_stream.leonardo-log-stream.name

  }
}


resource "aws_ecs_task_definition" "app" {
  family                = "${var.environment_name}-app"
  container_definitions = data.template_file.app.rendered
  
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