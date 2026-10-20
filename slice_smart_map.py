import os
from PIL import Image

def generate_deep_tiles(zoom_sources, output_dir="tiles", tile_size=200):
    os.makedirs(output_dir, exist_ok=True)

    for zoom_level, image_path in zoom_sources.items():
        if not os.path.exists(image_path):
            continue

        img = Image.open(image_path)
        width, height = img.size
        cols, rows = width // tile_size, height // tile_size
        
        zoom_dir = os.path.join(output_dir, str(zoom_level))
        os.makedirs(zoom_dir, exist_ok=True)

        for x in range(cols):
            x_dir = os.path.join(zoom_dir, str(x))
            os.makedirs(x_dir, exist_ok=True)
            
            for y in range(rows):
                box = (x * tile_size, y * tile_size, (x + 1) * tile_size, (y + 1) * tile_size)
                tile = img.crop(box)
                tile.save(os.path.join(x_dir, f"{y}.png"), "PNG")

    print("Deep multi-zoom tile pyramid generated!")

if __name__ == "__main__":
    zoom_configs = {
        0: "assets/map/master_z0.png",
        1: "assets/map/master_z1.png",
        2: "assets/map/master_z2.png",
        3: "assets/map/master_z3.png",
        4: "assets/map/master_z4.png"
    }
    generate_deep_tiles(zoom_configs, output_dir="tiles", tile_size=200)