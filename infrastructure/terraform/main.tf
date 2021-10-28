terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.6"
    }
  }
  required_version = "1.0.9"
}

provider "aws" {
  region = var.region_name
}

resource "aws_instance" "app_server" {
  ami           = var.instance_ami
  instance_type = var.instance_type
  key_name = "frankfurt"

  tags = {
    Name = "ExampleAppServerInstance"
  }
}