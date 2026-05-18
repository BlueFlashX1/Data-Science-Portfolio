#!/usr/bin/env python3
"""Export the AI4HC poster as a print-ready PDF at 48 in × 36 in landscape.

Pipeline:
  1. Render index_v1.html in headless Chrome with ?export=1 at a 4608×3456 viewport.
     CSS rule `body.export-mode` scales `.poster` 3.1× and centers it inside the
     window so panel shadows render fully (not clipped at the page edge).
  2. Save the screenshot as a PNG (4608×3456 px).
  3. Embed the PNG losslessly in a PDF via img2pdf at 96 DPI → 48×36 in exactly,
     with print-shop metadata (Title, Author, Subject, Keywords, Producer).

Usage:
  python3 export_poster.py                                # default html → default pdf
  python3 export_poster.py --out AI4HC_slide_poster.pdf   # custom output
  python3 export_poster.py --keep-png                     # keep intermediate PNG
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_HTML = ROOT / "index_v1.html"
DEFAULT_OUT  = ROOT / "AI4HC_poster_4x3ft_landscape.pdf"

# 48×36 in at 96 DPI = 4608×3456 px (matches body.export-mode CSS in index_v1.html)
PAGE_W_PX = 4608
PAGE_H_PX = 3456
DPI = 96

# Print-shop metadata (sRGB is assumed by default on US poster printers)
TEAM = [
    "Matthew Q. Lan Thompson",
    "Rishinath Reddy Enugala",
    "Abhiram Varma Nandimandalam",
    "Abhigyan Bommeria",
    "Usha Goud Gourigari",
]
PDF_TITLE    = "Emergency Room AI Simulator"
PDF_SUBJECT  = "iShowcase 2026 — University of Arizona College of Information Science"
PDF_AUTHOR   = ", ".join(TEAM)
PDF_KEYWORDS = ["ER simulator", "AI", "RAG", "MedGemma", "healthcare training", "iShowcase 2026"]
PDF_CREATOR  = "AI4HC scripts/export_poster.py"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]


def find_chrome() -> str:
    for path in CHROME_CANDIDATES:
        if path and Path(path).exists():
            return path
    sys.exit("ERROR: Chrome / Chromium not found. Install Google Chrome.")


def render_png(html_path: Path, png_path: Path) -> None:
    chrome = find_chrome()
    url = f"file://{html_path.resolve()}?export=1"
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={PAGE_W_PX},{PAGE_H_PX}",
        "--virtual-time-budget=8000",
        "--run-all-compositor-stages-before-draw",
        f"--screenshot={png_path}",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if not png_path.exists():
        sys.exit(f"ERROR: Chrome failed to write PNG.\n{result.stderr}")


def png_to_pdf(png_path: Path, pdf_path: Path) -> None:
    try:
        import img2pdf
    except ImportError:
        sys.exit("ERROR: img2pdf not installed. Run: pip3 install img2pdf")

    layout = img2pdf.get_fixed_dpi_layout_fun((DPI, DPI))
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(
            str(png_path),
            layout_fun=layout,
            title=PDF_TITLE,
            author=PDF_AUTHOR,
            subject=PDF_SUBJECT,
            keywords=PDF_KEYWORDS,
            creator=PDF_CREATOR,
            producer="img2pdf",
        ))


def main() -> int:
    p = argparse.ArgumentParser(description="Export AI4HC poster to print-ready PDF.")
    p.add_argument("--html", type=Path, default=DEFAULT_HTML, help=f"source HTML (default: {DEFAULT_HTML.name})")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"output PDF (default: {DEFAULT_OUT.name})")
    p.add_argument("--keep-png", action="store_true", help="keep the intermediate PNG next to the PDF")
    args = p.parse_args()

    if not args.html.exists():
        sys.exit(f"ERROR: HTML not found: {args.html}")

    if args.keep_png:
        png_path = args.out.with_suffix(".png")
        render_png(args.html, png_path)
        png_to_pdf(png_path, args.out)
        print(f"PNG: {png_path}")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            png_path = Path(tmp) / "poster.png"
            render_png(args.html, png_path)
            png_to_pdf(png_path, args.out)

    size_kb = args.out.stat().st_size / 1024
    print(f"PDF: {args.out}  ({size_kb:.0f} KB, 48×36 in, lossless)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
