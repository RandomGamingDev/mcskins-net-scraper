# mcskins-net-scraper
A basic scraper you can use to get the name, description, and actual skin off of [minecraftskins.net](https://www.minecraftskins.net) easily, whether it be just for storing the data or for something like use in a ML project

Simply run the program `scraper.py` with all the dependencies from [requirements.txt](https://github.com/RandomGamingDev/mcskins-net-scraper/blob/main/requirements.txt) installed and it will create a `skins` directory that will contain each category with each category containing folders with each folder representing a skin and each folder containing a `meta.txt` which contains the title and description and a `skin.png` containing the actual skin. This can then be easily searched through or used in whatever you want, whether it be something like a website, to train a ML model, or anything else. Please note, that I do not legally own this data which is why it isn't posted alongside the scraper, if you want the data you can scrape it yourself (it's just 104 lines of code after all just look through it there isn't really any risk to running it).

The rest of the python files are:
- `to-imagefolder.py` for converting to a format that's easier for use in things like HuggingFace (although I still recommend you do stuff like zip the file)

Note: This doesn't make use of any async or multithreaded code, and is completely made with synchronous code. This makes it easier to understand for more people, but far slower, and tbh part of it's just the fact that I don't feel like optimizing it any further since tthis is sufficient for my needs. However, if you feel like optimizing it and creating a fork or pull request go right ahead :D
