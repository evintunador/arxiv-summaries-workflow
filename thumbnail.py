import cv2
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import argparse
from datetime import datetime

def get_high_contrast_color(bg_color):
    brightness = sum(bg_color) / 3
    return (255, 255, 255) if brightness < 128 else (0, 0, 0)

# Get current date
now = datetime.now()
default = f"NEW\nARTIFICIAL\nINTELLIGENCE\nPAPERS\n{now.strftime('%b').upper()} {now.day}, {now.year}"

def main(video_path, text=default, coverage=2/3, font_size=140):
    # Capture first frame from video
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
    ret, frame = cap.read()
    cap.release()

    
    if not ret:
        print("Error reading video.")
        return

    # Resize to 16:9 ratio
    target_dim = (1920, 1080)
    frame = cv2.resize(frame, target_dim)

    # Create text overlay image
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    text_color = get_high_contrast_color(bg_color)
    text_img_width = int(coverage * target_dim[0])
    text_img = Image.new('RGB', (text_img_width, target_dim[1]), color=bg_color)

    font = ImageFont.truetype('arialbd.ttf', font_size)
    d = ImageDraw.Draw(text_img)

    #text_w, text_h = d.textsize(text, font=font)
    bbox = d.textbbox((0, 0), text, font=font)  # (left, top, right, bottom)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Calculate position to center the text
    position = ((text_img_width // 2) - (text_w // 2), (target_dim[1] // 2) - (text_h // 2))
    d.text(position, text, font=font, fill=text_color)

    # Convert PIL image to OpenCV format
    text_np = np.array(text_img)
    text_np = text_np[:, :, ::-1].copy()

    # Overlay text on the right position of the frame
    overlay_start = target_dim[0] - text_img_width
    frame[:, overlay_start:] = text_np

    # Save the final image
    output_path = 'thumbnail.jpg'
    cv2.imwrite(output_path, frame)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Overlay custom text on the first frame of a video.")
    parser.add_argument('video_path', type=str, help='Path to the video file.')
    parser.add_argument('--text', type=str, default=default, help='Custom text with new lines using \\n')
    parser.add_argument('--coverage', type=float, default=2/3, help='Fraction of frame to cover with text')
    parser.add_argument('--font_size', type=int, default=160, help='Font size of the overlay text')
    
    args = parser.parse_args()

    main(args.video_path, args.text, args.coverage, args.font_size)




