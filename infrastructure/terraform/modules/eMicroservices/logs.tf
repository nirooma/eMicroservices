resource "aws_cloudwatch_log_group" "nginx-log-group" {
  name              = "/ecs/${var.environment_name}/nginx"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_stream" "nginx-log-stream" {
  name           = "${var.environment_name}-nginx-log-stream"
  log_group_name = aws_cloudwatch_log_group.nginx-log-group.name
}

resource "aws_cloudwatch_log_group" "splinter-log-group" {
  name              = "/ecs/${var.environment_name}/spllnter"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_stream" "splinter-log-stream" {
  name           = "${var.environment_name}-splinter-log-stream"
  log_group_name = aws_cloudwatch_log_group.nginx-log-group.name
}