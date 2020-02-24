import PIL
import PIL.Image

image = PIL.Image.open(r'C:\Users\rex87\Desktop\standard_playing_cards3.png')

suit_d = {
	0:"trefle",
	1:"carreau",
	2:"coeur",
	3:"pique",
	4:"joker",
}

rank_d = {
	0:"as",
	1:"2",
	2:"3",
	3:"4",
	4:"5",
	5:"6",
	6:"7",
	7:"8",
	8:"9",
	9:"10",
	10:"valet",
	11:"dame",
	12:"roi",
}

for i in range(13):
	for j in range(5):
		fout = r'images\{}_{}.png'.format(suit_d[j], rank_d[i])
		image.crop((168*i, 244*j, 168*(i+1), 244*(j+1))).save(fout)
		print(fout)

# import IPython;IPython.embed(colors='Neutral')