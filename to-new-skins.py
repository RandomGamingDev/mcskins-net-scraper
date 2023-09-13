import mc_skin_updater
from PIL import Image
import os

dataDir = input("enter the directory to the data: ")

for category in os.listdir(path=dataDir):
	categoryDir = f"{ dataDir }/{ category }"
	for skin in os.listdir(path=categoryDir):
		skinDir = f"{ categoryDir }/{ skin }"
		skinImgName = "skin.png"
		skinImgDir = f"{ skinDir }/{ skinImgName }"

		skinImg = Image.open(skinImgDir)
		if skinImg.height == 32:
			mc_skin_updater.convert(skinImg).save(skinImgDir)
