import sys
sys.path.append("../BE-Logic")
import LoggerMeta
import tkinter as tk
import abc


@LoggerMeta.class_decorator_logger("INFO")
class SimpleWindow(abc.ABC, metaclass=LoggerMeta.MetaAbsLogger):
    """
    This is an abstract class that is the base for all our window classes
    ...

    Attributes
    ----------
    window: tk.Tk
        This attribute is the window we will customize

    height: int
        This attribute is height of the window we are creating

    width: int
        This attribute is the width of the window we are creating

    icon_filename: str
        This is the path to the file that will be used as icon for these windows

    Methods
    -------
    N/A
    """
    @abc.abstractmethod
    def __init__(self, height: int, width: int, title: str):
        self.logger.info("We call tk.Tk()")
        self.window = tk.Tk()
        self.window.title(title)
        self.height: int = height
        self.width: int = width
        self.window.geometry("{0}x{1}".format(width, height))
        self.icon_filename = "{0}/Config/icon.png".format(LoggerMeta.MetaAbsLogger.get_root())
        self.window.resizable(width=False, height=False)
        try:
            self.window.tk.call("wm", "iconphoto", self.window._w, tk.PhotoImage(file=self.icon_filename))
        except Exception as e:
            self.logger.warning("We could not customize the application icon: {0}".format(e))


if __name__ == "__main__":
    try:
        s = SimpleWindow(200, 200, "Exception")
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
