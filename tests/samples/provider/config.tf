provider "aws" {
    region = "eu-central-1"
    access_key = "my-secret-access-key"
    default_tags {  # note that this will be a list of objects, despite it not making much sense. Thats a provider issue, tho, not a pterradoctyl issue.
      tags = { "managed-by": "terraform"}
    }
}
