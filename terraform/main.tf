terraform {
  required_version = ">= 1.0.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

# -----------------------------------------------------------
# Step 1: Build Docker Image using shell command
# This avoids the Terraform docker provider's known issues
# with spaces in paths and tar archiving.
# -----------------------------------------------------------
resource "null_resource" "build_image" {
  # Re-build whenever source files change
  triggers = {
    dockerfile_hash = filemd5("${path.module}/../Dockerfile")
    main_py_hash    = filemd5("${path.module}/../src/main.py")
    requirements    = filemd5("${path.module}/../requirements.txt")
  }

  provisioner "local-exec" {
    working_dir = "${path.module}/.."
    command     = "docker build -t iot-devops-api:latest ."
  }
}

# -----------------------------------------------------------
# Step 2: Reference the built image
# -----------------------------------------------------------
data "docker_image" "iot_app_image" {
  name = "iot-devops-api:latest"

  depends_on = [null_resource.build_image]
}

# -----------------------------------------------------------
# Step 3: Create Docker Network
# -----------------------------------------------------------
resource "docker_network" "private_network" {
  name = "iot_devops_network"
}

# -----------------------------------------------------------
# Step 4: Run Docker Container
# -----------------------------------------------------------
resource "docker_container" "iot_app_container" {
  name  = "iot-devops-api-service"
  image = data.docker_image.iot_app_image.name

  ports {
    internal = 8000
    external = 8000
  }

  networks_advanced {
    name = docker_network.private_network.name
  }

  env = [
    "ENV=local",
    "API_VERSION=1.0.0"
  ]

  restart = "on-failure"

  depends_on = [null_resource.build_image]
}

# -----------------------------------------------------------
# Outputs
# -----------------------------------------------------------
output "app_url" {
  value       = "http://localhost:8000"
  description = "The URL of the local running API"
}

output "telemetry_endpoint" {
  value       = "http://localhost:8000/telemetry"
  description = "The telemetry endpoint for API testing"
}
