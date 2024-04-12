import tkinter as tk


class MyApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.canvas = tk.Canvas(self, width=200, height=200)
        self.canvas.pack()

        self.button = tk.Button(self, text='Kliknij mnie', command=self.on_click)
        self.button.pack()

    def draw(self):
        self.canvas.delete('all')
        self.canvas.create_text(100, 100, text='Paint Event', fill='red', font=('Helvetica', 20))

    def on_click(self):
        self.draw()


if __name__ == '__main__':
    app = MyApplication()
    app.mainloop()
