import {
  to = local_file.imported
  id = "dump.log"
}

resource "local_file" "imported" {
  filename = "dump.log"
  content = "Nothing here."
}
