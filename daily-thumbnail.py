import cv2
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import argparse
from datetime import datetime
import ast

def get_high_contrast_color(bg_color):
    brightness = sum(bg_color) / 3
    return (255, 255, 255) if brightness < 128 else (0, 0, 0)

# Get current date
now = datetime.now()
default = f"NEW\nARTIFICIAL\nINTELLIGENCE\nPAPERS\n{now.strftime('%b').upper()} {now.day}\n{now.year}"

def main(video_path, text=default):
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
    text_img = Image.new('RGB', (target_dim[0] // 2, target_dim[1]), color=bg_color)

    font = ImageFont.truetype('arialbd.ttf', 120)
    d = ImageDraw.Draw(text_img)

    #text_w, text_h = d.textsize(text, font=font)
    bbox = d.textbbox((0, 0), text, font=font)  # (left, top, right, bottom)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    position = ((target_dim[0] // 4) - (text_w // 2), (target_dim[1] // 2) - (text_h // 2))
    d.text(position, text, font=font, fill=text_color)

    # Convert PIL image to OpenCV format
    text_np = np.array(text_img)
    text_np = text_np[:, :, ::-1].copy()

    # Overlay text on the right half of the frame
    frame[:, target_dim[0] // 2:] = text_np

    # Save the final image
    output_path = 'output_image.jpg'
    cv2.imwrite(output_path, frame)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Overlay custom image on the first frame of a video.")
    parser.add_argument('video_path', type=str, help='Path to the video file.')
    parser.add_argument('--text', type=str, 
                        default=f"NEW\nARTIFICIAL\nINTELLIGENCE\nPAPERS\n{now.strftime('%b').upper()} {now.day-5}-{now.day}\n{now.year}",
                        help='Alternative title to input. Dont forget to do \ n for new lines')
    
    args = parser.parse_args()

    # Safely evaluate arg2 to interpret escape sequences
    arg2_evaluated = args.text.encode('utf-8').decode('unicode_escape')

    main(args.video_path, arg2_evaluated)




