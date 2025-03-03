```
# og-creator

**og-creator** is a Python CLI tool that automatically generates key image assets for your website—favicon, logos, and an OG preview image—from a single input logo. No more manual resizing for OG previews, logos, or favicons.

---

## **Features**

- **Automated Image Asset Generation**
  - Accepts a logo image (JPG/JPEG, PNG, SVG) in any size.
  - Generates:
    - `favicon.ico` (48×48)
    - A 40×40 logo (`logo_40.png`)
    - An 80×80 retina logo (`logo_80.png`)
    - A 1200×630 OG image (`og_image.jpg`), optimized to be under 300KB.
- **Smart Output Directory Handling**
  - If a `public` directory exists in the current working directory, assets are saved there.
  - Otherwise, a new `og-images` directory is created (aborting if it already exists).

---

## **Prerequisites**

- [Pillow](https://pypi.org/project/Pillow/)
- [cairosvg](https://pypi.org/project/CairoSVG/) (required for SVG processing)

---

## **Installation Steps**

1. **Clone the Repository** (e.g., to `~/projects/og-creator`):
   ```bash
   git clone https://github.com/<your-github-handle>/og-creator.git
   cd og-creator
   ```

2. **Create a Virtual Environment (optional but recommended)**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Make the Script Executable and Symlink It**:
   ```bash
   chmod +x og-creator.py
   ln -s ~/projects/og-creator/og-creator.py ~/.local/bin/og-creator
   ```
   - Ensure `~/.local/bin` is in your PATH and run:
     ```bash
     source ~/.bashrc
     ```

---

## **Usage**

### **Generate Image Assets**

Run the tool with your logo image as an argument:
```bash
og-creator path/to/your/logo.png
```
This command will generate:
- A `favicon.ico` (48×48)  
- A 40×40 logo (`logo_40.png`)  
- An 80×80 retina logo (`logo_80.png`)  
- A 1200×630 OG image (`og_image.jpg` optimized to be under 300KB)

*Output Directory Logic:*
- If a `public` directory is found in the current working directory, assets are saved there.
- Otherwise, a new `og-images` directory is created.

---

## **Credits**

Developed in quick collaboration with OpenAI's o3-mini-high model because I was tired of creating custom image sizes for OG previews, logos, and favicons.

---

## **License**

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
```
