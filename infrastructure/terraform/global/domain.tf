#resource "aws_route53_zone" "primary" {
#  name = "yallastam.com"
#}
#
#resource "aws_route53_record" "app" {
#  zone_id = aws_route53_zone.primary.zone_id
#  name    = var.domain
#  type    = "A"
#
#  alias {
#    name                   = aws_lb.load_balancer.dns_name
#    zone_id                = aws_lb.load_balancer.zone_id
#    evaluate_target_health = true
#  }
#}