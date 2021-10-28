module "global" {
  source = "./global"

  environment_name = var.environment_name
}

module "eMicroservices" {
  source = "./modules/eMicroservices"

  environment_name = var.environment_name
}