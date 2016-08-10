from tkinter import Tk
from view import View


def main():
    root = Tk()
    root.title('Chess')
    View(root)
    root.mainloop()

if __name__ == '__main__':
    main()
