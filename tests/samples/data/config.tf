data "external" "with_lifecycle" {
  program = ["echo", jsonencode({message="hello world"})]

  lifecycle {
    precondition {
      condition = true
      error_message = "Cannot update, file is locked!"
    }

    postcondition {
      condition = true
      error_message = "Cannot store top-secret secrets in dump.txt!"
    }
  }
}

data "external" "without_lifecycle" {
  program = ["echo", jsonencode({message="hello world"})]
}
