import cv2
import numpy as np
from tkinter.filedialog import *
import xlsxwriter
import xlrd
from skimage import feature, io, color, img_as_ubyte
from skimage.measure import shannon_entropy
import pandas as df
import ntpath


def sortSecond(val):
    return val[1]


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail  # tail or ntpath.basename(head)


def load_training_images():
    # show an "Open" dialog box and return the path to the selected file
    global directory
    directory = askdirectory(parent=root, initialdir=r"C:\Users\mafna\PycharmProjects\Data Mining\Lab4", title='Please select a directory')
    print(directory)


def save_CT_DD_to_database():
    row = 2
    test_book = xlsxwriter.Workbook('CT_DD Train Results.xlsx')
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
            sd = np.std(gray_image)
            variance = np.var(gray_image)
            quartiles = np.percentile(gray_image, [25, 50, 75])
            minimum = np.min(gray_image)
            maximum = np.max(gray_image)

            test_sheet.write(row, 0, filename)
            test_sheet.write(row, 1, mean_value)
            test_sheet.write(row, 2, sd)
            test_sheet.write(row, 3, variance)
            test_sheet.write(row, 4, minimum)
            test_sheet.write(row, 5, quartiles[0])
            test_sheet.write(row, 6, quartiles[1])
            test_sheet.write(row, 7, quartiles[2])
            test_sheet.write(row, 8, maximum)

            row += 1

    test_sheet.write(1, 0, "File Name")
    test_sheet.write(1, 1, "Mean Value")
    test_sheet.write(1, 2, "Standard Deviation")
    test_sheet.write(1, 3, "Variance")
    test_sheet.write(1, 4, "Minimum")
    test_sheet.write(1, 5, "Q1")
    test_sheet.write(1, 6, "Median")
    test_sheet.write(1, 7, "Q3")
    test_sheet.write(1, 8, "Maximum")

    print("Train Phase Ends")

    cv2.destroyAllWindows()
    test_book.close()


def save_GLCM_to_database():
    row = 2
    test_book = xlsxwriter.Workbook('GLCM Train Results.xlsx')
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


def save_SIFT_to_database():
    row = 2
    test_book = xlsxwriter.Workbook('SIFT Train Results.xlsx')
    test_sheet = test_book.add_worksheet()
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            print(filename)
            image = cv2.imread(directory + "/" + filename)
            # We use cvtColor, to convert to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow("gray image", gray_image)
            cv2.waitKey(1)
            sift = cv2.xfeatures2d.SIFT_create()
            keypoints, descriptors = sift.detectAndCompute(gray_image, None)
            desc = []
            for i in range(len(descriptors)):  # flatten
                for j in range(len(descriptors[0])):
                    desc.append(descriptors[i][j])
            if len(desc) >= 20:
                desc = desc[:20]

            test_sheet.write(row, 0, filename)
            for i in range(len(desc)):
                test_sheet.write(row, i+1, desc[i])
            row += 1
    print("Train Phase Ends")

    cv2.destroyAllWindows()
    test_book.close()


def save_SURF_to_database():
    row = 2
    test_book = xlsxwriter.Workbook('SURF Train Results.xlsx')
    test_sheet = test_book.add_worksheet()
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            print(filename)
            image = cv2.imread(directory + "/" + filename)
            # We use cvtColor, to convert to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow("gray image", gray_image)
            cv2.waitKey(1)
            surf = cv2.xfeatures2d.SURF_create()
            keypoints, descriptors = surf.detectAndCompute(gray_image, None)
            desc = []
            for i in range(len(descriptors)):  # flatten
                for j in range(len(descriptors[0])):
                    desc.append(descriptors[i][j])
            if len(desc) >= 20:
                desc = desc[:20]

            test_sheet.write(row, 0, filename)
            for i in range(len(desc)):
                test_sheet.write(row, i+1, desc[i])
            row += 1
    print("Train Phase Ends")

    cv2.destroyAllWindows()
    test_book.close()


