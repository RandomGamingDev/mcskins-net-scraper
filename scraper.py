from bs4 import BeautifulSoup
import aiohttp
import asyncio
import os

def safe_mkdir(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)

async def fetch(session, url):
    print(f"Fetching URL: {url}")
    async with session.get(url) as response:
        return await response.text()

async def download_image(session, url, path_to_file):
    try:
        print(f"Downloading image from URL: {url}")
        async with session.get(url) as response:
            if response.status == 200:
                with open(path_to_file, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                print(f"Image saved to: {path_to_file}")
            else:
                print(f"Failed to download {url}. Status code: {response.status}")
    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")

async def parse_navbar(session, url, skins_dir):
    print(f"Parsing navbar: {url}")
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'lxml')

    navbar = soup.find('nav', class_='main')
    sections = navbar.find_all('li')[1:-1]  # Skip the first and last item

    tasks = [parse_section(session, url, li.a['href'], skins_dir) for li in sections]
    await asyncio.gather(*tasks)

async def parse_section(session, base_url, section, skins_dir):
    section_dir = os.path.join(skins_dir, os.path.basename(section))
    safe_mkdir(section_dir)

    section_url = base_url + section
    html = await fetch(session, section_url)
    soup = BeautifulSoup(html, 'lxml')
    
    # Find all the skin blocks in the section.
    skin_blocks = soup.find_all('div', class_='card')

    # Loop over each skin block
    for block in skin_blocks:
        # Extract the relative URL of the skin
        skin = block.find('a')['href']

        # Create the section directories if they don't exist
        skinDir = section_dir + skin
        safe_mkdir(skinDir)

        # Get the URL to the skin
        skinURL = base_url + skin
        skinResult = await fetch(session, skinURL)

        # Get the name of the skin
        skinName = skinResult[skinResult.find("<h2 class=\"card-title\">") + 23:]
        skinName = skinName[:skinName.find('<')]

        # Get the description for the skin
        skinDescription = skinResult[skinResult.find("<p class=\"card-description\">") + 28:]
        skinDescription = skinDescription[:skinDescription.find('<')]

        # Create a text file containing the skin's name and description
        with open(skinDir + "/meta.txt", 'w') as f:
            f.write(f"Name: { skinName }\nDescription: { skinDescription }")

        # Get the URL to the skin img
        skinImgURL = skinURL + "/download"
        path_to_file = skinDir + "/skin.png"
        await download_image(session, skinImgURL, path_to_file)

        # Create a text file containing the skin's name and description
        with open(os.path.join(skinDir, "meta.txt"), 'w') as f:
            f.write(f"Name: { skinName }\nDescription: { skinDescription }")

        # Get the URL to the skin img
        skinImgURL = skinURL + "/download"
        path_to_file = os.path.join(skinDir, "skin.png")
        await download_image(session, skinImgURL, path_to_file)

    # Pagination: Continue to the next page if a 'next' button is present.
    next_button = soup.find('a', string='Next')
    if next_button and next_button.has_attr('href'):
        next_page_url = base_url + next_button['href']
        await parse_section(session, base_url, next_page_url, skins_dir)

async def main():
    print("Starting the script.")
    skins_dir = "skins"
    safe_mkdir(skins_dir)

    url = "https://www.minecraftskins.net"

    async with aiohttp.ClientSession() as session:
        await parse_navbar(session, url, skins_dir)

# Run the main coroutine
try:
    asyncio.run(main())
except Exception as e:
    print(f"An error occurred: {e}")