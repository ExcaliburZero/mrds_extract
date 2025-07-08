# mrds_extract [![Test](https://github.com/ExcaliburZero/mrds_extract/actions/workflows/test.yml/badge.svg)](https://github.com/ExcaliburZero/mrds_extract/actions/workflows/test.yml) [![Maintainability](https://qlty.sh/gh/ExcaliburZero/projects/mrds_extract/maintainability.svg)](https://qlty.sh/gh/ExcaliburZero/projects/mrds_extract)

`mrds_extract` is a set of tools for extracting data from and working with save data for the Nintendo DS game Monster Rancher DS.

## Tools

- `mrds-extract-save` - Converts a `*.sav` save file to a (mostly) human-readable JSON file.
- `mrds-fix-save-checksums` - Fixes the checksums of a modified save file to get the game to not detect it as corrupted.

## Usage

### mrds-extract-save

```console
$ mrds-extract-save --save_file '.\tests\data\save_files\5160 - Monster Rancher DS (U)(Independent) - 01 - After returning to ranch.sav'
```

### mrds-extract-save

```console
$ mrds-fix-save-checksums '.\tests\data\save_files\5160 - Monster Rancher DS (U)(Independent) - 01 - After returning to ranch.sav'
INFO> All checksums are already correct.
INFO> Wrote updated save file to: tests\data\save_files\5160 - Monster Rancher DS (U)(Independent) - 01 - After returning to ranch.sav
$ mrds-fix-save-checksums '.\tests\data\save_files_edited\5160 - Monster Rancher DS (U)(Independent) - 01 - After returning to ranch.sav'
INFO> Updated checksums:
INFO>   1st header checksum from 0xba4928f9 to 0xa7029e13
INFO>   1st body   checksum from 0x47d25c5d to 0x0015d247
INFO> Wrote updated save file to: tests\data\save_files_edited\5160 - Monster Rancher DS (U)(Independent) - 01 - After returning to ranch.sav
```

## Development

### Installation

```bash
uv run pip install -e .[test]
```

### Formatting

```bash
uv run task format
```

### Linting

```bash
uv run task lint
```

### Testing

```bash
uv run task test
```
