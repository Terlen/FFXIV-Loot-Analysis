import builtins
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
        with patch("builtins.open", mock_open(read_data='text,text2,text3,text4,text5,text6,text7')):
            assert isinstance(utils.dataReader.dataRead(mock_textFileObject), Iterable)

    def test_dataRead_fileNotExist(self):
        with pytest.raises(FileNotFoundError):
            assert isinstance(utils.dataReader.dataRead('test.file'), Iterable)

    def test_dataRead_binaryFile(self):
        with pytest.raises(csv.Error):
            with patch("builtins.open", mock_open(read_data=b'text')):
                assert isinstance(utils.dataReader.dataRead(mock_nontextFileObject), Iterable)
    
    def test_dataRead_wrongColumns(self):
        with patch("builtins.open", mock_open(read_data='text,text2,text3')):
            with pytest.raises(IndexError):
                assert isinstance(utils.dataReader.dataRead(mock_nontextFileObject), Iterable)

class Test_dataPrint_Unit:
  
    test_data = [['x','y','z','a','b']]

    def test_dataPrint(self):
        assert utils.dataReader.dataPrint(self.test_data) == None
    
    def test_dataPrint_Error(self, monkeypatch):
        def mock_exception():
            raise RuntimeError
        with pytest.raises(Exception):
            monkeypatch.setattr(builtins, 'print', mock_exception)
            assert utils.dataReader.dataPrint(self.test_data) == None

class Test_encounterSplit_Unit:
    
    test_validData = [['7/13/2021 18:07', 'ObtainLoot', 'Your Character', 'Byakko Totem', 0]]
    test_noEncounter = [['7/13/2021 18:07', 'GreedLoot', 'Your Character', 'Byakko Totem', 0]]
    test_partialEncounter = [['7/13/2021 18:07', 'AddLoot', '', 'Byakko Totem', 0],['7/13/2021 18:07', 'AddLoot', '', 'Byakko Axe', 0]]

    def test_encounterSplitter(self):
        assert isinstance(utils.dataReader.encounterSplitter(self.test_validData), Iterable)
    
    def test_encounterSplitter_noEncountersFound(self):
        assert utils.dataReader.encounterSplitter(self.test_noEncounter) == []
    
    def test_encounterSplitter_partialEncounter(self):
        assert isinstance(utils.dataReader.encounterSplitter(self.test_partialEncounter), Iterable)