import os
import csv

dataDir = input("Enter the directory to the data: ")
metaDataDir = f"{ dataDir }/metadata.csv"

with open(metaDataDir, 'r') as f:
	r = csv.reader(f)
	for row in r:
		fileName, category, name, description = row
		txtDir = f"{ dataDir }/{ fileName[:fileName.find('.')] }.txt"
		with open(txtDir, 'w') as txt:
			txt.write(f"A { name } minecraft skin in the { category } category. { description }")
os.remove(metaDataDir)
