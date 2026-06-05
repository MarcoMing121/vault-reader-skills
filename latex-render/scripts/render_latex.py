#!/usr/bin/env python3
"""
Render LaTeX formulas to PNG images.
Uses CodeCogs LaTeX rendering service.
"""

import argparse
import urllib.parse
import urllib.request
import os
import sys
from datetime import datetime
import hashlib
from pathlib import Path

# Import config
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_shared"))
from user_config import latex_cache_path

# CodeCogs LaTeX rendering service
CODECOGS_URL = "https://latex.codecogs.com/png.latex"


def render_latex(latex_code: str, output_path: str, dpi: int = 200, padding: int = 10) -> bool:
    """
    Render LaTeX code to a PNG image.
    
    Args:
        latex_code: LaTeX formula string
        output_path: Path to save the PNG file
        dpi: Resolution (higher = larger image)
        padding: Padding around formula in pixels
    
    Returns:
        True if successful, False otherwise
    """
    styled_latex = f'\\dpi{{{dpi}}}\\bg{{white}} {latex_code}'
    encoded_latex = urllib.parse.quote(styled_latex, safe='')
    url = f"{CODECOGS_URL}?{encoded_latex}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status != 200:
                print(f"Error: HTTP {response.status}", file=sys.stderr)
                return False
            
            image_data = response.read()
            
            if not image_data.startswith(b'\x89PNG'):
                print("Error: Response is not a valid PNG image", file=sys.stderr)
                return False
            
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            return True
            
    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Render LaTeX formulas to PNG images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s '\\int_0^\\infty e^{-x^2} dx'
  %(prog)s '\\frac{a}{b}' --dpi 300
  %(prog)s '$$E = mc^2$$' -o /custom/path.png

Default output: {LATEX_CACHE_PATH}/formula_<timestamp>.png
        '''.format(LATEX_CACHE_PATH=latex_cache_path())
    )
    
    parser.add_argument('latex', help='LaTeX code to render')
    parser.add_argument('-o', '--output', default=None, help='Output PNG file path (default: latex-cache)')
    parser.add_argument('--dpi', type=int, default=200, help='Image resolution (default: 200)')
    parser.add_argument('--padding', type=int, default=10, help='Padding in pixels (default: 10)')
    
    args = parser.parse_args()
    
    # Strip $$ delimiters if present
    latex = args.latex.strip()
    if latex.startswith('$$') and latex.endswith('$$'):
        latex = latex[2:-2].strip()
    elif latex.startswith('$') and latex.endswith('$'):
        latex = latex[1:-1].strip()
    
    # Generate default output path if not specified
    if args.output is None:
        latex_hash = hashlib.md5(latex.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"formula_{timestamp}_{latex_hash}.png"
        output_path = str(latex_cache_path() / filename)
    else:
        output_path = args.output
    
    print(f"Rendering: {latex}")
    print(f"Output: {output_path}")
    
    if render_latex(latex, output_path, args.dpi, args.padding):
        print(f"Success! Image saved to {output_path}")
        return 0
    else:
        print("Failed to render LaTeX", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
