variable "whisper" {
  type = string
  description = "Tell us something, quietly"
}

output "shout" {
  value = upper(var.whisper)
  description = "Your whispered message, but shouted."
}