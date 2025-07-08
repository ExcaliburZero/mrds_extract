import io
import pathlib

import pytest

from mrds_util.raw import SaveFile
from tests.util import save_files_directory

TEST_SAVE_FILES = sorted(save_files_directory.glob("*.sav"))
if len(TEST_SAVE_FILES) == 0:
    print(save_files_directory)
    raise AssertionError


class TestSaveFile:
    @pytest.mark.parametrize("filepath", TEST_SAVE_FILES)
    def test_from_bin_does_not_error(self, filepath: pathlib.Path) -> None:
        with filepath.open("rb") as input_stream:
            SaveFile.from_bin(input_stream)

    @pytest.mark.parametrize("filepath", TEST_SAVE_FILES)
    def test_update_checksum_does_not_change_binary(self, filepath: pathlib.Path) -> None:
        with filepath.open("rb") as input_stream:
            save_file = SaveFile.from_bin(input_stream)

        bin_before = io.BytesIO()
        save_file.write_bin(bin_before)

        for save_entry in save_file.entries:
            save_entry.update_checksums()

        bin_after = io.BytesIO()
        save_file.write_bin(bin_after)

        assert bin_before.getvalue() == bin_after.getvalue()

    @pytest.mark.parametrize("filepath", TEST_SAVE_FILES)
    def test_changing_value_changes_binary(self, filepath: pathlib.Path) -> None:
        with filepath.open("rb") as input_stream:
            save_file = SaveFile.from_bin(input_stream)

        bin_before = io.BytesIO()
        save_file.write_bin(bin_before)

        for save_entry in save_file.entries:
            save_entry.player_name = "Joker".encode("ascii")

        bin_after = io.BytesIO()
        save_file.write_bin(bin_after)

        assert bin_before.getvalue() != bin_after.getvalue()

    @pytest.mark.parametrize("filepath", TEST_SAVE_FILES)
    def test_changing_body_only_changes_body_checksum(self, filepath: pathlib.Path) -> None:
        with filepath.open("rb") as input_stream:
            save_file = SaveFile.from_bin(input_stream)

        for save_entry in save_file.entries:
            header_checksum_before = save_entry.header_checksum
            body_checksum_before = save_entry.body_checksum

            save_entry.monsters[0].power = 42
            save_entry.update_checksums()

            header_checksum_after = save_entry.header_checksum
            body_checksum_after = save_entry.body_checksum

            assert header_checksum_before == header_checksum_after
            assert body_checksum_before != body_checksum_after

    @pytest.mark.parametrize("filepath", TEST_SAVE_FILES)
    def test_changing_header_only_changes_header_checksum(self, filepath: pathlib.Path) -> None:
        """
        TODO: I'm not sure why this property holds. I suspect it shouldn't, but yet it does...

        Keeping this test to document that fact.
        """
        with filepath.open("rb") as input_stream:
            save_file = SaveFile.from_bin(input_stream)

        for save_entry in save_file.entries:
            header_checksum_before = save_entry.header_checksum
            body_checksum_before = save_entry.body_checksum

            save_entry.player_name = "Joker".encode("ascii")
            save_entry.update_checksums()

            header_checksum_after = save_entry.header_checksum
            body_checksum_after = save_entry.body_checksum

            assert header_checksum_before != header_checksum_after
            assert body_checksum_before == body_checksum_after
