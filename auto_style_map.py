import os
import cv2
import numpy as np

RAW_INPUT_PATH = "assets/map/raw_screenshot_hexham.png"
OUTPUT_DIR = "assets/map/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_cartoon_tier(zoom_level, scale_multiplier):
    if not os.path.exists(RAW_INPUT_PATH):
        print(f"Error: Missing {RAW_INPUT_PATH}")
        return

    print(f"Styling Zoom Level {zoom_level} (Scale: {scale_multiplier}x)...")
    
    img = cv2.imread(RAW_INPUT_PATH)
    h, w = img.shape[:2]
    new_w, new_h = int(w * scale_multiplier), int(h * scale_multiplier)
    img_resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    # Cartoon smoothing & edges
    color = cv2.bilateralFilter(img_resized, d=9, sigmaColor=75, sigmaSpace=75)
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

    # Color quantization using correct OpenCV constant
    data = color.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.1)
    K = 8
    _, label, center = cv2.kmeans(data, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    quantized = center[label.flatten()].reshape(color.shape)

    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cartoon = cv2.bitwise_and(quantized, edges_colored)

    output_path = os.path.join(OUTPUT_DIR, f"master_z{zoom_level}.png")
    cv2.imwrite(output_path, cartoon)
    print(f"Saved stylized master_z{zoom_level}.png!")

if __name__ == "__main__":
    create_cartoon_tier(0, 1.0)
    create_cartoon_tier(1, 1.5)
    create_cartoon_tier(2, 2.5)
    create_cartoon_tier(3, 4.0)
    create_cartoon_tier(4, 6.0)
    print("\nStyling complete! Now run: python slice_smart_map.py")