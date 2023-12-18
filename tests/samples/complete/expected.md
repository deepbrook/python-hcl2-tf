# This is the module header's Heading!

Here's some text! And here to!

New paragraph!

> Markdown quotes!

**And** fancy *formatting*!

## Requirements

Terraform: **`~>1`**

|Provider|Version|Source|
|---|---|---|
|aws|`~>1`|[Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)|

## Backend `local`

|Attribute|Value|
|---|---|
|path|./terraform.state|


## Input Variables

### `locked`
Declare the file locked and prevent TF from applying changes.

|Attribute|Value|
|---|---|
|**Required**|`false`|
|**Type**|`bool`|
|**Default**|`false`|

### `content`
Content to publish in the dump file.

|Attribute|Value|
|---|---|
|**Required**|`true`|
|**Type**|`string`|
|**Sensitive**|`true`|


## Resources

### `local_file.dump`

Source: `config.tf::local_file.dump`

Preconditions:

- if not `!var.locked`: Cannot update, file is locked!
- if not `!startswith(var.content, "top-secret")`: Cannot store top-secret secrets in dump.txt!

Postconditions:

- None

### `local_file.log`

Source: `config.tf::local_file.log`

