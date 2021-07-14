import utils.dataReader
from collections.abc import Iterable

class mock_csvFile(Iterable):
    def __next__():
        return 'test'


class Test_dataRead_Unit:
    
    def test_dataRead():
        assert isinstance(utils.dataReader.dataRead(mock_csvFile()), Iterable)