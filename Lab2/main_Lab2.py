import os
import cv2
import numpy as np
from tkinter import *
from tkinter.filedialog import *
import xlsxwriter

root = Tk() # we don't want a full GUI, so keep the root window from appearing
test_book = xlsxwriter.Workbook('Train Results.xlsx')
test_sheet = test_book.add_worksheet()


def load_images():
    # show an "Open" dialog box and return the path to the selected file
    global directory
    directory = askdirectory(parent=root, initialdir="/", title='Please select a directory')
    print(directory)


def save_to_database():
    row = 2
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            print(filename)
            image = cv2.imread(directory+"/"+filename)
            # We use cvtColor, to convert to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow("gray image", gray_image)
            cv2.waitKey(10)
            # numpy calculation
            mean_value = np.mean(gray_image)
            print(mean_value)

            sd = np.std(gray_image)
            print(sd)

            label = ''
            # cutting the label from the filename
            for c in filename:
                if 'a' <= c <= 'z':
                    label += c
                else:
                    break

            test_sheet.write(row, 0, filename)
            test_sheet.write(row, 1, label)
            test_sheet.write(row, 2, mean_value)
            test_sheet.write(row, 3, sd)

            row += 1

    test_sheet.write(1, 0, "File Name")
    test_sheet.write(1, 1, "Photo Name")
    test_sheet.write(1, 2, "Mean Value")
    test_sheet.write(1, 3, "Standard Deviation")
    print("Train Phase Ends")

    cv2.destroyAllWindows()
    test_book.close()





topFrame = Frame(root, width=1000, height=460, relief='raised', borderwidth=5)
topFrame.pack()
bottomFrame = Frame(root, borderwidth=5)
bottomFrame.pack(side=BOTTOM)

button1 = Button(bottomFrame, text="Load Training images\n(Browse Training image folder)", width=25, fg="red", bg="black", command=load_images)
button2 = Button(bottomFrame, text="Extract Feature and\n store in database", width=25, fg="red", bg="black", command=save_to_database)
button3 = Button(bottomFrame, text="Load Feature Data\n(Browse Training feature Data file)", width=25, fg="red", bg="black")
button4 = Button(bottomFrame, text="Load Query image\n(Browse Test image)", fg="green")
button5 = Button(bottomFrame, text="Display (Extract query image \n feature and show the similar images)", fg="green")
button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=LEFT)
button5.pack(side=LEFT)


root.mainloop()