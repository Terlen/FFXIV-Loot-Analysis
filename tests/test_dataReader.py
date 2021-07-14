import utils.dataReader
from collections.abc import Iterable

class mock_textFileObject():
    def __next__():
        return 'test'
    def __iter__(self):
        return self


class Test_dataRead_Unit:
    
    def test_dataRead():
        assert isinstance(utils.dataReader.dataRead(mock_textFileObject()), Iterable)