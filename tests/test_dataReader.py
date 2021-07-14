import utils.dataReader
from collections.abc import Iterable
from csv import Error as csvError
import pytest

class mock_textFileObject():
    def __next__():
        return 'test'
    def __iter__(self):
        return self

class mock_nontextFileObject():
    def __next__():
        return 2
    def __iter__(self):
        return self

class Test_dataRead_Unit:
    
    def test_dataRead():
        assert isinstance(utils.dataReader.dataRead(mock_textFileObject()), Iterable)

    def test_dataRead_invalidObject():
        with pytest.raises(csvError):
             assert isinstance(utils.dataReader.dataRead(mock_nontextFileObject()), Iterable)