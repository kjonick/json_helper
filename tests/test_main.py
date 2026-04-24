import json
from pathlib import Path
from unittest.mock import patch

import pytest

from json_helper.main import build_parser, main


# ── help ──────────────────────────────────────────────────────────────────────

def test_no_args_prints_help(capsys):
    with patch("sys.argv", ["json-helper"]):
        main()
    out = capsys.readouterr().out
    assert "Welcome to JSON Helper tool" in out
    assert "new" in out


def test_help_flag_exits_zero():
    parser = build_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["--help"])
    assert exc.value.code == 0


# ── new ───────────────────────────────────────────────────────────────────────

def test_new_creates_file(tmp_path):
    target = tmp_path / "test.json"
    with patch("sys.argv", ["json-helper", "new", str(target)]):
        main()
    assert target.exists()
    assert json.loads(target.read_text()) == {}


def test_new_prints_error_if_file_exists(tmp_path, capsys):
    target = tmp_path / "existing.json"
    target.write_text("{}\n")
    with patch("sys.argv", ["json-helper", "new", str(target)]):
        with pytest.raises(SystemExit) as exc:
            main()
    assert exc.value.code == 1
    assert "Error:" in capsys.readouterr().out


# ── copy ──────────────────────────────────────────────────────────────────────

def test_copy_creates_destination(tmp_path):
    src = tmp_path / "src.json"
    src.write_text('{"key": "value"}\n')
    dst = tmp_path / "dst.json"
    with patch("sys.argv", ["json-helper", "copy", str(src), str(dst)]):
        main()
    assert dst.exists()
    assert json.loads(dst.read_text()) == {"key": "value"}


def test_copy_prints_error_if_source_missing(tmp_path, capsys):
    with patch("sys.argv", ["json-helper", "copy", str(tmp_path / "missing.json"), str(tmp_path / "dst.json")]):
        with pytest.raises(SystemExit) as exc:
            main()
    assert exc.value.code == 1
    assert "Error:" in capsys.readouterr().out


# ── merge ─────────────────────────────────────────────────────────────────────

def test_merge_produces_output(tmp_path):
    f1 = tmp_path / "a.json"
    f2 = tmp_path / "b.json"
    out = tmp_path / "out.json"
    f1.write_text('{"a": 1}\n')
    f2.write_text('{"b": 2}\n')
    with patch("sys.argv", ["json-helper", "merge", str(f1), str(f2), str(out)]):
        main()
    assert json.loads(out.read_text()) == {"a": 1, "b": 2}


def test_merge_prints_error_if_file_missing(tmp_path, capsys):
    f1 = tmp_path / "a.json"
    f1.write_text("{}\n")
    with patch("sys.argv", ["json-helper", "merge", str(f1), str(tmp_path / "missing.json"), str(tmp_path / "out.json")]):
        with pytest.raises(SystemExit) as exc:
            main()
    assert exc.value.code == 1
    assert "Error:" in capsys.readouterr().out


# ── delete ────────────────────────────────────────────────────────────────────

def test_delete_removes_file(tmp_path):
    target = tmp_path / "to_delete.json"
    target.write_text("{}\n")
    with patch("sys.argv", ["json-helper", "delete", str(target)]):
        main()
    assert not target.exists()


def test_delete_prints_error_if_file_missing(tmp_path, capsys):
    with patch("sys.argv", ["json-helper", "delete", str(tmp_path / "missing.json")]):
        with pytest.raises(SystemExit) as exc:
            main()
    assert exc.value.code == 1
    assert "Error:" in capsys.readouterr().out

