import tkinter as tk
import tkinter.simpledialog


class LineWidthDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Select line width:").grid(row=0, columnspan=2)
        self.entry = tk.Entry(master)
        self.entry.grid(row=1, column=0)
        self.slider = tk.Scale(master, from_=1, to=10, orient=tk.HORIZONTAL)
        self.slider.grid(row=1, column=1)
        return self.entry

    def apply(self):
        try:
            self.result = int(self.slider.get())
        except ValueError:
            self.result = None
