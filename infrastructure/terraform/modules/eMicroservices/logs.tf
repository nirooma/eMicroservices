resource "aws_cloudwatch_log_group" "gen-log-group" {
  name              = "/ecs/${var.environment_name}"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_stream" "nginx-log-stream" {
  name           = "${var.environment_name}-nginx"
  log_group_name = aws_cloudwatch_log_group.gen-log-group.name
}

resource "aws_cloudwatch_log_stream" "splinter-log-stream" {
  name           = "${var.environment_name}-splinter"
  log_group_name = aws_cloudwatch_log_group.gen-log-group.name
}

resource "aws_cloudwatch_log_stream" "leonardo-log-stream" {
  name           = "${var.environment_name}-leonardo"
  log_group_name = aws_cloudwatch_log_group.gen-log-group.name
}

resource "aws_cloudwatch_log_stream" "leonardo-db-log-stream" {
  name           = "${var.environment_name}-leonardo-db"
  log_group_name = aws_cloudwatch_log_group.gen-log-group.name
}
resource "aws_cloudwatch_log_stream" "rabbitmq-log-stream" {
  name           = "${var.environment_name}-rabbitmq"
  log_group_name = aws_cloudwatch_log_group.gen-log-group.name
}