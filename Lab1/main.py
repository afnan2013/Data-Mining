import os
import numpy as np
import cv2
import xlsxwriter

directory = r'F:\Study\4-2 Term\Data Mining\Train and test ETH 80 dataset\TestETH80data328';
row =2

workbook = xlsxwriter.Workbook('First Results.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(1, 0, "Photo Name")
worksheet.write(1, 1, "Mean Value")
worksheet.write(1, 2, "Standard Deviation")

for filename in os.listdir(directory):
    if filename.endswith(".png"):
        image = cv2.imread(directory+"/"+filename)
        # We use cvtColor, to convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # numpy calculation
        mean_value = np.mean(gray_image)
        print(mean_value)

        sd = np.std(gray_image)
        print(sd)

        s = '';

        # window shown waits for any key pressing event
        for c in filename :
            if 'a' <= c <= 'z':
                s += c
            else:
               break

        worksheet.write(row, 0, s)
        worksheet.write(row, 1, mean_value)
        worksheet.write(row, 2, sd)

        row +=1
        # window shown waits for any key pressing event

        continue
    else:
        continue

cv2.destroyAllWindows()
workbook.close()