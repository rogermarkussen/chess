from tkinter import Tk
from view import View
from controller import Controller


def main():
    root = Tk()
    root.title('Chess')
    controller = Controller()
    view = View(root, controller)
    root.mainloop()

if __name__ == '__main__':
    main()
