from tkinter import *

root = Tk()

mylabel = Label(root, text="This is very easy")
mylabel.pack()
one = Label(root, text="One", fg="black", bg="white")
one.pack(fill=X)
two = Label(root, text="Two", fg="white", bg="black")
two.pack(side=LEFT, fill=Y)

topFrame = Frame(root)
topFrame.pack(height=200, width=100)
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

button1 = Button(bottomFrame, text="Load Training images(Browse Training image folder)", fg="red")
button2 = Button(bottomFrame, text="Extract Feature and store in database", fg="red")
button3 = Button(bottomFrame, text="Load Feature Data(Browse Training feature Data file)", fg="green")
button4 = Button(bottomFrame, text="Load Query image(Browse Test image)", fg="green")
button5 = Button(bottomFrame, text="Display (Extract query image feature and show the similar images)", fg="green")
button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=LEFT)
button5.pack(side=LEFT)


root.mainloop()