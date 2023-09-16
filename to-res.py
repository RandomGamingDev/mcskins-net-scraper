import os
from PIL import Image

dataDir = input("Enter the directory to the data: ")
res = int(input("Enter the resolution that you want: "))

for fileName in os.listdir(dataDir):
	if fileName[fileName.find('.'):] != ".png":
		continue

	filePath = f"{ dataDir }/{ fileName }"
	Image.open(filePath)\
		.resize((res, res), Image.Resampling.NEAREST)\
		.save(filePath)
