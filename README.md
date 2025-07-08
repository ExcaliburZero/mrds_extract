# mrds_extract [![Test](https://github.com/ExcaliburZero/mrds_extract/actions/workflows/test.yml/badge.svg)](https://github.com/ExcaliburZero/mrds_extract/actions/workflows/test.yml) [![Maintainability](https://qlty.sh/gh/ExcaliburZero/projects/mrds_extract/maintainability.svg)](https://qlty.sh/gh/ExcaliburZero/projects/mrds_extract)

`mrds_extract` is a set of tools for extracting data from and working with save data for the Nintendo DS game Monster Rancher DS.

## Tools
* `mrds-extract-save` - Converts a `*.sav` save file to a (mostly) human-readable JSON file.
* `mrds-fix-save-checksums` - Fixes the checksums of a modified save file to get the game to not detect it as corrupted.

## Development

### Installation

```bash
uv run pip install -e .[test]
```

### Linting

```bash
uv run task lint
```
