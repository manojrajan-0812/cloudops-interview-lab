terraform {
  required_version = ">= 1.3"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

resource "random_string" "deploy_id" {
  length  = 8
  special = false
  upper   = false

  keepers = {
    environment = var.environment
  }
}

resource "local_file" "app_config" {
  content  = <<-EOT
    environment=${var.environment}
    version=${var.app_version}
    replicas=${var.replica_count}
    deploy_id=${random_string.deploy_id.result}
  EOT
  filename = "${path.module}/output/app_config.txt"
}

resource "null_resource" "deployment" {
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = "echo 'Deploying version ${var.app_version} to ${var.environment}'"
  }
}