def load_training_feature_data():
    # show an "Open" dialog box and return the path to the selected file
    global directory_feature
    directory_feature = askopenfilename(title='Please select a feature file')
    print(directory_feature)


def load_test_images():
    # show an "Open" dialog box and return the path to the selected file
    global test_directory
    test_directory = askdirectory(parent=root, initialdir=r"C:\Users\mafna\PycharmProjects\Data Mining\Lab4", title='Please select a Query directory')
    print(test_directory)


def save_CT_DD_Test_to_database():
    row = 2
    test_book = xlsxwriter.Workbook('CT_DD Test Results.xlsx')
    test_sheet = test_book.add_worksheet()
    for filename in os.listdir(test_directory):
        if filename.endswith(".png"):
            print(filename)
            image = cv2.imread(test_directory + "/" + filename)
            # We use cvtColor, to convert to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow("gray image", gray_image)
            cv2.waitKey(1)
            # numpy calculation
            mean_value = np.mean(gray_image)
            sd = np.std(gray_image)
            variance = np.var(gray_image)
            quartiles = np.percentile(gray_image, [25, 50, 75])
            minimum = np.min(gray_image)
            maximum = np.max(gray_image)

            test_sheet.write(row, 0, filename)
            test_sheet.write(row, 1, mean_value)
            test_sheet.write(row, 2, sd)
            test_sheet.write(row, 3, variance)
            test_sheet.write(row, 4, minimum)
            test_sheet.write(row, 5, quartiles[0])
            test_sheet.write(row, 6, quartiles[1])
            test_sheet.write(row, 7, quartiles[2])
            test_sheet.write(row, 8, maximum)

            row += 1

    test_sheet.write(1, 0, "File Name")
    test_sheet.write(1, 1, "Mean Value")
    test_sheet.write(1, 2, "Standard Deviation")
    test_sheet.write(1, 3, "Variance")
    test_sheet.write(1, 4, "Minimum")
    test_sheet.write(1, 5, "Q1")
    test_sheet.write(1, 6, "Median")
    test_sheet.write(1, 7, "Q3")
    test_sheet.write(1, 8, "Maximum")

    print("Test Feature Extraction Ends")
    cv2.destroyAllWindows()
    test_book.close()


def save_GLCM_Test_to_database():
    row = 2
    test_book = xlsxwriter.Workbook('GLCM Test Results.xlsx')
    test_sheet = test_book.add_worksheet()
    for filename in os.listdir(test_directory):
        if filename.endswith(".png"):
            print(filename)
            image = io.imread(test_directory + "/" + filename)
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

    print("Test Feature Extraction Ends")

    cv2.destroyAllWindows()
    test_book.close()


def save_SIFT_Test_to_database():
    row = 2
    test_book = xlsxwriter.Workbook('SIFT Test Results.xlsx')
    test_sheet = test_book.add_worksheet()
    for filename in os.listdir(test_directory):
        if filename.endswith(".png"):
            print(filename)
            image = cv2.imread(test_directory + "/" + filename)
            # We use cvtColor, to convert to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow("gray image", gray_image)
            cv2.waitKey(1)
            sift = cv2.xfeatures2d.SIFT_create()
            keypoints, descriptors = sift.detectAndCompute(gray_image, None)
            desc = []
            for i in range(len(descriptors)):  # flatten
                for j in range(len(descriptors[0])):
                    desc.append(descriptors[i][j])
            if len(desc) >= 20:
                desc = desc[:20]

            test_sheet.write(row, 0, filename)
            for i in range(len(desc)):
                test_sheet.write(row, i+1, desc[i])
            row += 1
    print("Test Feature Extraction Ends")

    cv2.destroyAllWindows()
    test_book.close()


