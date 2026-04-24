# JSON Helper

A Linux command-line tool for managing JSON files.

## Operations

| Command | Description |
|---------|-------------|
| `new`   | Create a new empty JSON file |
| `copy`  | Copy a JSON file to a new location |
| `merge` | Merge two JSON files into a third (keys from file2 take precedence) |
| `delete`| Delete a JSON file |

## Requirements

- Python 3.10 or higher
- `pytest >= 7.0` (for running tests)
- `PyInstaller >= 6.0` (for building the executable)

## CI / Build Artifacts

Builds are automated via GitHub Actions. 

- **Pull requests** - runs the test suite and builds the binary to validate the change.
- **Merge to `main`** - runs the test suite, builds the binary, and uploads `dist/json_helper` as a downloadable artifact

The latest artifact can be downloaded from the **Actions** tab in the GitHub repository.

## Local Development Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package with build dependencies (includes pytest and pyinstaller):

```bash
pip install -e .[build]
```

## Testing Locally

Run all tests:

```bash
python -m pytest tests/ -v
```

## Building Locally (Standalone Executable)

Build the executable:

```bash
pyinstaller json_helper.spec
```

The compiled binary will be in:

```
dist/json_helper
```

## Install

After building, copy the binary to a location on your PATH:

```bash
cp dist/json_helper /usr/local/bin/json-helper
```

Or run directly from the `dist/` folder:

```bash
./dist/json_helper
```

## Usage

Show help:

```bash
json-helper -h
json-helper [command] -h
```

Create a new empty JSON file:

```bash
json-helper new output.json
```

Copy a JSON file:

```bash
json-helper copy source.json destination.json
```

Merge two JSON files into a third:

```bash
json-helper merge file1.json file2.json output.json
```

Delete a JSON file:

```bash
json-helper delete target.json
```

## Examples

```bash
$ json-helper new config.json
Created: config.json

$ json-helper copy config.json config_backup.json
Copied: config.json -> config_backup.json

$ json-helper merge defaults.json overrides.json final.json
Merged: defaults.json + overrides.json -> final.json

$ json-helper delete config_backup.json
Deleted: config_backup.json
```
