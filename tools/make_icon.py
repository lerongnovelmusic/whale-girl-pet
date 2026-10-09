"""Generate the app icon from the pet sprite.

Source is the transparent maid sprite produced for the DSH plugin, so the icon is
repo-owned artwork rather than a personal file. The character sits in a mostly
transparent 512x512 canvas, so it is cropped to its alpha bounding box first and
re-centred on a square canvas; otherwise the taskbar icon would be mostly empty.

Outputs:
  assets/icon.png  256x256, used by BrowserWindow({icon}) and by packed builds
  assets/icon.ico  multi-size Windows icon
"""

from PIL import Image

SRC = r"D:\deepseek_harness_project\whale-pet-custom\maid-pet.png"
OUT_DIR = r"D:\deepseek_harness_project\whale-pet-app\assets"
SIZE = 256

image = Image.open(SRC).convert("RGBA")

# Crop to the visible character, then pad back to a square so the drawing keeps
# its aspect ratio and stays centred.
bbox = image.getbbox()
character = image.crop(bbox)
side = max(character.width, character.height)
square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
square.paste(character, ((side - character.width) // 2, (side - character.height) // 2), character)

icon = square.resize((SIZE, SIZE), Image.LANCZOS)
icon.save(f"{OUT_DIR}/icon.png", "PNG")

# A multi-resolution .ico keeps small taskbar sizes crisp.
icon.save(
    f"{OUT_DIR}/icon.ico",
    "ICO",
    sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
)

# Report the alpha coverage so a mostly-empty icon cannot slip through unnoticed.
alpha = icon.getchannel("A")
opaque = sum(1 for value in alpha.getdata() if value > 8)
print(f"source bbox        : {bbox}")
print(f"icon size          : {icon.size}")
print(f"opaque coverage    : {opaque / (SIZE * SIZE):.1%} of the canvas")
print(f"wrote              : {OUT_DIR}/icon.png, {OUT_DIR}/icon.ico")