def save_SURF_Test_to_database():
    row = 2
    test_book = xlsxwriter.Workbook('SURF Test Results.xlsx')
    test_sheet = test_book.add_worksheet()
    for filename in os.listdir(test_directory):
        if filename.endswith(".png"):
            print(filename)
            image = cv2.imread(test_directory + "/" + filename)
            # We use cvtColor, to convert to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow("gray image", gray_image)
            cv2.waitKey(1)
            surf = cv2.xfeatures2d.SURF_create()
            keypoints, descriptors = surf.detectAndCompute(gray_image, None)
            desc = []
            for i in range(len(descriptors)):  # flatten
                for j in range(len(descriptors[0])):
                    desc.append(descriptors[i][j])
            if len(desc) >= 40:
                desc = desc[:20]

            test_sheet.write(row, 0, filename)
            for i in range(len(desc)):
                test_sheet.write(row, i+1, desc[i])
            row += 1
    print("Test Feature Extraction Ends")

    cv2.destroyAllWindows()
    test_book.close()


def load_test_feature_data():
    # show an "Open" dialog box and return the path to the selected file
    global directory_test_feature
    directory_test_feature = askopenfilename(title='Please select a Test feature file')
    print(directory_test_feature)
    global results_filename
    results_filename = "Prediction "+path_leaf(directory_test_feature)


def display_similar_images_by_city_block_distance():
    print(directory_test_feature)
    print(directory)

    results_prediction_book = xlsxwriter.Workbook("UsingCityBlock "+results_filename)
    results_predition_sheet = results_prediction_book.add_worksheet()
    results_predition_sheet.write(1, 0, "Actual Image Name")
    results_predition_sheet.write(1, 1, "Predicted Image Name")

    book = xlrd.open_workbook(directory_feature)
    sheet = book.sheet_by_index(0)

    book1 = xlrd.open_workbook(directory_test_feature)
    sheet1 = book1.sheet_by_index(0)

    test_row = 2
    for k in range(sheet1.nrows-2):
        fittness = []
        loop = 2
        for i in range(sheet.nrows-2):
            sum = 0
            for j in range(1, sheet.ncols):
                sum += abs(float(sheet1.cell_value(test_row, j) - sheet.cell_value(loop, j)))
            row = [loop, sum]
            fittness.append(row)
            loop = loop + 1

        fittness.sort(key=sortSecond)
        print(fittness)

        index = fittness[0][0]
        testFile = sheet1.cell_value(test_row, 0)
        predictedFile = sheet.cell_value(index, 0)

        results_predition_sheet.write(test_row, 0, testFile)
        results_predition_sheet.write(test_row, 1, predictedFile)
        print(testFile,"  ", predictedFile)
        test_row = test_row + 1
    results_prediction_book.close()


def display_similar_images_by_canberra_distance():
    print(directory_test_feature)
    print(directory)

    results_prediction_book = xlsxwriter.Workbook("UsingCanberra " + results_filename)
    results_predition_sheet = results_prediction_book.add_worksheet()
    results_predition_sheet.write(1, 0, "Actual Image Name")
    results_predition_sheet.write(1, 1, "Predicted Image Name")

    book = xlrd.open_workbook(directory_feature)
    sheet = book.sheet_by_index(0)

    book1 = xlrd.open_workbook(directory_test_feature)
    sheet1 = book1.sheet_by_index(0)

    test_book = xlsxwriter.Workbook('Predition Results Can.xlsx')
    test_sheet = test_book.add_worksheet()
    test_row = 2
    for k in range(sheet1.nrows - 2):
        fittness = []
        loop = 2
        for i in range(sheet.nrows - 2):
            sum = 0
            for j in range(1, sheet.ncols):
                if float(sheet1.cell_value(test_row, j) + sheet.cell_value(loop, j)) != 0:
                    sum += abs(float(sheet1.cell_value(test_row, j) - sheet.cell_value(loop, j))) / (float(sheet1.cell_value(test_row, j) + sheet.cell_value(loop, j)))
                else:
                    sum += abs(float(sheet1.cell_value(test_row, j) - sheet.cell_value(loop, j)))
            row = [loop, sum]
            fittness.append(row)
            loop = loop + 1

        fittness.sort(key=sortSecond)
        print(fittness)

        index = fittness[0][0]
        testFile = sheet1.cell_value(test_row, 0)
        predictedFile = sheet.cell_value(index, 0)
        print(testFile, "  ", predictedFile)
        test_row = test_row + 1

    results_prediction_book.close()


