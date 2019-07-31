import os
import cv2
import numpy as np
from tkinter import *
from tkinter.filedialog import *
import xlsxwriter
import xlrd
from PIL import ImageTk, Image

root = Tk() # we don't want a full GUI, so keep the root window from appearing
root.winfo_toplevel().title("Image Recognition Using City Block Distance and Features : Five Number Summery and Variance")
topFrame = Frame(root, width=1000, height=460, borderwidth=5)
topFrame.pack()
midFrame = Frame(root, width=500, height=50, borderwidth=5)
midFrame.pack()
bottomFrame = Frame(root, borderwidth=5)
bottomFrame.pack(side=BOTTOM)


def sortSecond(val):
    return val[1]


def load_images():
    # show an "Open" dialog box and return the path to the selected file
    global directory
    directory = askdirectory(parent=root, initialdir="/", title='Please select a directory')
    print(directory)


def save_to_database():
    row = 2
    test_book = xlsxwriter.Workbook('Train Results.xlsx')
    test_sheet = test_book.add_worksheet()
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            print(filename)
            image = cv2.imread(directory+"/"+filename)
            # We use cvtColor, to convert to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow("gray image", gray_image)
            cv2.waitKey(1)
            # numpy calculation
            mean_value = np.mean(gray_image)
            print(mean_value)

            sd = np.std(gray_image)
            print(sd)

            variance = np.var(gray_image)

            quartiles = np.percentile(gray_image, [25, 50, 75])

            minimum = np.min(gray_image)
            maximum = np.max(gray_image)

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
            test_sheet.write(row, 4, variance)
            test_sheet.write(row, 5, minimum)
            test_sheet.write(row, 6, quartiles[0])
            test_sheet.write(row, 7, quartiles[1])
            test_sheet.write(row, 8, quartiles[2])
            test_sheet.write(row, 9, maximum)

            row += 1

    test_sheet.write(1, 0, "File Name")
    test_sheet.write(1, 1, "Label Name")
    test_sheet.write(1, 2, "Mean Value")
    test_sheet.write(1, 3, "Standard Deviation")
    test_sheet.write(1, 4, "Variance")
    test_sheet.write(1, 5, "Minimum")
    test_sheet.write(1, 6, "Q1")
    test_sheet.write(1, 7, "Median")
    test_sheet.write(1, 8, "Q3")
    test_sheet.write(1, 9, "Maximum")

    print("Train Phase Ends")

    cv2.destroyAllWindows()
    test_book.close()


def load_feature_data():
    # show an "Open" dialog box and return the path to the selected file
    global directory_feature
    directory_feature = askopenfilename(title='Please select a feature file')
    print(directory_feature)


def select_query_image():
    print(directory_feature)
    global directory_query
    directory_query = askopenfilename(title='Please select a QUERY image')
    print(directory_query)
    img = Image.open(directory_query)
    img = img.resize((125, 125), Image.BICUBIC)
    img = ImageTk.PhotoImage(img)
    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    query_image.config(image=img)
    query_image.image = img


def display_similar_images():
    print(directory_query)
    print(directory)
    book = xlrd.open_workbook(directory_feature)
    sheet = book.sheet_by_index(0)

    q_image = cv2.imread(directory_query)
    gray_image = cv2.cvtColor(q_image, cv2.COLOR_BGR2GRAY)
    variance = np.var(gray_image)
    quartiles = np.percentile(gray_image, [25, 50, 75])
    minimum = np.min(gray_image)
    maximum = np.max(gray_image)

    fittness = []
    loop = 2
    for i in range(sheet.nrows-2):
        print(sheet.cell_value(loop, 4))
        v = abs(float(variance - sheet.cell_value(loop, 4)))
        mini = abs(float(minimum - sheet.cell_value(loop, 5)))
        q1 = abs(float(quartiles[0] - sheet.cell_value(loop, 6)))
        q2 = abs(float(quartiles[1] - sheet.cell_value(loop, 7)))
        q3 = abs(float(quartiles[2] - sheet.cell_value(loop, 8)))
        maxi = abs(float(maximum - sheet.cell_value(loop, 9)))
        s = v + mini + q1 + q2 + q3 + maxi
        row = [i, s]
        fittness.append(row)
        loop = loop + 1
        print(v)
    fittness.sort(key=sortSecond)
    print(fittness)

    result_label = Label(topFrame, text="Similar Images")
    result_label.pack()

    l = 10
    for i in range(l):
        nestedRow = fittness[0]
        index = nestedRow[0]
        imageFile = sheet.cell_value(index-1, 0)

        img = Image.open(directory + "/" + imageFile)
        img = img.resize((125, 125), Image.BICUBIC)
        img = ImageTk.PhotoImage(img)
        result = Label(topFrame, image=img)
        result.pack(side=LEFT)
        result.image = img


query_label = Label(topFrame, text="Query Image")
query_image = Label(topFrame, text="Image will be here")
query_label.pack()
query_image.pack()

button1 = Button(bottomFrame, text="Load Training images\n(Browse Training image folder)", width=25, fg="white", bg="blue", command=load_images)
button2 = Button(bottomFrame, text="Extract Feature and\n store in database", width=25, fg="white", bg="red", command=save_to_database)
button3 = Button(bottomFrame, text="Load Feature Data\n(Browse Training feature Data file)", width=25, fg="white", bg="green", command=load_feature_data)
button4 = Button(bottomFrame, text="Load Query image\n(Browse Test image)", fg="black", bg="aqua", command=select_query_image)
button5 = Button(bottomFrame, text="Display (Extract query image \n feature and show the similar images)", fg="white", bg="brown", command=display_similar_images)
button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=LEFT)
button5.pack(side=LEFT)


root.mainloop()
