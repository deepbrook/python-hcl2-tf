terraform {
  backend "local" {
    path = "./terraform.tfstate"
    workspace_dir = "./workspaces"
  }
}


terraform {
  required_version = "~>1"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~>1"
    }
  }
}