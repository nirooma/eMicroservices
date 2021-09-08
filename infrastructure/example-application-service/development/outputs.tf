output "load_balancer_dns" {
  value = module.example-application-service.load_balancer_dns
}

output "ecr_url" {
  value = module.example-application-service.ecr_url
}