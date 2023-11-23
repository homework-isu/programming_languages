import pytest
from widgets import MainWindow, Layout, Alignment, LineEdit, ComboBox


class TestWidgets():
    def test_main_window_with_depth_1(self):
        app = MainWindow("Application")
        layout1 = Layout(app, Alignment.HORIZONTAL)
        layout2 = Layout(app, Alignment.VERTICAL)

        d = app.json()
        app_from_d = MainWindow.from_json(d)
        new_d = app_from_d.json()
        assert d == new_d
        assert app.title == app_from_d.title
        assert len(app.children) == len(app_from_d.children)

        for i in range(len(app.children)):
            assert app.children[i].alignment == app_from_d.children[i].alignment

    def test_main_window_with_depth_2(self):
        app = MainWindow("Application")
        layout1 = Layout(app, Alignment.HORIZONTAL)
        layout2 = Layout(app, Alignment.VERTICAL)
        combobox1 = ComboBox(layout1, [1, 2, 3, 4])
        combobox2 = ComboBox(layout1, [1, 2, 3, 4])
        combobox3 = ComboBox(layout2, [1, 2, 3, 4])

        d = app.json()
        app_from_d = MainWindow.from_json(d)
        new_d = app_from_d.json()
        assert d == new_d
        assert app.title == app_from_d.title
        assert len(app.children) == len(app_from_d.children)

        for i in range(len(app.children)):
            assert app.children[i].alignment == app_from_d.children[i].alignment
            assert len(app.children[i].children) == len(app_from_d.children[i].children)
            for j in range(len(app.children[i].children)):
                assert app.children[i].children[j].items == app_from_d.children[i].children[j].items

