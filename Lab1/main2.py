import os
import numpy as np
import cv2
import xlsxwriter

directory = r'F:\Study\4-2 Term\Data Mining\Train and test ETH 80 dataset\TrainETH80data2952'
train_book = xlsxwriter.Workbook('Train Results.xlsx')
train_sheet = train_book.add_worksheet()

row = 2
for filename in os.listdir(directory):
    if filename.endswith(".png"):
        print(filename)
        image = cv2.imread(directory + "/" + filename)
        # I use cvtColor, to convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # numpy calculation mean
        mean_value = np.mean(gray_image)
        print(mean_value)

        # numpy calculation standard deviation
        sd = np.std(gray_image)
        print(sd)

        label = ''
        # cutting the label from the filename
        for c in filename:
            if 'a' <= c <= 'z':
                label += c
            else:
                break

        train_sheet.write(row, 0, label)
        train_sheet.write(row, 1, mean_value)
        train_sheet.write(row, 2, sd)
        row += 1

train_sheet.write(1, 0, "Photo Name")
train_sheet.write(1, 1, "Mean Value")
train_sheet.write(1, 2, "Standard Deviation")
print("Train Phase Ends")

cv2.destroyAllWindows()
train_book.close()
