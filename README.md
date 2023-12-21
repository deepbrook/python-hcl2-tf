# HCL2 Terraform Config Interface

This library offers a Terraform-centric extension to the :mod:`hcl2` library. It's primary use-case is documentation generation in conjunction
with templating engines, such as jinja2.

While Terraform configuration uses the HCL2 spec, it enforces an additional set of rules
for various block types (e.g. such as uniqueness of block labels). the `python-hcl2` library
does not know about this, of course, and rightly ignores this rule set.

## Usage Example

Load a configuration file from [tests/samples](tests/samples):

```python
>>>import hcl2tf, pathlib
>>>config_tf = pathlib.Path.cwd().joinpath("tests", "samples", "complete", "config.tf").read_text()
>>>config = hcl2tf.loads(config_tf)
>>>config
{
    "terraform": {
        "backend": {
            "type": "local",
            "path": "./terraform.state"
        },
        "required_version": "~>1",
        "required_providers": {
            "aws": {
                "source": "hashicorp/aws",
                "version": "~>1"
            }
        }
    },
    "variable": {
        "locked": {
            "type": "${bool}",
            "default": false,
            "description": "Declare the file locked and prevent TF from applying changes."
        },
        "content": {
            "type": "${string}",
            "description": "Content to publish in the dump file.",
            "sensitive": true
        }
    },
    "locals": {
        "something": "entirely unrelated",
        "another": "thing, unmentioned",
        "today": "${timestamp()}"
    },
    "check": {
        "file_only_accessible_by_me": {
            "assert": [
                {
                    "condition": "${formatdate(\"EEE\", local.today) != \"Fri\"}",
                    "error_message": "OMG! WARNING! Do NOT deploy on a Friday!"
                }
            ]
        }
    },
    "module": {
        "disclose": {
            "source": "./modules/shout",
            "whisper": "${var.content}"
        }
    },
    "moved": {
        "${local_file.dump}": "${local_file.old_dump}"
    },
    "resource": {
        "local_file": {
            "dump": {
                "filename": "dump.txt",
                "content": "this is my file's contents: ${module.disclose.shout}",
                "lifecycle": {
                    "ignore_changes": [
                        "${file_permission}"
                    ],
                    "precondition": [
                        {
                            "condition": "${!var.locked}",
                            "error_message": "Cannot update, file is locked!"
                        },
                        {
                            "condition": "${!startswith(var.content, \"top-secret\")}",
                            "error_message": "Cannot store top-secret secrets in dump.txt!"
                        }
                    ]
                }
            },
            "log": {
                "filename": "log.txt",
                "content": "Updated dump to ${module.disclose.shout}"
            }
        }
    },
    "data": {},
    "output": {},
    "provider": {},
    "import": {}
}
```

The returned `AddressableDict` instance implements a superset of all regular `dict` methods, in addition to the possibility of looking up block definitions using their configuration address:


```python
>>>config["variable"]
{
    "locked": {
        "type": "${bool}",
        "default": false,
        "description": "Declare the file locked and prevent TF from applying changes."
    },
    "content": {
        "type": "${string}",
        "description": "Content to publish in the dump file.",
        "sensitive": true
    }
}
>>>config.get("import")
{}
# hcl2tf is smart enough to detect resource addresses do not have a block type prepended
# so you can plug in any valid state address for data and resource block definitions as a 'key'.
>>>config["local_file.dump"]
{
    "filename": "dump.txt",
    "content": "this is my file's contents: ${module.disclose.shout}",
    "lifecycle": {
        "ignore_changes": [
            "${file_permission}"
        ],
        "precondition": [
            {
                "condition": "${!var.locked}",
                "error_message": "Cannot update, file is locked!"
            },
            {
                "condition": "${!startswith(var.content, \"top-secret\")}",
                "error_message": "Cannot store top-secret secrets in dump.txt!"
            }
        ]
    }
}
```



## Resource and Data Dicts
## Module, Variable, Output
## Check
## Import and Moved
## Terraform
