from PIL import Image, ImageOps

try:
    img = Image.open('img/home-banner-hq.png')
    flipped = ImageOps.mirror(img)
    flipped.save('img/home-banner-hq-flipped.png')
    print("Success: Flipped image saved to img/home-banner-hq-flipped.png")
except Exception as e:
    print(f"Error flipping image: {e}")
