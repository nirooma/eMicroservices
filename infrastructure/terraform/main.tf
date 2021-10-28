module "global" {
  source = "./global"

  environment_name = var.environment_name
}

module "eMicroservices" {
  source = "./modules/eMicroservices"

  environment_name      = var.environment_name
  ecs_security_group_id = module.global.ecs_security_group_id
  private_subnet_1_id   = module.global.private_subnet_1_id
  private_subnet_2_id   = module.global.private_subnet_2_id
}