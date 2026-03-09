# EV100 — Electro-Voice Centennial Vision Board

137 images across 14 creative territories. A visual operating system for the EV100 centennial program.

**Live board:** https://markschwandt.github.io/ev100-vision-board/

---

## Self-Hosting the Images

The board currently loads images from Pinterest CDN. To move them to self-hosted local files:

### Prerequisites
```bash
pip install requests
```

### Run
```bash
git clone https://github.com/markschwandt/ev100-vision-board.git
cd ev100-vision-board
python3 scripts/download_images.py
```

The script will:
1. Download all 137 images into `images/{category}/` folders
2. Rewrite `index.html` to reference local paths instead of Pinterest CDN

### Commit
```bash
git add images/ index.html
git commit -m "feat: self-host all vision board images"
git push
```

---

## Image Categories

| Category | Images | Description |
|----------|--------|-------------|
| Immersive Sound Art | 10 | Where sound becomes visual art |
| Futuristic Stage Design | 10 | Tomorrow's stages, built for today's performers |
| Celebrations & Crowds | 8 | The energy of a hundred thousand voices |
| Brand Activation | 8 | Turning brand stories into unforgettable experiences |
| Bold Typography | 8 | Words that demand attention |
| Live Performance | 8 | Raw emotion, center stage |
| Spatial Audio | 8 | Sound that surrounds and transforms |
| Sound Engineers | 8 | The invisible artists behind every great sound |
| Festival Community | 8 | United by music, connected by sound |
| Light Experiences | 8 | Walking through light, sound, and space |
| Anniversary Branding | 9 | How the best brands honor milestones |
| Product Design | 16 | The art and craft of audio hardware |
| Experiential Installations | 15 | Immersive spaces that blur reality |
| Behind the Scenes | 13 | The magic that happens before the show |
