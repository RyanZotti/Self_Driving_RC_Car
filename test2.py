from tkinter import *

main = Tk()

def leftKey(event):
    print("Left key pressed")

def rightKey(event):
    print("Right key pressed")

frame = Frame(main, width=100, height=100)
main.bind('<Left>', leftKey)
main.bind('<Right>', rightKey)
frame.pack()
main.mainloop()
