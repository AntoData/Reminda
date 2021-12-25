import sys
sys.path.append("../BE-Logic")
import LoggerMeta
import tkinter as tk
from tkinter import ttk
import abc


@LoggerMeta.class_decorator_logger("INFO")
class SimpleWindow(abc.ABC, metaclass=LoggerMeta.MetaAbsLogger):
    @abc.abstractmethod
    def __init__(self, height: int, width: int, title: str):
        self.window = tk.Tk()
        self.window.title(title)
        self.height: int = height
        self.width: int = width
        self.window.geometry("{0}x{1}".format(width, height))


if __name__ == "__main__":
    try:
        s = SimpleWindow(200,200,"Exception")
        assert False
    except Exception as e:
        assert True
    @LoggerMeta.class_decorator_logger("INFO")
    class NewWindow(SimpleWindow):
        def __init__(self):
            SimpleWindow.__init__(self, 300, 400, "Example")

    n = NewWindow()
    print(n.width)
    n.window.mainloop()
