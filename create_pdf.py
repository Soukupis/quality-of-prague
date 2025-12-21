#!/usr/bin/env python3
"""
PDF Generation Script for Quality of Prague Documentation (Mac - No LaTeX Required)

This script creates a print-friendly single-page HTML that you can convert to PDF
using your Mac's built-in print functionality (Cmd+P → Save as PDF).
"""

from pathlib import Path
import re
import sys

def collect_documentation():
    """Collect all documentation pages into a single HTML."""

    docs_dir = Path(__file__).parent / "docs"
    html_dir = docs_dir / "build" / "html"

    if not html_dir.exists():
        print("❌ Error: Documentation not built yet!")
        print("Please run: make docs")
        return False

    print(f"📂 Reading documentation from: {html_dir}")

    # Main pages to include
    pages = [
        "index.html",
        "packages.html",
        "modules/index.html",
        "modules/callbacks.html",
        "modules/components.html",
        "modules/configs.html",
        "modules/pages.html",
        "modules/utils.html",
    ]

    # Collect content from each page
    content_sections = []

    for page in pages:
        page_path = html_dir / page
        print(f"   Reading: {page}")
        if page_path.exists():
            try:
                with open(page_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    # Extract main content - try different patterns
                    # Pattern 1: document div
                    match = re.search(r'<div class="document"[^>]*>(.*?)</div>\s*<div class="sphinxsidebar"',
                                    html_content, re.DOTALL)
                    if not match:
                        # Pattern 2: body content
                        match = re.search(r'<section[^>]*>(.*?)</section>', html_content, re.DOTALL)

                    if match:
                        content_sections.append(f"<!-- Content from {page} -->\n{match.group(1)}\n")
                    else:
                        print(f"   ⚠️  Warning: Could not extract content from {page}")
            except Exception as e:
                print(f"   ❌ Error reading {page}: {e}")
        else:
            print(f"   ⚠️  Not found: {page}")

    if not content_sections:
        print("❌ Error: No content sections found!")
        return False

    print(f"\n✅ Collected {len(content_sections)} sections")

    # Create print-friendly HTML
    output_html = docs_dir / "Quality_of_Prague_Documentation_Print.html"

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Quality of Prague - Complete Documentation</title>
    <style>
        /* Screen Styles */
        @media screen {{
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                line-height: 1.6;
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
                color: #333;
                background: #fff;
            }}
            .print-instructions {{
                background: #e3f2fd;
                border-left: 4px solid #2196f3;
                padding: 20px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .print-instructions h2 {{
                margin-top: 0;
                color: #1976d2;
            }}
            code {{
                background: #f5f5f5;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: "SF Mono", Monaco, "Courier New", monospace;
            }}
        }}
        
        /* Print Styles */
        @media print {{
            .print-instructions {{
                display: none !important;
            }}
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 10pt;
                line-height: 1.5;
                color: #000;
            }}
            h1 {{
                font-size: 20pt;
                page-break-before: always;
                margin-top: 1.5cm;
                color: #2c3e50;
            }}
            h1:first-of-type {{
                page-break-before: avoid;
            }}
            h2 {{
                font-size: 16pt;
                margin-top: 1cm;
                color: #34495e;
                page-break-after: avoid;
            }}
            h3 {{
                font-size: 13pt;
                margin-top: 0.7cm;
                color: #5d6d7e;
            }}
            h4 {{
                font-size: 11pt;
                margin-top: 0.5cm;
                color: #7f8c8d;
            }}
            code {{
                font-family: "Courier New", Courier, monospace;
                font-size: 9pt;
                background: #f5f5f5;
                padding: 1px 3px;
                border: 1px solid #ddd;
            }}
            pre {{
                font-family: "Courier New", Courier, monospace;
                font-size: 8pt;
                background: #f8f9fa;
                padding: 8px;
                border: 1px solid #dee2e6;
                overflow: auto;
                page-break-inside: avoid;
                margin: 0.5cm 0;
            }}
            .highlight {{
                background: #f8f9fa;
                border-left: 3px solid #3b82f6;
                padding: 8px;
                page-break-inside: avoid;
            }}
            dl {{
                page-break-inside: avoid;
            }}
            dt {{
                font-weight: bold;
                margin-top: 0.3cm;
            }}
            dd {{
                margin-left: 1.5cm;
                margin-bottom: 0.3cm;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 0.5cm 0;
                page-break-inside: avoid;
            }}
            th, td {{
                border: 1px solid #dee2e6;
                padding: 0.3cm;
                text-align: left;
            }}
            th {{
                background: #f8f9fa;
                font-weight: bold;
            }}
            a {{
                color: #000;
                text-decoration: none;
            }}
            a[href]:after {{
                content: " (" attr(href) ")";
                font-size: 8pt;
                color: #666;
            }}
            nav, .sidebar, .related {{
                display: none;
            }}
        }}
        
        /* Common Styles */
        h1, h2, h3, h4 {{
            font-weight: 600;
        }}
        .section {{
            margin-bottom: 1.5em;
        }}
    </style>
</head>
<body>
    <div class="print-instructions">
        <h2>📄 How to Create PDF (Mac)</h2>
        <ol>
            <li><strong>Press Cmd+P</strong> (or File → Print)</li>
            <li><strong>Click the "PDF" dropdown</strong> in the bottom-left corner</li>
            <li><strong>Select "Save as PDF"</strong></li>
            <li><strong>Choose a location and save</strong></li>
        </ol>
        <p><strong>Note:</strong> This instruction box will not appear in the PDF.</p>
    </div>

    <div class="document">
        {''.join(content_sections)}
    </div>
    
    <hr style="margin-top: 2cm;">
    <footer style="text-align: center; color: #666; font-size: 9pt;">
        <p><em>Generated: December 21, 2025 | Quality of Prague Documentation</em></p>
    </footer>
</body>
</html>
"""

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"\n✅ Print-friendly HTML created!")
    print(f"📄 Location: {output_html}")
    print(f"\n📌 Opening in your default browser...")
    print(f"\n🖨️  To create PDF:")
    print(f"   1. Press Cmd+P (or File → Print)")
    print(f"   2. Click 'PDF' dropdown (bottom-left)")
    print(f"   3. Select 'Save as PDF'")
    print(f"   4. Choose location and save")

    # Open in default browser
    import subprocess
    subprocess.run(['open', str(output_html)])

    return True

if __name__ == "__main__":
    import sys
    success = collect_documentation()
    sys.exit(0 if success else 1)

