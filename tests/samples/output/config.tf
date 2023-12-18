
output "foo" {
  value = "hello"
  description = "Our chosen word of greeting."
}

output "bar" {
  value = "world"
  description = "Our greeting's target audience."
  sensitive = true
}
