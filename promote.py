from tkinter import *


class PromoteDialog:

    dialog = None
    canvas = None
    images = {}
    pieces = ['rook', 'knight', 'bishop', 'queen']
    piece_abbr = ['r', 'n', 'b', 'q']

    def __init__(self, root, color, pos_from, pos_to, controller):
        self.root = root
        self.color = color
        self.pos_from = pos_from
        self.pos_to = pos_to
        self.controller = controller
        self.make_dialog()
        self.make_canvas()
        self.make_images()
        self.canvas.bind('<Button-1>', self.on_image_clicked)
        self.root.unbind('<Button-1>')

    def make_dialog(self):
        self.dialog = Toplevel(self.root)
        self.dialog.title('Forvandling av bonde')
        self.dialog.geometry('320x80+420+140')
        self.dialog.attributes('-topmost', True)

    def make_canvas(self):
        self.canvas = Canvas(self.dialog, width=300, height=60)
        self.canvas.pack(padx=10, pady=10)

    def make_images(self):
        x_positions = [30, 110, 190, 270]
        for index, piece in enumerate(self.pieces):
            filename = './pieces_image/{}_{}.png'.format(piece, self.color)
            if filename not in self.images:
                self.images[filename] = PhotoImage(file=filename)
            self.canvas.create_image(x_positions[index], 30, image=self.images[filename])

    def get_clicked_piece(self, x):
        index = 10
        if x < 60:
            index = 0
        if 75 < x < 140:
            index = 1
        if 160 < x < 220:
            index = 2
        if x > 230:
            index = 3
        if index < 4:
            return self.piece_abbr[index].upper() if self.color == 'white' else self.piece_abbr[index]
        return None

    def on_image_clicked(self, event):
        selected_piece = self.get_clicked_piece(event.x)
        self.controller.make_promotion_move(self.pos_from, self.pos_to, selected_piece, self.color, self)

    def destroy_choosing_view(self):
        self.dialog.destroy()
