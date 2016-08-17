from tkinter import Tk
from view import View
from controller import Controller


def main():
    root = Tk()
    root.title('Chess')
    root.geometry('1000x720+250+250')
    root.attributes('-topmost', True)
    controller = Controller()
    view = View(root, controller)
    root.mainloop()

if __name__ == '__main__':
    main()
