import pystray
from PIL import Image, ImageDraw

def create_icon_image():
    size = 64
    image = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, size - 8, size - 8), fill="#4a7dbd")
    return image

def build_tray_icon(on_open_report, on_open_settings, on_quit):
    menu = pystray.Menu(
        pystray.MenuItem("View Weekly Report", on_open_report),
        pystray.MenuItem("Settings", on_open_settings),
        pystray.MenuItem("Quit", on_quit),
    )
    icon = pystray.Icon(
        "Daily_Use_Organizer",
        create_icon_image(),
        "Daily_Use_Organizer",
        menu
    )
    return icon