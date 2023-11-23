from enum import Enum
import struct


class Alignment(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Widget():
    _name = "Widget"

    def __init__(self, parent):
        self.parent = parent
        self.children = []
        if self.parent is not None:
            self.parent.add_child(self)

    def add_child(self, child: "Widget"):
        self.children.append(child)

    def __str__(self):
        res = f"{self._name}"
        res += f"(parent: {self.parent._name})" if self.parent is not None else ""
        if len(self.children) > 0:
            res += f"\n\t{self.children}"
        return res

    def __repr__(self):
        return str(self)

    def json(self):
        res = {self._name: {}}
        if len(self.children) > 0:
            res[self._name]["children"] = [child.json() for child in self.children]

        return res

    @classmethod
    def from_json(cls, json, parent=None):
        class_name = next(iter(json))
        root = None

        keys = json[class_name].keys()

        match class_name:
            case "MainWindow":
                title = json["MainWindow"]["title"]
                root = MainWindow(title)
            case "Layout":
                alignment = json["Layout"]["alignment"]
                root = Layout(parent, alignment)
            case "LineEdit":
                max_length = json["LineEdit"]["max_length"]
                root = LineEdit(parent, max_length)
            case "ComboBox":
                items = json["ComboBox"]["items"]
                root = ComboBox(parent, items)

        if "children" in keys:
            for child in json[class_name]["children"]:
                # print(child, f"{ parent._name if parent is not None else None }")
                _ = Widget.from_json(child, root)

        return root



class MainWindow(Widget):
    _name = "MainWindow"

    def __init__(self, title: str):
        super().__init__(None)
        self.title = title

    def json(self):
        res = super().json()
        res[self._name]["title"] = self.title
        return res

    def __str__(self):
        res = f"{self._name} "
        res += f"(title: {self.title})"
        res += f"(parent: {self.parent._name})" if self.parent is not None else ""
        if len(self.children) > 0:
            res += f"\n\t{self.children}"
        return res


class Layout(Widget):
    _name = "Layout"

    def __init__(self, parent, alignment: Alignment):
        super().__init__(parent)
        self.alignment = alignment

    def json(self):
        res = super().json()
        res[self._name]["alignment"] = self.alignment
        return res

    def __str__(self):
        res = f"{self._name} "
        res += f"(alignment: {self.alignment})"
        res += f"(parent: {self.parent._name})" if self.parent is not None else ""
        if len(self.children) > 0:
            res += f"\n\t{self.children}"
        return res


class LineEdit(Widget):
    _name = "LineEdit"

    def __init__(self, parent, max_length: int = 10):
        super().__init__(parent)
        self.max_length = max_length

    def json(self):
        res = super().json()
        res[self._name]["max_length"] = self.max_length
        return res

    def __str__(self):
        res = f"{self._name} "
        res += f"(max_length: {self.max_length})"
        res += f"(parent: {self.parent._name})" if self.parent is not None else ""
        if len(self.children) > 0:
            res += f"\n\t{self.children}"
        return res


class ComboBox(Widget):
    _name = "ComboBox"

    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items

    def json(self):
        res = super().json()
        res[self._name]["items"] = self.items
        return res

    def __str__(self):
        res = f"{self._name} "
        res += f"(items: {self.items})"
        res += f"(parent: {self.parent._name})" if self.parent is not None else ""
        if len(self.children) > 0:
            res += f"\n\t{self.children}"
        return res
