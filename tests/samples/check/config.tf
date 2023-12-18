check "today_is_not_friday" {
  assert {
    condition = formatdate("EEE", timestamp()) != "Fri"
    error_message = "OMG! WARNING! Do NOT deploy on a Friday!"
  }
}

check "someone_said_hello" {
  data "external" "hello_world" {
    program = ["echo", jsonencode({message="Someone says hello!"})]
  }
  
  assert {
    condition = data.external.hello_world.result.message == "Someone says hello!"
    error_message = "Nobody said hello :(!"
  }
}
