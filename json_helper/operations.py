import json
import shutil
from pathlib import Path


def create_file(path: str) -> None:
    """Create a new empty JSON file at *path*. Raises FileExistsError if it already exists."""
    print(f"Creating new file: {path}")
    target = Path(path)
    if target.exists():
        raise FileExistsError(f"{path} already exists")
    try:
        target.write_text(json.dumps({}, indent=2) + "\n", encoding="utf-8")
    except OSError as e:
        raise OSError(f"Unable to create {path}: {e.strerror}") from e
    print(f"Created: {path}")


def copy_file(source: str, dest: str) -> None:
    """Copy a JSON file to a new location."""
    src = Path(source)
    print(f"Copying files: {source} -> {dest}")
    if not src.exists():
        raise FileNotFoundError(f"{source} not found")
    try:
        shutil.copy(src, dest)
    except OSError as e:
        raise OSError(f"Unable to copy {source} to {dest}: {e.strerror}") from e
    print(f"Copied: {source} -> {dest}")


def merge_files(file1: str, file2: str, output: str) -> None:
    """Merge two JSON objects into a third file. Keys from file2 take precedence."""
    print(f"Merging files: {file1} and {file2} into {output}")
    for path in (file1, file2):
        if not Path(path).exists():
            raise FileNotFoundError(f"{path} not found")
    data1 = json.loads(Path(file1).read_text(encoding="utf-8"))
    data2 = json.loads(Path(file2).read_text(encoding="utf-8"))
    merged = {**data1, **data2}
    try:
        Path(output).write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    except OSError as e:
        raise OSError(f"Unable to write {output}: {e.strerror}") from e
    print(f"Merged: {file1} + {file2} -> {output}")


def delete_file(path: str) -> None:
    """Delete a JSON file."""
    print(f"Deleting file: {path}")
    target = Path(path)
    if not target.exists():
        raise FileNotFoundError(f"{path} not found")
    try:
        target.unlink()
    except OSError as e:
        raise OSError(f"Unable to delete {path}: {e.strerror}") from e
    print(f"Deleted: {path}")
