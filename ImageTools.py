""" 
IMAGE TOOLS

Author: Cary Stothart
Date: 09/09/2016
Version: 1.0

DESCRIPTION:

A simple collection of image manipulation tools.

TOOLS:

Automatic Image Cropping:
Automatically crops all of the images in a given folder.

Image Resizing:
Proportionally resizes all of the images in a given folder.

"""

import glob
import re
import argparse

import PIL
from PIL import Image
        
class ImageTools:

    def __init__(self):
        self._parse()
        if self._args.tool != "s" and self._args.tool != "c":
            print "You must enter either s or c for the \"tool\" argument: " \
                  "c = automatically crop; s = resize"
            exit()
        if self._args.tool == "s" and self._args.newWidth == None:
            print "If you want to resize the images, you need to enter " \
                  "a value for the newWidth argument. For example: " \
                  "ImageTools.py s in_folder_name --newWidth 300"
            exit()
        self._processImages()
        
    def _parse(self):
        parser = argparse.ArgumentParser(description="A simple collection " \
                 "of image manipulation tools. Example: ImageTools.py c " \
                 "in_folder_name --outDir out_folder_name")
        parser.add_argument("tool", help="what you want to do to the" \
                            " images: c = automatically crop; s = resize")
        parser.add_argument("inDir", help="the folder that the images are in") 
        parser.add_argument("--outDir", help="the folder where you want all" \
                            " of the modified images to be saved. If not " \
                            "used, modified images will be saved in the " \
                            "source folder")
        parser.add_argument("--newWidth", help="If you enter s for the " \
                            "\"tool\" argument, specify here the new width " \
                            "in pixels you want the images to have. The " \
                            "height will be sized proportionate to the " \
                            "width. For example, if you have 20x30 images " \
                            "and enter 60 for this argument, the new size " \
                            "of the images will be 60x90", type=int)
        self._args = parser.parse_args()
        
    def _autoCropImage(self, img_path):
        print "Cropping " + img_path
        match = re.search("([\\\\ | /]\w*)(\.\w+)", img_path)
        img = Image.open(img_path)
        img.load()
        img_box = img.getbbox()
        croppedImg = img.crop(img_box)
        if(self._args.outDir):
            outName = self._args.outDir + match.group(1) + "_cropped" + \
                       match.group(2)
        else:
            outName = self._args.inDir + match.group(1) + "_cropped" + \
                       match.group(2)
        croppedImg.save(outName)
        
    def _resizeImage(self, img_path):
        print "Resizing " + img_path
        basewidth = self._args.newWidth
        match = re.search("([\\\\ | /]\w*)(\.\w+)", img_path)
        img = Image.open(img_path)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        resizedImg = img.resize((basewidth, hsize), Image.ANTIALIAS)
        if(self._args.outDir):
            outName = self._args.outDir + match.group(1) + "_resized" + \
                       match.group(2)
        else:
            outName = self._args.inDir + match.group(1) + "_resized" + \
                       match.group(2)
        resizedImg.save(outName)
        
    def _processImages(self):
        if self._args.tool == "c":
            for img_path in glob.glob(self._args.inDir + "/*"):
                self._autoCropImage(img_path)
        if self._args.tool == "s":
            for img_path in glob.glob(self._args.inDir + "/*"):
                self._resizeImage(img_path)                

tools = ImageTools()