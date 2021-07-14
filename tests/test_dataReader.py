import utils.dataReader
from collections.abc import Iterable
import csv
from unittest.mock import mock_open, patch
import pytest

class mock_textFileObject:
    def __next__(*args, **kwargs):
        return 'test'
    def __iter__(self):
        return self

class mock_nontextFileObject:
    def __next__():
        return 2
    def __iter__(self):
        return self

class Test_dataRead_Unit:
    
    def test_dataRead(self, monkeypatch):
        with patch("builtins.open", mock_open(read_data='text')):
            assert isinstance(utils.dataReader.dataRead(mock_textFileObject), Iterable)

    def test_dataRead_fileNotExist(self):
        with pytest.raises(FileNotFoundError):
            assert isinstance(utils.dataReader.dataRead('test.file'), Iterable)

    def test_dataRead_binaryFile(self):
        with pytest.raises(csv.Error):
            with patch("builtins.open", mock_open(read_data=b'text')):
                assert isinstance(utils.dataReader.dataRead(mock_nontextFileObject), Iterable)