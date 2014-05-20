from kivy.app import App
from kivy.uix.widget import Widget


class A_Widget(Widget):
    pass


class A_New_App(App):
    def build(self):
        return A_Widget()


if __name__ == '__main__':
    A_New_App().run()