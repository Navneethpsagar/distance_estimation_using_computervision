#import opencv and numpy
import cv2  
import numpy as np
import os
from tabulate import tabulate
import csv

os.system('cls')


#trackbar callback fucntion does nothing but required for trackbar
def change_x_min(val):
    global x_min 
    x_min = val
def change_x_max(val):
    global x_max 
    x_max = val
def change_y_min(val):
    global y_min 
    y_min = val
def change_y_max(val):
    global y_max
    y_max = val
# def change_x_min(x):
#     global x_min 
#     x_min = cv2.getTrackbarPos('x_max','controls')
# def change_x_max(x):
#     global x_max 
#     x_max = cv2.getTrackbarPos('x_max','controls')
# def change_y_min(x):
#     global y_min 
#     y_min = cv2.getTrackbarPos('y_min','controls')
# def change_y_max(x):
#     global y_max
#     y_max = cv2.getTrackbarPos('y_max','controls')




#initial color and crop dimensions
circle_color=(0,0,255)
x_min = 0
x_max = 0
y_min = 0
y_max = 0

# input and output
image_input = './input_new/'
image_output = './output_test/'
name_list = []
image_global = 0

# fields and table to store the data
fields = ['Location', 'Name', 'Background', 'Width', 'Height', 'MegaPixels', 'Distance(cm)', 'Measurement(mm)', 'Crop']  
table=[]

# to obtain the list of files in the given directory
def get_files_list(file_path):
    return os.listdir(file_path)

# to check if given output directory exists or not
def check_paths(image_ip, image_op):
    if not os.path.exists(image_ip):
        print('Input Folder Error')
        exit()
    if not os.path.exists(image_op):
        os.mkdir(image_op)

# saving dat ato file and displaying the table
def save_data(rows):        
    # name of csv file  
    filename = "results.csv"

    # display table
    print(tabulate(rows, headers=fields, tablefmt="grid"))

    # writing to csv file  
    with open(filename, 'w') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        csvwriter.writerow(fields)
        # writing the data rows  
        csvwriter.writerows(rows)

# crop image funciton
def crop_image(image, dimension):
    return image[dimension[0]:dimension[1],dimension[2]:dimension[3]]

# main function
if __name__ == '__main__':

    # checking paths and creating them if needed
    check_paths(image_input, image_output)

    # getting list of folders in the input folder
    image_folders = get_files_list(image_input)

    # cycling through the list of folders
    for i in range(0, 1): #len(image_folders)):  
        
        # the output folder 
        image_output_folder_path = image_output + image_folders[i]
        # image input folder path for reaing
        image_folder_path = image_input + image_folders[i]

        # making output directory if not existing
        if not os.path.exists(image_output_folder_path):
            os.mkdir(image_output_folder_path)

        # getting the list of images inside the folder
        images_names = get_files_list(image_folder_path)
        
        # cycling through the images in the current folder
        for j in range(0, 1):#len(images_names)):

            dimension = [0,0,0,0]
            
            # adding the image name to the big list
            name_list.append(images_names[j])

            # reading the image
            image_global = cv2.imread(image_folder_path + '/' + images_names[j])

            # converting the image to GRAY
            img = cv2.cvtColor(image_global.copy(), cv2.COLOR_BGR2GRAY)

            # the path of input image
            print('image_path: ',image_folder_path + '/' + images_names[j])
            #create a black image 
            img = cv2.imread(image_folder_path+'/'+images_names[j])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # getting the image size dimentions
            screen_res = 900, 1200
            scale_width = screen_res[0] / img.shape[1]
            scale_height = screen_res[1] / img.shape[0]
            scale = min(scale_width, scale_height)
            #resized window width and height
            window_width = int(img.shape[1] * scale)
            window_height = int(img.shape[0] * scale)
            # making the windows
            cv2.namedWindow('Image Window', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image Window', window_width, window_height)
            #create a seperate window named 'controls' for trackbar
            cv2.namedWindow('controls')
            cv2.resizeWindow('controls', 1000, 500)
            #create trackbar in 'controls' window with name 'r''
            cv2.createTrackbar('x_min','controls',0,img.shape[1],change_x_min)
            cv2.createTrackbar('x_max','controls',img.shape[1],img.shape[1],change_x_max)
            cv2.createTrackbar('y_min','controls',0,img.shape[0],change_y_min)
            cv2.createTrackbar('y_max','controls',img.shape[0],img.shape[0],change_y_max)
            # cropping the image
            while(1):
                
                copy = img.copy()
                #returns current position/value of trackbar 
                x_min= int(cv2.getTrackbarPos('x_min','controls'))
                x_max= int(cv2.getTrackbarPos('x_max','controls'))
                y_min= int(cv2.getTrackbarPos('y_min','controls'))
                y_max= int(cv2.getTrackbarPos('y_max','controls'))

                # start coordinates
                start_point = (x_min, y_min)
                # Ending coordinate, here (220, 220) represents the bottom right corner of rectangle
                end_point = (x_max, y_max)
                
                # Blue color in BGR
                color = (255, 0, 0)
                
                # Line thickness of 2 px
                thickness = 4
                
                # Using cv2.rectangle() method
                # Draw a rectangle with blue line borders of thickness of 2 px
                image = cv2.rectangle(copy, start_point, end_point, color, thickness)


                cv2.imshow('Image Window',image)
                # print('Crop: ', [y_min, y_max, x_min, x_max])

                #waitfor the user to press escape and break the while loop 
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    dimension = [y_min, y_max, x_min, x_max]
                    break
            # saving the paramaters for the image
            background_ = None
            if image_folders[i][10:12] == 'b':
                background_ = 'Black'
            elif image_folders[i][10:12] == 'w':
                background_ = 'White'
            # getting the megapixel of the image    
            megapixels = round(image_global.shape[0] * image_global.shape[1] / 1000000, 0)
            # getting the distance of the image
            distance = image_folders[i][0:2]
            # getting the measurement taken by the image
            measurement = image_folders[i][5:7]

            # storing the output filename
            output_filename = str(distance) + 'cm_' + str(measurement) + 'mm_' + str(int(megapixels)) + 'mp_' + background_ + '.jpg'
            print('Image output name: ', images_names[j], output_filename)

            # writing the cropped image to file
            # cv2.imwrite('./output_crop_gray/'+output_filename, crop_image(img, dimension))
            cv2.imshow('Image Window', crop_image(img, dimension))
            cv2.waitKey(0)
            # adding the image and its details to a csv file
            table.append([image_folder_path, images_names[j], background_, image_global.shape[1], image_global.shape[0], megapixels, distance, measurement, dimension])
                
    print('Number of images: ', len(name_list))
    print('Table: ', table)
    save_data(table)

#destroys all window
cv2.destroyAllWindows()