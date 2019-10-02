import cv2
import numpy as np
from tkinter import *
from tkinter.filedialog import *
import xlsxwriter
import xlrd
from PIL import ImageTk, Image
from skimage import feature, io, color, img_as_ubyte
from skimage.measure import shannon_entropy


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
            image = io.imread(directory + "/" + filename)
            grey_img = img_as_ubyte(color.rgb2gray(image))

            greyCoMatrix = feature.greycomatrix(grey_img, [1], [0], levels=256, symmetric=True, normed=True)

            max_prob = np.amax(greyCoMatrix)
            contrast = feature.greycoprops(greyCoMatrix, 'contrast')
            correlation = feature.greycoprops(greyCoMatrix, 'correlation')
            homogeneity = feature.greycoprops(greyCoMatrix, 'homogeneity')
            energy = feature.greycoprops(greyCoMatrix, 'energy')
            entropy = shannon_entropy(grey_img)

            test_sheet.write(row, 0, filename)
            test_sheet.write(row, 1, max_prob)
            test_sheet.write(row, 2, contrast)
            test_sheet.write(row, 3, correlation)
            test_sheet.write(row, 4, homogeneity)
            test_sheet.write(row, 5, energy)
            test_sheet.write(row, 6, entropy)

            row += 1

    test_sheet.write(1, 0, "File Name")
    test_sheet.write(1, 1, "Maximum Probability")
    test_sheet.write(1, 2, "Contrast")
    test_sheet.write(1, 3, "Correlation")
    test_sheet.write(1, 4, "Homogeneity")
    test_sheet.write(1, 5, "Energy")
    test_sheet.write(1, 6, "Entropy")

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

    q_image = io.imread(directory_query)
    grey_img = img_as_ubyte(color.rgb2gray(q_image))

    greyCoMatrix = feature.greycomatrix(grey_img, [1], [0], levels=256, symmetric=True, normed=True)

    max_prob = np.amax(greyCoMatrix)
    contrast = feature.greycoprops(greyCoMatrix, 'contrast')
    correlation = feature.greycoprops(greyCoMatrix, 'correlation')
    homogeneity = feature.greycoprops(greyCoMatrix, 'homogeneity')
    energy = feature.greycoprops(greyCoMatrix, 'energy')
    entropy = shannon_entropy(grey_img)

    fittness = []
    loop = 2
    for i in range(sheet.nrows - 2):
        print(sheet.cell_value(loop, 4))
        m_p = abs(float(max_prob - sheet.cell_value(loop, 1))) / (abs(float(max_prob)) + abs(float(sheet.cell_value(loop, 1))))
        con = abs(float(contrast - sheet.cell_value(loop, 2))) / (abs(float(contrast)) + abs(float(sheet.cell_value(loop, 2))))
        corr = abs(float(correlation - sheet.cell_value(loop, 3))) / (abs(float(correlation)) + abs(float(sheet.cell_value(loop, 3))))
        homo = abs(float(homogeneity - sheet.cell_value(loop, 4))) / (abs(float(homogeneity)) + abs(float(sheet.cell_value(loop, 4))))
        en = abs(float(energy - sheet.cell_value(loop, 5))) / (abs(float(energy)) + abs(float(sheet.cell_value(loop, 5))))
        entr = abs(float(entropy - sheet.cell_value(loop, 6))) / (abs(float(entropy)) + abs(float(sheet.cell_value(loop, 6))))
        s = m_p + con + corr + homo + en + entr
        row = [i, s]
        fittness.append(row)
        loop = loop + 1
    fittness.sort(key=sortSecond)
    print(fittness)

    result_label = Label(topFrame, text="Similar Images")
    result_label.pack()

    l = 10
    for i in range(l):
        index = fittness[i][0]
        imageFile = sheet.cell_value(index - 1, 0)

        img = Image.open(directory + "/" + imageFile)
        img = img.resize((125, 125), Image.BICUBIC)
        img = ImageTk.PhotoImage(img)
        result = Label(topFrame, image=img)
        result.pack(side=LEFT)
        result.image = img


root = Tk()     # we don't want a full GUI, so keep the root window from appearing
root.winfo_toplevel().title("Image Recognition Using City Block Distance and Features : Five Number Summery and Variance")
topFrame = Frame(root, width=1000, height=460, borderwidth=5)
topFrame.pack()
midFrame = Frame(root, width=500, height=50, borderwidth=5)
midFrame.pack()
bottomFrame = Frame(root, borderwidth=5)
bottomFrame.pack(side=BOTTOM)

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