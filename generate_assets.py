"""
XUiDa64 - High-Resolution Logo & Multi-Size Icon Generator
Generates icon.png, icon.ico, logo.png, and logo_small.png with anti-aliasing.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_emblem(size=1024):
    """Draws the core XUiDa shield / CPU emblem at high resolution."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    r_outer = int(size * 0.44)
    r_inner = int(size * 0.41)

    # 1. Subtle Outer Glow
    glow_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    pts_glow = [
        (cx + (r_outer + 16) * math.cos(math.radians(60 * i - 30)),
         cy + (r_outer + 16) * math.sin(math.radians(60 * i - 30)))
        for i in range(6)
    ]
    glow_draw.polygon(pts_glow, fill=(0, 210, 255, 60))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=20))
    img.paste(glow_img, (0, 0), glow_img)

    # 2. Outer Hexagonal Shield
    pts_outer = [
        (cx + r_outer * math.cos(math.radians(60 * i - 30)),
         cy + r_outer * math.sin(math.radians(60 * i - 30)))
        for i in range(6)
    ]
    # Gradient border
    draw.polygon(pts_outer, fill=(20, 27, 40, 255), outline=(0, 210, 255, 255), width=18)

    # 3. Inner Shield Plate
    pts_inner = [
        (cx + r_inner * math.cos(math.radians(60 * i - 30)),
         cy + r_inner * math.sin(math.radians(60 * i - 30)))
        for i in range(6)
    ]
    draw.polygon(pts_inner, fill=(13, 17, 24, 255), outline=(37, 99, 235, 255), width=8)

    # 4. Silicon CPU Die in the center
    die_size = int(size * 0.32)
    die_x0 = cx - die_size // 2
    die_y0 = cy - die_size // 2
    die_x1 = cx + die_size // 2
    die_y1 = cy + die_size // 2

    # Circuit traces extending outward
    trace_len = int(size * 0.12)
    trace_color = (0, 210, 255, 200)
    gold_node = (16, 185, 129, 255)

    # Horizontal & Vertical traces
    for offset in [-80, 0, 80]:
        # Left
        draw.line([(die_x0, cy + offset), (die_x0 - trace_len, cy + offset)], fill=trace_color, width=6)
        draw.ellipse([die_x0 - trace_len - 8, cy + offset - 8, die_x0 - trace_len + 8, cy + offset + 8], fill=gold_node)
        # Right
        draw.line([(die_x1, cy + offset), (die_x1 + trace_len, cy + offset)], fill=trace_color, width=6)
        draw.ellipse([die_x1 + trace_len - 8, cy + offset - 8, die_x1 + trace_len + 8, cy + offset + 8], fill=gold_node)
        # Top
        draw.line([(cx + offset, die_y0), (cx + offset, die_y0 - trace_len)], fill=trace_color, width=6)
        draw.ellipse([cx + offset - 8, die_y0 - trace_len - 8, cx + offset + 8, die_y0 - trace_len + 8], fill=gold_node)
        # Bottom
        draw.line([(cx + offset, die_y1), (cx + offset, die_y1 + trace_len)], fill=trace_color, width=6)
        draw.ellipse([cx + offset - 8, die_y1 + trace_len - 8, cx + offset + 8, die_y1 + trace_len + 8], fill=gold_node)

    # Draw CPU Die Box
    draw.rounded_rectangle([die_x0, die_y0, die_x1, die_y1], radius=24, fill=(24, 33, 49, 255), outline=(0, 210, 255, 255), width=8)

    # 5. Bold Dynamic Cyber "X"
    # Diagonal 1: Top-Left to Bottom-Right
    x_w = int(size * 0.08)
    d = int(die_size * 0.7)
    draw.line([(cx - d, cy - d), (cx + d, cy + d)], fill=(255, 255, 255, 255), width=x_w)
    # Diagonal 2: Top-Right to Bottom-Left
    draw.line([(cx + d, cy - d), (cx - d, cy + d)], fill=(0, 210, 255, 255), width=x_w)

    # Center pulse node
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(16, 185, 129, 255), outline=(255, 255, 255, 255), width=6)

    # 6. Green "64" Badge at bottom-right of the shield
    b_cx = cx + int(r_outer * 0.55)
    b_cy = cy + int(r_outer * 0.55)
    b_w, b_h = int(size * 0.22), int(size * 0.13)
    draw.rounded_rectangle([b_cx - b_w // 2, b_cy - b_h // 2, b_cx + b_w // 2, b_cy + b_h // 2], radius=16, fill=(16, 185, 129, 255), outline=(255, 255, 255, 255), width=6)

    # "64" Text
    try:
        font_64 = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", int(b_h * 0.7))
    except Exception:
        font_64 = ImageFont.load_default()
    draw.text((b_cx, b_cy), "64", fill=(13, 17, 24, 255), font=font_64, anchor="mm")

    return img

def create_full_logo(emblem_img):
    """Creates an 800x220 banner logo with emblem + modern typography."""
    w, h = 840, 220
    banner = Imagenew = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    # Resize emblem
    emb_size = 190
    emb = emblem_img.resize((emb_size, emb_size), Image.Resampling.LANCZOS)
    banner.paste(emb, (16, (h - emb_size) // 2), emb)

    draw = ImageDraw.Draw(banner)
    text_x = emb_size + 36

    # Typography
    try:
        font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 68)
        font_64 = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)
        font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 18)
        font_desc = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_64 = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_desc = ImageFont.load_default()

    # Title "XUiDa"
    draw.text((text_x, 42), "XUiDa", fill=(255, 255, 255, 255), font=font_title)
    
    # "64" badge
    badge_x = text_x + 235
    badge_y = 52
    draw.rounded_rectangle([badge_x, badge_y, badge_x + 64, badge_y + 44], radius=8, fill=(16, 185, 129, 255))
    draw.text((badge_x + 32, badge_y + 22), "64", fill=(13, 17, 24, 255), font=font_64, anchor="mm")

    # Subtitle "EXTREME EDITION"
    draw.text((text_x + 2, 126), "EXTREME EDITION", fill=(0, 210, 255, 255), font=font_sub)

    # Description
    draw.text((text_x + 2, 156), "OPEN HARDWARE DIAGNOSTICS & BENCHMARK SUITE", fill=(156, 163, 175, 255), font=font_desc)

    return banner

def create_compact_logo(emblem_img):
    """Creates a 260x54 compact header logo for the sidebar."""
    w, h = 260, 54
    banner = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    emb_size = 46
    emb = emblem_img.resize((emb_size, emb_size), Image.Resampling.LANCZOS)
    banner.paste(emb, (6, (h - emb_size) // 2), emb)

    draw = ImageDraw.Draw(banner)
    text_x = emb_size + 14

    try:
        font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)
        font_64 = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 13)
        font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 10)
    except Exception:
        font_title = ImageFont.load_default()
        font_64 = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((text_x, 10), "XUiDa", fill=(255, 255, 255, 255), font=font_title)

    badge_x = text_x + 72
    badge_y = 12
    draw.rounded_rectangle([badge_x, badge_y, badge_x + 26, badge_y + 18], radius=4, fill=(16, 185, 129, 255))
    draw.text((badge_x + 13, badge_y + 9), "64", fill=(13, 17, 24, 255), font=font_64, anchor="mm")

    draw.text((text_x, 34), "EXTREME EDITION", fill=(0, 210, 255, 255), font=font_sub)

    return banner

def main():
    os.makedirs("assets", exist_ok=True)
    print("Generating high-res emblem...")
    emblem_1024 = create_emblem(1024)

    # 1. assets/icon.png (512x512)
    icon_512 = emblem_1024.resize((512, 512), Image.Resampling.LANCZOS)
    icon_512.save("assets/icon.png", "PNG")
    print("Saved: assets/icon.png")

    # 2. assets/icon.ico (multi-resolution Windows ICO)
    ico_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    ico_imgs = [emblem_1024.resize(sz, Image.Resampling.LANCZOS) for sz in ico_sizes]
    ico_imgs[0].save("assets/icon.ico", format="ICO", sizes=ico_sizes)
    print("Saved: assets/icon.ico")

    # 3. assets/logo.png
    full_logo = create_full_logo(emblem_1024)
    full_logo.save("assets/logo.png", "PNG")
    print("Saved: assets/logo.png")

    # 4. assets/logo_small.png
    small_logo = create_compact_logo(emblem_1024)
    small_logo.save("assets/logo_small.png", "PNG")
    print("Saved: assets/logo_small.png")

    print("All branding assets generated successfully!")

if __name__ == "__main__":
    main()
