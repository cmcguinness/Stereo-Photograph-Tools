from PIL import Image, ImageTk
from tkinter import Tk, messagebox, Button, Label, PhotoImage, mainloop, Frame, filedialog
from stereotools import StereoTools
from mpo import MPO

class AlignTool:
    def __init__(self):
        self.ui_image = None
        self.image = None
        self.mpo = None
        self.tools = StereoTools()
        self.tkimg = None
        self.root = None
        self.show_diff = False
        self.toggle_diff_button = None
        self.style = 'color'
        self.gamma = 1.0
        self.gamma_label = None

    def open_file(self):
        file_path = filedialog.askopenfilename(title="Select an MPO File", filetypes=[("MPO files", "*.mpo"), ("All files", "*.*")])
        if file_path is not None:
            self.mpo = MPO(file_path)
            self.tools.set_image(self.mpo)

    def edit_ana(self):
        global saved_class
        saved_class = self

        WIDTH, HEIGHT = 800, 600
        self.root = Tk()


        top = Frame(self.root)
        bottom = Frame(self.root)


        top.pack(side="top")
        my_ana = self.tools.make_anaglyph(style=self.style, gamma=self.gamma)
        self.tkimg = ImageTk.PhotoImage(my_ana.resize((WIDTH, HEIGHT), Image.Resampling.NEAREST))

        Button(top, text="<<-", command=lambda: self.shift(10,0)).pack(side="left")
        Button(top, text="<-", command=lambda: self.shift(1,0)).pack(side="left")
        Button(top, text="->", command=lambda: self.shift(-1,0)).pack(side="left")
        Button(top, text="->>", command=lambda: self.shift(-10,0)).pack(side="left")

        Button(top, text="⇑", command=lambda: self.shift(0,10)).pack(side="left")
        Button(top, text="↑", command=lambda: self.shift(0,1)).pack(side="left")
        Button(top, text="↓", command=lambda: self.shift(0,-1)).pack(side="left")
        Button(top, text="⇓", command=lambda: self.shift(0,-10)).pack(side="left")

        Label(top, text=" ").pack(side="left")

        self.toggle_diff_button = Button(top, text="Diff", command=self.toggle_diff)
        self.toggle_diff_button.pack(side="left")

        self.style_button = Button(top, text="Color", command=self.toggle_style)
        self.style_button.pack(side="left")

        Label(top, text=" ").pack(side="left")
        Button(top, text="γ ↑", command=lambda: self.toggle_gamma(1)).pack(side="left")
        Button(top, text="γ ↓", command=lambda: self.toggle_gamma(-1)).pack(side="left")

        self.gamma_label = Label(top, text="γ=1.0")
        self.gamma_label.pack(side="left")

        Label(top, text=" ").pack(side="left")

        Button(top, text="Save", command=self.save).pack(side="left")

        self.lbl = Label(bottom, image=self.tkimg)
        self.lbl.pack()
        bottom.pack(side="bottom", fill="both", expand=True)
        mainloop()

    def toggle_diff(self):
        self.show_diff = not self.show_diff
        if self.show_diff:
            self.toggle_diff_button['text'] = 'Normal'
        else:
            self.toggle_diff_button['text'] = 'Diff'

        self.shift(0,0)

    def toggle_style(self):
        styles = [('color', 'Color'), ('l-bw', 'Low Color'), ('bw', 'B&W')]
        for i in range(len(styles)):
            if styles[i][0] == self.style:
                n = (i+1) % len(styles)
                self.style = styles[n][0]
                self.style_button['text'] = styles[n][1]
                self.shift(0,0)
                return

    def toggle_gamma(self, increment):
        self.gamma += increment/10

        self.gamma_label['text'] = f'γ={self.gamma:.1f}'
        self.shift(0,0)


    def shift(self, delta_x, delta_y):
        self.tools.shift_x += delta_x
        self.tools.shift_y += delta_y
        my_ana = self.tools.make_anaglyph(style=self.style, gamma=self.gamma, show_diff=self.show_diff)
        WIDTH, HEIGHT = 800, 600
        img = ImageTk.PhotoImage(my_ana.resize((WIDTH, HEIGHT), Image.Resampling.NEAREST))
        self.lbl.configure(image=img)
        self.lbl.image = img
        self.lbl.pack()
        # self.canvas.update_idletasks()

    def save(self):
        dir = directory = filedialog.askdirectory(title="Save file to")
        self.tools.make_anaglyph(suffix='ana_edited', style=self.style, output_directory=dir)
        messagebox.showinfo('Saved',f'File {self.tools.outname} saved.')
        exit(0)


if __name__ == "__main__":
    at = AlignTool()
    at.open_file()
    at.edit_ana()



