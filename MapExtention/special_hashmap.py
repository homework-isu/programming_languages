from enum import Enum
import re


class Condition(Enum):
    LESS = 0
    LESS_OR_EQUAL = 1
    EQUAL = 2
    NOT_EQUAL = 3
    GREATER_OR_EQUAL = 4
    GREATER = 5


class ploc():

    def __init__(self, map, keys):
        self._map = map
        self._keys = keys

    def validate_key(self, key):
        pattern = re.compile(r'^[><=]*[><=]?[0-9]+\.{0,1}[0-9]{0,}$')
        return bool(pattern.match(key))

    def extract_condition_and_val(self, key):
        key = key.replace(" ", "")
        if not self.validate_key(key):
            raise Exception("Invalid key: " + key)

        if len(key) == 1:
            raise Exception("Invalid key")

        if len(key) >= 2:
            match key[:2]:
                case ">=":
                    return Condition.GREATER_OR_EQUAL, key[2:]
                case "<=":
                    return Condition.LESS_OR_EQUAL, key[2:]
                case "<>":
                    return Condition.NOT_EQUAL, key[2:]
            match key[0]:
                case ">":
                    return Condition.GREATER, key[1:]
                case "<":
                    return Condition.LESS, key[1:]
                case "=":
                    return Condition.EQUAL, key[1:]

    def extract_multy_key(self, key):
        key = key.replace("(", "")
        key = key.replace(")", "")
        return [val.replace(" ", "") for val in key.split(",")]

    def __getitem__(self, key_to_get):
        result = []
        conditions_and_keys = [self.extract_condition_and_val(val) for val in key_to_get.split(",")]

        for key in self._keys:
            multy_key = self.extract_multy_key(key)
            is_ok = True
            if len(multy_key) == len(conditions_and_keys):
                for i in range(len(multy_key)):
                    if multy_key[i].isnumeric():
                        multy_key[i] = int(multy_key[i])
                        value = int(conditions_and_keys[i][1])
                    else:
                        is_ok = False
                        break

                    match conditions_and_keys[i][0]:
                        case Condition.LESS:
                            if multy_key[i] >= value:
                                is_ok = False
                                break
                        case Condition.LESS_OR_EQUAL:
                            if multy_key[i] > value:
                                is_ok = False
                                break
                        case Condition.EQUAL:
                            if multy_key[i] != value:
                                is_ok = False
                                break
                        case Condition.NOT_EQUAL:
                            if multy_key[i] == value:
                                is_ok = False
                                break
                        case Condition.GREATER_OR_EQUAL:
                            if multy_key[i] < value:
                                is_ok = False
                                break
                        case Condition.GREATER:
                            if multy_key[i] <= value:
                                is_ok = False
                                break
                if is_ok:
                    result.append(self._map[key])
        return result


class SpecialHashMap():

    def __init__(self):
        self._map = {}
        self._keys = []
        self._iloc = []
        self._is_sorted = True

    def __getitem__(self, key):
        return self._map[key]

    def __setitem__(self, key, value):
        if key not in self._keys:
            self._is_sorted = False
            self._keys += [key]

        self._map[key] = value

    @property
    def iloc(self):
        if len(self._keys) == 0:
            return []

        if not self._is_sorted:
            self._keys.sort()

        if len(self._keys) != len(self._iloc):
            self._iloc = [self._map[key] for key in self._keys]

        return self._iloc

    @property
    def ploc(self):
        return ploc(self._map, self._keys)

