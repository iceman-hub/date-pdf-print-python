from PIL import Image, ImageDraw, ImageFont

# create an image
out = Image.new("RGB", (150, 100), (255, 255, 255))

# get a font
fnt = ImageFont.truetype("./fonts/montserrat.ttf", 40)
# get a drawing context
d = ImageDraw.Draw(out)

# draw multiline text
d.multiline_text((10,10), "Hello\nWorld", font=fnt, fill=(250, 205, 0))
out.show('gnome')
out.save("fuuuuuuuuu.jpg")
