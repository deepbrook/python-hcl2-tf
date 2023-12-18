
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
