"""Unit tests for app.services.file_utils -- file generation & cleanup."""

import os
import pytest
from unittest.mock import patch
from app.services.file_utils import generate_resume_file, cleanup_file


@pytest.fixture
def tmp_upload_dir(tmp_path):
    """Override UPLOAD_DIR to use a temp directory."""
    with patch("app.services.file_utils.UPLOAD_DIR", str(tmp_path)):
        yield tmp_path


class TestGenerateResumeFile:
    def test_creates_file(self, tmp_upload_dir):
        filepath, filename = generate_resume_file(1, "My resume content")
        assert os.path.exists(filepath)

    def test_content_matches(self, tmp_upload_dir):
        content = "Python, FastAPI, PostgreSQL"
        filepath, _ = generate_resume_file(2, content)
        with open(filepath, "r") as f:
            assert f.read() == content

    def test_original_naming(self, tmp_upload_dir):
        _, filename = generate_resume_file(3, "content", is_optimized=False)
        assert "original" in filename
        assert "optimized" not in filename

    def test_optimized_naming(self, tmp_upload_dir):
        _, filename = generate_resume_file(4, "content", is_optimized=True)
        assert "optimized" in filename

    def test_returns_tuple(self, tmp_upload_dir):
        result = generate_resume_file(5, "content")
        assert isinstance(result, tuple)
        assert len(result) == 2


class TestCleanupFile:
    def test_removes_existing_file(self, tmp_upload_dir):
        filepath, _ = generate_resume_file(10, "temp content")
        assert os.path.exists(filepath)
        cleanup_file(filepath)
        assert not os.path.exists(filepath)

    def test_nonexistent_file_no_error(self, tmp_upload_dir):
        # Should not raise
        cleanup_file("/nonexistent/path/file.txt")
