from widgets import MainWindow, Layout, Alignment, LineEdit, ComboBox

app = MainWindow("Application")
layout1 = Layout(app, Alignment.HORIZONTAL)
# layout2 = Layout(app, Alignment.VERTICAL)

edit1 = LineEdit(layout1, 20)
edit2 = LineEdit(layout1, 30)

# box1 = ComboBox(layout2, [1, 2, 3, 4])
# box2 = ComboBox(layout2, ["a", "b", "c"])

print(app)

d = app.json()

app = MainWindow.from_json(d)
print(app)

print(d)
