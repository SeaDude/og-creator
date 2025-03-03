#!/usr/bin/env python3
"""
og-creator: A CLI tool to generate favicon, logos, and an OG preview image.

Requirements:
1. Input: A logo image file (jpg/jpeg, png, svg).
2. Output:
   - If a "public" directory exists in the current working directory, output all files there.
   - Otherwise, create a new directory called "og-images" and output the files there.
   - Generated files include:
       - favicon.ico (with sizes 16×16, 32×32, and 48×48)
       - 40×40 logo (logo_40.png)
       - 80×80 retina logo (logo_80.png)
       - 1200×630 OG image (og_image.jpg), optimized to be under 300KB.
3. If the target output directory already exists (in the case of "og-images"), the tool aborts to avoid overwriting.
4. This tool is a stand-alone Python CLI that can be symlinked for global use.
"""

import os
import sys
import argparse
import io
from PIL import Image, ImageOps

def convert_svg_to_png(svg_path):
    try:
        import cairosvg
    except ImportError:
        print("Error: cairosvg is required for processing SVG files. Install it with 'pip install cairosvg'.")
        sys.exit(1)
    # Convert SVG to PNG bytes and load with Pillow.
    png_bytes = cairosvg.svg2png(url=svg_path)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")

def load_image(input_path):
    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".svg":
        return convert_svg_to_png(input_path)
    else:
        return Image.open(input_path).convert("RGBA")

def save_favicon(img, output_dir):
    # Create favicon.ico with multiple sizes.
    sizes = [(16, 16), (32, 32), (48, 48)]
    favicon_path = os.path.join(output_dir, "favicon.ico")
    img.save(favicon_path, format="ICO", sizes=sizes)
    print(f"Favicon saved to {favicon_path}")

def save_resized_logo(img, output_dir):
    # Save a 40x40 logo.
    logo_40 = img.resize((40, 40), resample=Image.LANCZOS)
    logo_40_path = os.path.join(output_dir, "logo_40.png")
    logo_40.save(logo_40_path, format="PNG")
    print(f"40x40 logo saved to {logo_40_path}")

    # Save an 80x80 retina logo.
    logo_80 = img.resize((80, 80), resample=Image.LANCZOS)
    logo_80_path = os.path.join(output_dir, "logo_80.png")
    logo_80.save(logo_80_path, format="PNG")
    print(f"80x80 retina logo saved to {logo_80_path}")

def save_og_image(img, output_dir):
    # Create a 1200x630 OG image using ImageOps.fit for a centered crop.
    target_size = (1200, 630)
    og_img = ImageOps.fit(img, target_size, method=Image.LANCZOS)
    # Convert to RGB to remove any alpha channel
    og_img = og_img.convert("RGB")
    og_path = os.path.join(output_dir, "og_image.jpg")
    
    # Save as JPEG and optimize so file size is under 300KB.
    quality = 85
    while quality > 10:
        buffer = io.BytesIO()
        og_img.save(buffer, format="JPEG", quality=quality, optimize=True)
        size_kb = buffer.tell() / 1024
        if size_kb <= 300:
            with open(og_path, "wb") as f:
                f.write(buffer.getvalue())
            print(f"OG image saved to {og_path} (quality={quality}, size={size_kb:.2f}KB)")
            return
        quality -= 5
    # If quality falls too low, save with minimal acceptable quality.
    og_img.save(og_path, format="JPEG", quality=quality, optimize=True)
    print(f"OG image saved to {og_path} with minimal quality={quality}")

def main():
    parser = argparse.ArgumentParser(description="og-creator: Generate favicon, logos, and OG preview image from a logo image.")
    parser.add_argument("input_image", help="Path to the input logo image (jpg, jpeg, png, svg)")
    args = parser.parse_args()
    
    cwd = os.getcwd()
    public_dir = os.path.join(cwd, "public")
    
    # Determine output directory based on existence of "public"
    if os.path.isdir(public_dir):
        output_dir = public_dir
        print(f"Found 'public' directory. Using it as output directory: {output_dir}")
    else:
        output_dir = os.path.join(cwd, "og-images")
        if os.path.exists(output_dir):
            print(f"Error: The directory '{output_dir}' already exists. Aborting to avoid overwriting.")
            sys.exit(1)
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Load the input image.
    try:
        img = load_image(args.input_image)
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)
    
    # Generate outputs.
    save_favicon(img, output_dir)
    save_resized_logo(img, output_dir)
    save_og_image(img, output_dir)
    
    print("All images have been generated successfully.")

if __name__ == "__main__":
    main()
