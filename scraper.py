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
        print(f"\tDownloading image from URL: {url}")
        async with session.get(url) as response:
            if response.status == 200:
                with open(path_to_file, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                print(f"\t\tImage saved to: {path_to_file}")
            else:
                print(f"\t\tFailed to download {url}. Status code: {response.status}")
    except Exception as e:
        print(f"\t\tAn error occurred while downloading {url}: {e}")

async def parse_navbar(session, url, skins_dir):
    print(f"\tParsing navbar: {url}")
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'lxml')

    navbar = soup.find('nav', class_='main')
    sections = navbar.find_all('li')[:-1]  # Skip the last item

    tasks = [parse_section(session, url, li.a['href'], skins_dir) for li in sections]
    await asyncio.gather(*tasks)

async def get_num_pages(session, section_url):
    html = await fetch(session, section_url)
    soup = BeautifulSoup(html, 'lxml')
    
    # Get the page counter
    page_counter = soup.find('span', class_='count')
    # Get the page counter's string
    page_counter_span = page_counter.find('span')
    page_counter_str = page_counter_span.text
    # Get the start of the number representing the number of pages
    page_count_start = page_counter_str.rfind(' ') + 1
    # Return the number of pages
    return int(page_counter_str[page_count_start:])

async def parse_section(session, base_url, section, skins_dir):
    section_dir = os.path.join(skins_dir, os.path.basename(section))
    safe_mkdir(section_dir)

    section_url = base_url + section
    num_pages = await get_num_pages(session, section_url)

    # Loop over all pages
    for i in range(1, num_pages + 1):
        section_page_url = f"{ section_url }/{ i }"
        html = await fetch(session, section_page_url)
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
