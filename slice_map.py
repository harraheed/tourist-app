import os
from PIL import Image

def generate_multi_zoom_tiles(zoom_sources, output_dir="tiles", tile_size=200):
    """
    Takes specific master images for each zoom level, slices them into 
    exact 200x200 pixel grids, and organizes them for Leaflet.
    
    zoom_sources = {
        0: "assets/map/town_overview.png",  # Macro view
        1: "assets/map/town_district.png",  # Mid view
        2: "assets/map/town_street.png"     # Micro street-level detail (Image 3 style)
    }
    """
    os.makedirs(output_dir, exist_ok=True)

    for zoom_level, image_path in zoom_sources.items():
        if not os.path.exists(image_path):
            print(f"Skipping Zoom {zoom_level}: File not found at {image_path}")
            continue

        img = Image.open(image_path)
        width, height = img.size
        
        cols = width // tile_size
        rows = height // tile_size
        
        print(f"Processing Zoom {zoom_level}: Grid size {cols}x{rows} ({tile_size}x{tile_size}px tiles)")
        
        zoom_dir = os.path.join(output_dir, str(zoom_level))
        os.makedirs(zoom_dir, exist_ok=True)

        for x in range(cols):
            x_dir = os.path.join(zoom_dir, str(x))
            os.makedirs(x_dir, exist_ok=True)
            
            for y in range(rows):
                # Crop each 200x200 tile
                box = (
                    x * tile_size,
                    y * tile_size,
                    (x + 1) * tile_size,
                    (y + 1) * tile_size
                )
                tile = img.crop(box)
                
                # Save into Leaflet expected z/x/y structure
                tile_path = os.path.join(x_dir, f"{y}.png")
                tile.save(tile_path, "PNG")

    print("Smart multi-zoom tile generation complete!")

if __name__ == "__main__":
    # Map out your detail levels from macro to micro
    zoom_configs = {
        0: "assets/map/master_z0.png",  # Whole town overview
        1: "assets/map/master_z1.png",  # District / shopping core view
        2: "assets/map/master_z2.png"   # Ultra-detailed street/shop front view
    }
    generate_multi_zoom_tiles(zoom_configs, output_dir="tiles", tile_size=200)