def display_similar_images_by_random_forest():
    print()


root = Tk() # we don't want a full GUI, so keep the root window from appearing
root.winfo_toplevel().title("Image Recognition Using City Block Distance and Features : Five Number Summery and Variance")

bottomFrame = Frame(root, borderwidth=5)
bottomFrame.pack(side=BOTTOM)

button1 = Button(bottomFrame, text="Load Training images\n(Browse Training image folder)", width=25, fg="white", bg="blue", command=load_training_images)

button2 = Button(bottomFrame, text="Extract CT+DD Feature\n and store in database", width=25, fg="white", bg="red", command=save_CT_DD_to_database)
button3 = Button(bottomFrame, text="Extract GLCM Feature\n and store in database", width=25, fg="white", bg="red", command=save_GLCM_to_database)
button4 = Button(bottomFrame, text="Extract SIFT Feature\n and store in database", width=25, fg="white", bg="red", command=save_SIFT_to_database)
button5 = Button(bottomFrame, text="Extract SURF Feature\n and store in database", width=25, fg="white", bg="red", command=save_SURF_to_database)

button6 = Button(bottomFrame, text="Load Training Feature Data\n(Browse Training feature Data file)", width=25, fg="white", bg="green", command=load_training_feature_data)
button7 = Button(bottomFrame, text="Load Test Images\n(Browse Query Image Folder)", fg="black", bg="aqua", command=load_test_images)

button8 = Button(bottomFrame, text="Extract CT+DD Feature\n for query images and store", width=25, fg="white", bg="blue", command=save_CT_DD_Test_to_database)
button9 = Button(bottomFrame, text="Extract GLCM Feature \nfor query images and store", width=25, fg="white", bg="red", command=save_GLCM_Test_to_database)
button10 = Button(bottomFrame, text="Extract SIFT Feature \nfor query images and store", width=25, fg="white", bg="red", command=save_SIFT_Test_to_database)
button11 = Button(bottomFrame, text="Extract SURF Feature \nfor query images and store", width=25, fg="white", bg="red", command=save_SURF_Test_to_database)
button12 = Button(bottomFrame, text="Load Test Feature Data \n(Browse Query feature file)", width=25, fg="white", bg="red", command=load_test_feature_data)

button13 = Button(bottomFrame, text="Show similar images using\n City block distance(in excel sheet)", fg="white", bg="brown", command=display_similar_images_by_city_block_distance)
button14 = Button(bottomFrame, text="Show similar images using\n Canberra distance(in excel sheet)", width=25, fg="white", bg="red", command=display_similar_images_by_canberra_distance)
button15 = Button(bottomFrame, text="Show similar images using\n Random Forest(in excel sheet)", width=25, fg="white", bg="red", command=display_similar_images_by_random_forest)


button1.grid(row=0, column=0)
button2.grid(row=1, column=0)
button3.grid(row=2, column=0)
button4.grid(row=3, column=0)
button5.grid(row=4, column=0)
button6.grid(row=1, column=1)
button7.grid(row=2, column=1)
button8.grid(row=0, column=2)
button9.grid(row=1, column=2)
button10.grid(row=2, column=2)
button11.grid(row=3, column=2)
button12.grid(row=4, column=2)
button13.grid(row=0, column=3)
button14.grid(row=1, column=3)
button15.grid(row=2, column=3)

root.mainloop()
