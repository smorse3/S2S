import tkinter as tk

from gui.main_window import MainWindow
from gui.styles import apply_win95_style


def main():

    root = tk.Tk()

    apply_win95_style(root)

    app = MainWindow(root)

    root.mainloop()


if __name__ == "__main__":

    main()