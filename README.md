# generate\_erd.py

## Introduction

This is a simple Python 3 script for generating ER diagrams from an SQLite
database file. 

## Formatters

Currently there are two formatters pre-packaged. `dot` and `latex`. Both of them
are styled for my personal tastes but if you dislike them they are easy to
change.

### Adding and customising formatters

The script dynamically loads the formatter at runtime. This means your custom
formatter file must meet the following:

1. Must be in python path (easiest way is putting it in the same directory as
   the script)
2. Must have a function `format_erd`

The signature of `format_erd` must be:

```python
def format_erd(tables: [DBTable], links: [DBLink], out) -> None:
```

Note that `DBTable` and `DBLink` will not be defined unless you add them
yourself (the type hints are not mandatory). You can inspect the code of
`generate_erd.py` to see the fields of these. `out` is a callable of undefined
type that has the signature `(str) -> Any` (it will likely be `print`, but this
is left open as a customisation point)


## Usage

```bash
generate_erd.py <sqlite database file> -f <name of formatter>
```


## License 

This project is licensed under the MIT license. See LICENSE for more
information.

