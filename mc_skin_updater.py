from PIL import Image, ImageOps

def convert(oldSkin): # The function assumes that you already checked that this is an old MC skin
	newSkin = Image.new(mode="RGBA", size=(64, 64))
	newSkin.paste(oldSkin, (0, 0)) # Paste in most of the skin itself

	# Copying right to left leg
	legUL = ImageOps.mirror(oldSkin.crop((4, 16, 4 + 4, 16 + 4))) # To top left
	newSkin.paste(legUL, (20, 48))
	legUR = oldSkin.crop((8, 16, 8 + 4, 16 + 4)) # To top right
	newSkin.paste(legUR, (24, 48))
	legBL = ImageOps.mirror(oldSkin.crop((0, 20, 0 + 12, 20 + 12))) # To bottom left
	newSkin.paste(legBL, (16, 52))
	legBR = ImageOps.mirror(oldSkin.crop((12, 20, 12 + 4, 20 + 12))) # To bottom right
	newSkin.paste(legBR, (28, 52))

	# Copying right to left arm
	legUL = ImageOps.mirror(oldSkin.crop((44, 16, 44 + 4, 16 + 4))) # To top left
	newSkin.paste(legUL, (36, 48))
	legUR = ImageOps.mirror(oldSkin.crop((48, 16, 48 + 4, 16 + 4))) # To top right
	newSkin.paste(legUR, (40, 48))
	legBL = ImageOps.mirror(oldSkin.crop((40, 20, 40 + 12, 20 + 12))) # To bottom left
	newSkin.paste(legBL, (32, 52))
	legBR = ImageOps.mirror(oldSkin.crop((52, 20, 52 + 4, 20 + 12))) # To bottom right
	newSkin.paste(legBR, (44, 52))

	return newSkin
