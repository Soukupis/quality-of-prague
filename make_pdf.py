#!/usr/bin/env python3
"""PDF generator that extracts complete Sphinx documentation."""

import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Setup paths
script_dir = Path(__file__).parent
docs_dir = script_dir / "docs"
html_dir = docs_dir / "build" / "html"
output_file = docs_dir / "Quality_of_Prague_Documentation_Print.html"

print(f"Script directory: {script_dir}")
print(f"HTML directory: {html_dir}")
print(f"Output file: {output_file}")

# Check if docs exist
if not html_dir.exists():
    print("\n❌ Error: Documentation not built!")
    print("Please run: make docs")
    sys.exit(1)

print(f"\n✅ Found documentation at: {html_dir}")

# Pages to include
pages_to_extract = [
    ("index.html", "Overview"),
    ("packages.html", "Dependencies and Packages"),
    ("modules/callbacks.html", "Callbacks Module"),
    ("modules/components.html", "Components Module"),
    ("modules/pages.html", "Pages Module"),
    ("modules/utils.html", "Utilities Module"),
    ("modules/configs.html", "Configuration Module"),
]

print(f"\n📖 Extracting content from {len(pages_to_extract)} pages...")

# Extract content from each page
all_content = []

for page_file, page_title in pages_to_extract:
    page_path = html_dir / page_file
    if not page_path.exists():
        print(f"   ⚠️  Skipping {page_file} (not found)")
        continue

    print(f"   📄 Reading {page_file}...")

    try:
        with open(page_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

            # Find the main content section
            content = soup.find('div', class_='document')
            if not content:
                content = soup.find('section')
            if not content:
                content = soup.find('div', role='main')

            if content:
                # Remove navigation elements
                for nav in content.find_all(['nav', 'div'], class_=['sphinxsidebar', 'related']):
                    nav.decompose()

                # Add page title
                content_html = f'<div class="page-section">\n<h1 class="page-title">{page_title}</h1>\n{str(content)}\n</div>\n'
                all_content.append(content_html)
                print(f"      ✅ Extracted content")
            else:
                print(f"      ⚠️  No content found")
    except Exception as e:
        print(f"      ❌ Error: {e}")

if not all_content:
    print("\n❌ No content extracted!")
    sys.exit(1)

print(f"\n✅ Extracted {len(all_content)} sections")

# Create HTML with CSS as a separate string
css_content = """
        @media screen {
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
                max-width: 1000px;
                margin: 40px auto;
                padding: 20px;
                line-height: 1.6;
                color: #333;
            }
            .instructions {
                background: #e3f2fd;
                border-left: 4px solid #2196f3;
                padding: 20px;
                margin: 20px 0;
                border-radius: 4px;
            }
            .instructions h2 {
                margin-top: 0;
                color: #1976d2;
            }
        }
        
        @media print {
            .instructions { display: none !important; }
            @page { 
                size: A4;
                margin: 2cm;
            }
            body {
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 10pt;
                line-height: 1.5;
                color: #000;
            }
            .page-section {
                page-break-before: always;
            }
            .page-section:first-of-type {
                page-break-before: avoid;
            }
            h1, .page-title {
                font-size: 20pt;
                margin-top: 0;
                color: #2c3e50;
                page-break-after: avoid;
            }
            h2 {
                font-size: 16pt;
                margin-top: 0.8cm;
                color: #34495e;
                page-break-after: avoid;
            }
            h3 {
                font-size: 13pt;
                margin-top: 0.5cm;
                color: #5d6d7e;
            }
            h4 {
                font-size: 11pt;
                margin-top: 0.4cm;
                color: #7f8c8d;
            }
            code, .sig-name {
                font-family: "Courier New", Courier, monospace;
                font-size: 9pt;
                background: #f5f5f5;
                padding: 1px 3px;
            }
            pre, .highlight {
                font-family: "Courier New", Courier, monospace;
                font-size: 8pt;
                background: #f8f9fa;
                padding: 8px;
                border: 1px solid #dee2e6;
                overflow: auto;
                page-break-inside: avoid;
                margin: 0.3cm 0;
            }
            dl {
                margin: 0.3cm 0;
            }
            dt {
                font-weight: bold;
                margin-top: 0.2cm;
            }
            dd {
                margin-left: 1.5cm;
                margin-bottom: 0.2cm;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 0.3cm 0;
                page-break-inside: avoid;
                font-size: 9pt;
            }
            th, td {
                border: 1px solid #dee2e6;
                padding: 0.2cm;
                text-align: left;
            }
            th {
                background: #f8f9fa;
                font-weight: bold;
            }
            a {
                color: #000;
                text-decoration: none;
            }
            nav, .sidebar, .related, .sphinxsidebar {
                display: none !important;
            }
        }
        
        h1, h2, h3, h4 {
            font-weight: 600;
        }
        code {
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
        }
        pre {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        .page-section {
            margin-bottom: 2em;
        }
"""

# Build the complete HTML
html_parts = [
    '<!DOCTYPE html>\n<html>\n<head>\n',
    '    <meta charset="utf-8">\n',
    '    <title>Quality of Prague - Complete Documentation</title>\n',
    '    <style>\n',
    css_content,
    '    </style>\n</head>\n<body>\n',
    '    <div class="instructions">\n',
    '        <h2>📄 Create PDF (Mac)</h2>\n',
    '        <ol>\n',
    '            <li><strong>Press Cmd+P</strong> (or File → Print)</li>\n',
    '            <li><strong>Click "PDF"</strong> dropdown (bottom-left)</li>\n',
    '            <li><strong>Select "Save as PDF"</strong></li>\n',
    '            <li><strong>Save!</strong></li>\n',
    '        </ol>\n',
    '        <p><strong>Note:</strong> This instruction box will not appear in the PDF.</p>\n',
    '    </div>\n\n',
]

html_parts.extend(all_content)

html_parts.extend([
    '\n    <hr style="margin-top: 2cm; page-break-before: avoid;">\n',
    '    <footer style="text-align: center; color: #666; font-size: 9pt; page-break-before: avoid;">\n',
    '        <p><em>Quality of Prague Documentation | Generated December 21, 2025</em></p>\n',
    '    </footer>\n',
    '</body>\n</html>'
])

html_content = ''.join(html_parts)

# Write the file
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    file_size = output_file.stat().st_size
    print(f"\n✅ Created: {output_file}")
    print(f"   Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
except Exception as e:
    print(f"\n❌ Error writing file: {e}")
    sys.exit(1)

# Open in browser
print(f"\n📌 Opening in browser...")
import subprocess
try:
    subprocess.run(['open', str(output_file)], check=True)
    print(f"\n🖨️  Instructions:")
    print(f"   1. Press Cmd+P")
    print(f"   2. PDF → Save as PDF")
    print(f"   3. Done!")
except Exception as e:
    print(f"❌ Error opening browser: {e}")
    print(f"Please manually open: {output_file}")

print(f"\n✅ Complete!")

