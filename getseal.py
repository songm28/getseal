import cv2
import numpy as np
import PIL.Image as Image
import sys, getopt
import time, os
import utils

def transparent_back(img):
    img = img.convert('RGBA')
    L, H = img.size
    color_0 = (255,255,255,255)
    for h in range(H):
        for l in range(L):
            dot = (l,h)
            color_1 = img.getpixel(dot)
            if color_1 == color_0:
                color_1 = color_1[:-1] + (0,)
                img.putpixel(dot,color_1)
    # print("in transparent_back.........")
    # print(type(img), img)
    # print(img.max(), img.min())
    return img

def extract_rgb(inputfile):
  np.set_printoptions(threshold=np.inf)
  image=cv2.imread(inputfile)
  
  hue_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  # cv2.imshow("s", hue_image)
  # cv2.waitKey(0)

  # print(type(image), image)
  # print(type(hue_image), hue_image)

  low_range = np.array([150,24,150])
  high_range = np.array([180, 255, 255])
  th = cv2.inRange(hue_image, low_range, high_range)
  index1 = th == 255
  
  # save image
  img = np.zeros(image.shape, np.uint8)
  
  img[:, :] = (255,255,255)
  img[index1] = image[index1]#(0,0,255)
  # cv2.imshow("s", img)
  # cv2.waitKey(0)
  
  # cv2.imwrite(os.path.join(os.path.dirname(outputfile), "{}_{}".format("mytest", os.path.basename(outputfile))), img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
  # cv2.imwrite(outputfile, img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
  # # delete rgb(255,255,255)
  # img1 = Image.open(outputfile)
  # img1=transparent_back(img1)
  # img1.save(outputfile)
  return img

def save_rgb_to_file(img_rgb, outputfile):
  if img_rgb.min() == 0:
    # blank image
    print("blank pages")
    return False
  cv2.imwrite(outputfile, img_rgb, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

def main(input_pdf, output_img_folder, pages=None):
  # pdf to imgs
  img_folder_name = os.path.basename(input_pdf).split(".")[0].replace(" ", "_")
  img_folder_fullpath = os.path.join(output_img_folder, img_folder_name)
  images = utils.Utils.pdf2image(
    sourcefile=input_pdf, 
    img_target_folder=img_folder_fullpath,
    pages=pages
  )
  for img in os.listdir(img_folder_fullpath):
    img_path = os.path.join(img_folder_fullpath, img)
    
    start = time.time()
    outputfilename = "{}__{}".format("seal", os.path.basename(img_path))
    outputfile = os.path.join(img_folder_fullpath, outputfilename)
    # action(img_path, outputfile)
    img_rgb=extract_rgb(img_path)
    save_rgb_to_file(img_rgb=img_rgb, outputfile=outputfile)
    end = time.time()
    print("cost time: {} seconds....".format(str(end-start)))


if __name__ == "__main__":
  inputfile = "artwork_10ml_no.pdf"
  # inputfile = "artwork125.pdf"
  output_img_folder = os.path.join("imgs")
  main(input_pdf=inputfile, output_img_folder=output_img_folder, pages=[0])

