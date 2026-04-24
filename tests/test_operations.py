import json
import os
import stat
from pathlib import Path

import pytest

skip_if_root = pytest.mark.skipif(os.getuid() == 0, reason="root bypasses permission checks")

from json_helper.operations import copy_file, create_file, delete_file, merge_files


# ── create_file ──────────────────────────────────────────────────────────────

class TestCreateFile:
    def test_creates_empty_json(self, tmp_path):
        target = tmp_path / "new.json"
        create_file(str(target))
        assert target.exists()
        assert json.loads(target.read_text()) == {}

    def test_raises_if_file_already_exists(self, tmp_path):
        target = tmp_path / "existing.json"
        target.write_text("{}\n")
        with pytest.raises(FileExistsError, match="already exists"):
            create_file(str(target))

    def test_raises_if_directory_missing(self, tmp_path):
        target = tmp_path / "no_such_dir" / "file.json"
        with pytest.raises(OSError, match="Unable to create"):
            create_file(str(target))


# ── copy_file ─────────────────────────────────────────────────────────────────

class TestCopyFile:
    def test_copies_file(self, tmp_path):
        src = tmp_path / "src.json"
        src.write_text('{"a": 1}\n')
        dst = tmp_path / "dst.json"
        copy_file(str(src), str(dst))
        assert dst.exists()
        assert json.loads(dst.read_text()) == {"a": 1}

    def test_raises_if_source_missing(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="not found"):
            copy_file(str(tmp_path / "ghost.json"), str(tmp_path / "dst.json"))

    @skip_if_root
    def test_raises_if_dest_not_writable(self, tmp_path):
        src = tmp_path / "src.json"
        src.write_text("{}\n")
        read_only_dir = tmp_path / "locked"
        read_only_dir.mkdir()
        read_only_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)
        try:
            with pytest.raises(OSError, match="Unable to copy"):
                copy_file(str(src), str(read_only_dir / "dst.json"))
        finally:
            read_only_dir.chmod(stat.S_IRWXU)


# ── merge_files ───────────────────────────────────────────────────────────────

class TestMergeFiles:
    def test_merges_two_files(self, tmp_path):
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        out = tmp_path / "out.json"
        f1.write_text('{"x": 1, "y": 2}\n')
        f2.write_text('{"y": 99, "z": 3}\n')
        merge_files(str(f1), str(f2), str(out))
        result = json.loads(out.read_text())
        assert result == {"x": 1, "y": 99, "z": 3}

    def test_file2_keys_take_precedence(self, tmp_path):
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        out = tmp_path / "out.json"
        f1.write_text('{"key": "from_file1"}\n')
        f2.write_text('{"key": "from_file2"}\n')
        merge_files(str(f1), str(f2), str(out))
        assert json.loads(out.read_text()) == {"key": "from_file2"}

    def test_raises_if_file1_missing(self, tmp_path):
        f2 = tmp_path / "b.json"
        f2.write_text("{}\n")
        with pytest.raises(FileNotFoundError, match="not found"):
            merge_files(str(tmp_path / "ghost.json"), str(f2), str(tmp_path / "out.json"))

    def test_raises_if_file2_missing(self, tmp_path):
        f1 = tmp_path / "a.json"
        f1.write_text("{}\n")
        with pytest.raises(FileNotFoundError, match="not found"):
            merge_files(str(f1), str(tmp_path / "ghost.json"), str(tmp_path / "out.json"))

    @skip_if_root
    def test_raises_if_output_not_writable(self, tmp_path):
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        f1.write_text("{}\n")
        f2.write_text("{}\n")
        read_only_dir = tmp_path / "locked"
        read_only_dir.mkdir()
        read_only_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)
        try:
            with pytest.raises(OSError, match="Unable to write"):
                merge_files(str(f1), str(f2), str(read_only_dir / "out.json"))
        finally:
            read_only_dir.chmod(stat.S_IRWXU)


# ── delete_file ───────────────────────────────────────────────────────────────

class TestDeleteFile:
    def test_deletes_file(self, tmp_path):
        target = tmp_path / "to_delete.json"
        target.write_text("{}\n")
        delete_file(str(target))
        assert not target.exists()

    def test_raises_if_file_missing(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="not found"):
            delete_file(str(tmp_path / "ghost.json"))

    @skip_if_root
    def test_raises_if_not_permitted(self, tmp_path):
        target = tmp_path / "protected.json"
        target.write_text("{}\n")
        target.chmod(0o000)
        read_only_dir = tmp_path
        read_only_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)
        try:
            with pytest.raises((OSError, PermissionError)):
                delete_file(str(target))
        finally:
            read_only_dir.chmod(stat.S_IRWXU)
            target.chmod(stat.S_IRWXU)
