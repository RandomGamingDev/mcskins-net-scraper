import requests
import shutil
import os

def removeWhitespace(string):
    string = string.replace('\n', '');
    string = string.replace('\t', '');
    string = string.replace(' ', '');
    return string

def safeMkdir(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)

# Creates the skins directory if it doesn't exist
skinsDir = "skins"
safeMkdir(skinsDir)

# The URL to the website
url = "https://www.minecraftskins.net"
# Get the HTML from the website
result = requests.get(url).text
# Remove whitespace and unnecessary characters
result = removeWhitespace(result)

# Get the navbar
navbar = result[result.find("<navclass=\"main\">"):result.find("</nav>")]

# Get the navbar's sections
sections = navbar.split("<li>")
# Remove the unnecessary sections at the start and end
sections.pop(0)
sections.pop()
# Remove the HTML surrounding the hrefs
sections = [section[8:] for section in sections]
sections = [section[:section.find('"')] for section in sections]

# Loop over each section
for section in sections:
    # Create the section directories if they don't exist
    sectionDir = skinsDir + section[9:]
    safeMkdir(sectionDir)

    # Get the URL to the section
    sectionURL = url + section
    # Get the HTML from the section
    sectionResult = requests.get(sectionURL).text
    # Remove whitespace and unnecessary characters
    sectionResult = removeWhitespace(sectionResult)

    # Get the counter
    sectionCounter = sectionResult[sectionResult.find("<spanclass=\"count\">"):]

    # Get the number of pages
    numPages = sectionCounter[sectionCounter.find("of") + 2:]
    numPages = int(numPages[:numPages.find('<')])
    
    # Loop over each page
    for i in range(1, numPages + 1):
        # Get the URL to the page
        pageURL = f"{ sectionURL }/{ i }"
        # Get the HTML from the section
        pageResult = requests.get(pageURL).text
        # Remove whitespace and unnecessary characters
        pageResult = removeWhitespace(pageResult)

        # Get the skin section
        pageSection = pageResult[pageResult.find("<divclass=\"rowgrid\">"):]

        # Get the skins
        skins = pageSection.split("<aclass=\"panel-link\"href=\"")
        skins = [skin[:skin.find('"')] for skin in skins]
        # Remove the unnecessary sections at the start
        skins.pop(0)
        
        # Loop over each skin
        for skin in skins:
            # Create the section directories if they don't exist
            skinDir = sectionDir + skin
            safeMkdir(skinDir)

            # Get the URL to the skin
            skinURL = url + skin
            skinResult = requests.get(skinURL).text

            # Get the name of the skin
            skinName = skinResult[skinResult.find("<h2 class=\"hero-title\">") + 23:]
            skinName = skinName[:skinName.find('<')]

            # Get the description for the skin
            skinDescription = skinResult[skinResult.find("<p class=\"card-description\">") + 28:]
            skinDescription = skinDescription[:skinDescription.find('<')]

            # Create a text file containing the skin's name and description
            with open(skinDir + "/meta.txt", 'w') as f:
                f.write(f"Name: { skinName }\nDescription: { skinDescription }")

            # Get the URL to the skin img
            skinImgURL = skinURL + "/download"
            skinImgResult = requests.get(skinImgURL, stream=True).raw
            skinImgResult.decode_content = True
            # Save the skin img
            with open(skinDir + "/skin.png", "wb") as f:
                shutil.copyfileobj(skinImgResult, f)
