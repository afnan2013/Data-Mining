import os
import numpy as np
import cv2
import xlsxwriter

directory = r'F:\Study\4-2 Term\Data Mining\Train and test ETH 80 dataset\TestETH80data328'
test_book = xlsxwriter.Workbook('Test Results.xlsx')
test_sheet = test_book.add_worksheet()

row = 2
for filename in os.listdir(directory):
    if filename.endswith(".png"):
        print(filename)
        image = cv2.imread(directory+"/"+filename)
        # We use cvtColor, to convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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

        test_sheet.write(row, 0, label)
        test_sheet.write(row, 1, mean_value)
        test_sheet.write(row, 2, sd)
        row += 1

test_sheet.write(1, 0, "Photo Name")
test_sheet.write(1, 1, "Mean Value")
test_sheet.write(1, 2, "Standard Deviation")
print("Test Phase Ends")

cv2.destroyAllWindows()
test_book.close()
