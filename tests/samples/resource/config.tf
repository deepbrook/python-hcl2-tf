variable "content" {
  type = string
}

variable "locked" {
  type = bool
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

    postcondition {
      condition = !startswith(var.content, "top-secret")
      error_message = "Cannot store top-secret secrets in dump.txt!"
    }
  }
}

resource "local_file" "log" {
  filename = "log.txt"
  content = "Updated dump to ${module.disclose.shout}"
}
