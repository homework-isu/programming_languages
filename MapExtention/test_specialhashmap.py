import pytest
from special_hashmap import SpecialHashMap


class TestSpecialHashMap():

    def test_getitem(self):
        map = SpecialHashMap()

        map["value1"] = 1
        map["value2"] = 2
        map["value3"] = 3

        assert map["value1"] == 1
        assert map["value2"] == 2
        assert map["value3"] == 3


    def test_iloc(self):
        map = SpecialHashMap()

        assert map.iloc == []

        map["value1"] = 1
        map["value2"] = 2
        map["value3"] = 3
        map["1"] = 10
        map["2"] = 20
        map["3"] = 30
        map["1, 5"] = 100
        map["5, 5"] = 200
        map["10, 5"] = 300

        assert map.iloc[0] == 10
        assert map.iloc[2] == 300
        assert map.iloc[5] == 200
        assert map.iloc[8] == 3

    def test_ploc(self):
        map = SpecialHashMap()
        map["value1"] = 1
        map["value2"] = 2
        map["value3"] = 3
        map["1"] = 10
        map["2"] = 20
        map["3"] = 30
        map["(1, 5)"] = 100
        map["(5, 5)"] = 200
        map["(10, 5)"] = 300
        map["(1, 5, 3)"] = 400
        map["(5, 5, 4)"] = 500
        map["(10, 5, 5)"] = 600

        assert map.ploc[">=1"] == [10, 20, 30]
        assert map.ploc[">1"] == [20, 30]
        assert map.ploc["<>1"] == [20, 30]
        assert map.ploc["<=2"] == [10, 20]
        assert map.ploc["<3"] == [10, 20]
        assert map.ploc[">0, >0"] == [100, 200, 300]
        assert map.ploc[">=10, >0"] == [300]
        assert map.ploc["<5, >=5, >=3"] == [400]
        assert map.ploc["<5, >=5, =12"] == []

    def test_exaption(self):
        map = SpecialHashMap()
        map["value1"] = 1
        map["value2"] = 2
        map["value3"] = 3
        map["1"] = 10
        map["2"] = 20
        map["3"] = 30

        with pytest.raises(Exception):
            map.ploc["1, 5"]

        with pytest.raises(Exception):
            map.ploc[">=value"]