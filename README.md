# HCL2 Terraform Config Interface

This library offers a Terraform-centric extension to the :mod:`hcl2` library. It's primary use-case is documentation generation in conjunction
with templating engines, such as jinja2.

While Terraform configuration uses the HCL2 spec, it enforces an additional set of rules
for various block types (e.g. such as uniqueness of block labels). the `python-hcl2` library
does not know about this, of course and rightly ignores this rule set.

Given the following tf file:

```hcl
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
```

Accodring to HCL spec, `hcl2.load` parses this configuration as this:

```json
{
 'resource': [
    {
        'local_file': {
            'dump': {
                'filename': 'dump.txt', 'content': "this is my file's contents: ${module.disclose.shout}", 
                'lifecycle': [
                    {'ignore_changes': ['${file_permission}'], 'precondition': [{'condition': '${!var.locked}', 'error_message': 'Cannot update, file is locked!'}], 'postcondition': [{'condition': '${!startswith(var.content, "top-secret")}', 'error_message': 'Cannot store top-secret secrets in dump.txt!'}]}
                ]
            }
        }
    }
 ]}
```
Accessing the resource `local_file.dump` thus requires the following python code:

```python
config = hcl2.loads(pathlib.Path("config.tf").read_text())
config["resource"][0]["local_file"]["dump"]
```

Note that we must *know* that index 0 is the local_file.dump block definition. Block definitions are added to arrays in the order they are read, meaning if another resource definition is added before this one, its index will change, resulting in brittle code.

In `hcl2tf` land, using key-based access, this looks *slightly* leaner and also ends up being more solid:

```python
config = hcl2tf.loads(pathlib.Path("config.tf").read_text())
config
{
 'resource':
    {
        'local_file': {
            'dump': {
                'filename': 'dump.txt', 'content': "this is my file's contents: ${module.disclose.shout}", 
                'lifecycle': {
                    'ignore_changes': ['${file_permission}'],
                    'precondition': [
                        {'condition': '${!var.locked}', 'error_message': 'Cannot update, file is locked!'}
                    ],
                    'postcondition': [
                        {'condition': '${!startswith(var.content, "top-secret")}', 'error_message': 'Cannot store top-secret secrets in dump.txt!'}
                    ]
                }
                
            }
        }
    }
 }
config["resource"]["local_file"]["dump"]
```

A *little* underwhelming, sure. But things get neat when you use config addresses instead of key-based access:

```python
config["local_file.dump"]
```

Since we're in Terraform land, we know that addresses *not* starting with a block type, the address points to a resource. `hcl2tf` knows this, and loads the config from the `resource` definition accordingly.

This is possible due to a small custom dict class. It wraps the compacted configuration  and allows us to look up block definitions using their actual Terraform Configuration address[^1].

[^1]: This excludes block instances, as created in the terraform state when a block definition declares the `count` or `for_each` argument. You *may* pass an address with index of key access, but the instance identifier is ignored. I.e., `aws_s3_bucket.this["someInstance"]` is valid, but will not return instance-specific values, as this library does **not** inspect state.


## Resource and Data Dicts
## Module, Variable, Output
## Check
## Import and Moved
## Terraform
