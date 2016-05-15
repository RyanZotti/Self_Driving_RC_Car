import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.text = tk.Text(self)
        self.text.pack()
        self.text.bind("<KeyRelease-Return>", self.on_return_release)

    def on_return_release(self, event):
        self.text.insert("end", "boink! ")

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
