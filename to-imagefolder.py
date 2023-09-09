import os
import csv

dataDir = input("Enter the directory to the data: ")

with open(f"{ dataDir }/metadata.csv", 'w', newline='') as csv_file:
	# Create the CSV writer
	csv_writer = csv.writer(csv_file)

	# Write all of the CSV fields
	csv_fields = ["file_name", "category", "name", "description"]
	csv_writer.writerow(csv_fields)
	
	for category in os.listdir(path=dataDir):
		categoryDir = f"{ dataDir }/{ category }"
		# Skip if it isn't a directory
		if not os.path.isdir(categoryDir):
			continue

		for skin in os.listdir(path=categoryDir):
			skinDir = f"{ categoryDir }/{ skin }"

			# Where the skin's image is
			imgDir = f"{ skinDir }/skin.png"
			# Where we're moving it to
			newImgName = f"{ skin }.png"
			newImgDir = f"{ dataDir }/{ newImgName }"

			# Moving the skin
			os.rename(imgDir, newImgDir)

			# Extract all of the data from the original meta.txt file
			fields = ["Name", "Description"]
			metadata = None
			metaTxtDir = f"{ skinDir }/meta.txt"
			with open(metaTxtDir, 'r') as f:
				toFind = ": "
				metadata = [line[line.find(toFind) + len(toFind):].replace('\n', '') for line in f.readlines()]
				
			csv_writer.writerow([newImgName, category, metadata[0], metadata[1]])
				
			# The original skin directory is no longer needed
			os.remove(metaTxtDir)
			os.rmdir(skinDir)
		os.rmdir(categoryDir)
