# mcskins-net-scraper
A basic scraper you can use to get the name, description, and actual skin off of [minecraftskins.net](https://www.minecraftskins.net) easily, whether it be just for storing the data or for something like use in a ML project

There is an asynchronous version (`scraper.py`) and a synchronous version (`sync-scraper.py`) (I recommend using the asynchronous version as it is a bit faster)

Simply run the program `scraper.py` with all the dependencies from [requirements.txt](https://github.com/RandomGamingDev/mcskins-net-scraper/blob/main/requirements.txt) installed and it will create a `skins` directory that will contain each category with each category containing folders with each folder representing a skin and each folder containing a `meta.txt` which contains the title and description and a `skin.png` containing the actual skin. This can then be easily searched through or used in whatever you want, whether it be something like a website, to train a ML model, or anything else. Please note, that I do not legally own this data which is why it isn't posted alongside the scraper, if you want the data you can scrape it yourself (it's just 104 lines of code after all just look through it there isn't really any risk to running it).

The rest of the python files are:
- `to-new-skins.py` for cleaning the data by converting all pre-1.8 skins to their newer version using `mc_skin_updater.py` from https://github.com/RandomGamingDev/mc_skin_updater_py. This script expects the default structure and image resolution from scraping (which it keeps the same).
- `to-imagefolder.py` for converting to a format that's easier for use in things like HuggingFace (although I still recommend you do stuff like zip the file) and for general processing. This script expects the default structure from scraping (which it converts to the imagefolder structure).
- `to-1dir-dataset.py` for converting to a format that's easier to use for multiple projects. This script expects the imagefolder structure from converting the data via `to-imagefolder.py` (which it converts to a 1 directory based basic structure where there's the images with a txt file of the same front part of the name with a description created from the name, category, and description).
- `to-res.py` for changing the resolution with NEAREST min & mag resizing for whatever your needs may be (png compression helps to keep the file sizes small so storage shouldn't be much of a concern. This expects either the imagefolder or 1dir structure and will keep it the same, but will modify the image resolution.

Thanks to Kiddooo & 105hua for making an asynchronous version of the scraper
