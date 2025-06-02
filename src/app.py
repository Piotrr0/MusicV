from window import Window;

class Application:
    def __init__(self):
        self.window = Window()

    def run(self):
        self.window.update()