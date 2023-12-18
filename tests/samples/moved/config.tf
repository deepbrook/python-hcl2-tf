moved {
  from = local_file.old
  to = local_file.new
}

resource "local_file" "new" {
  filename = "new.txt"
  content = "New and shiny!"
}
