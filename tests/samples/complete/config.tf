/*# This is the module header's Heading!

Here's some text! And here to!

New paragraph!

> Markdown quotes!

**And** fancy *formatting*!
*/

terraform {
  backend "local" {
    path = "./terraform.state"
    
  }
}

variable "locked" {
  type    = bool
  default = false
  description = "Declare the file locked and prevent TF from applying changes."
}

variable "content" {
  type = string
  description = "Content to publish in the dump file."
  sensitive = true
}

locals {
  something = "entirely unrelated"
}

locals {
  another ="thing, unmentioned"
}

locals {
  today = timestamp()
}

check "file_only_accessible_by_me" {
  assert {
    condition = formatdate("EEE",local.today) != "Fri"
    error_message = "OMG! WARNING! Do NOT deploy on a Friday!"
  }

}

module "disclose" {
  source = "./modules/shout"
  whisper = var.content
}

moved {
  from = local_file.old_dump
  to = local_file.dump
}

resource "local_file" "dump" {
  filename = "dump.txt"
  content = "this is my file's contents: ${module.disclose.shout}"

  lifecycle {
    ignore_changes = [ file_permission ]

    precondition {
      condition = !var.locked
      error_message = "Cannot update, file is locked!"
    }

    precondition {
      condition = !startswith(var.content, "top-secret")
      error_message = "Cannot store top-secret secrets in dump.txt!"
    }
  }
}

resource "local_file" "log" {
  filename = "log.txt"
  content = "Updated dump to ${module.disclose.shout}"
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

/*
# This is the module footer's Heading!

Here's some text! And here to!

New paragraph!

> Markdown quotes!

**And** fancy *formatting*!
*/