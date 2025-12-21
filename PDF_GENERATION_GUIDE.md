# 📄 PDF Documentation Guide (Mac - No LaTeX)

## ✅ Solution Created!

I've created a simple, Mac-friendly way to generate PDF documentation without requiring LaTeX or any complex setup.

---

## 🚀 Quick Start

Just run:

```bash
make docs-pdf
```

That's it! A browser window will open with instructions.

---

## 📖 How It Works

### Step 1: Generate Print-Friendly HTML

The `create_pdf.py` script:
1. Collects all your documentation pages
2. Combines them into a single HTML file
3. Adds print-optimized CSS styling
4. Opens it in your default browser

### Step 2: Save as PDF (Built-in Mac Feature)

Once the browser opens:

1. **Press `Cmd+P`** (or go to File → Print)
2. **Click the "PDF" dropdown** (bottom-left corner of print dialog)
3. **Select "Save as PDF"**
4. **Choose a location** and save

**That's it!** No LaTeX, no complex tools needed.

---

## 🎨 What's Included in the PDF

The generated PDF will contain:

✅ **Complete API Reference** - All 66+ functions  
✅ **Dependencies and Packages** - All packages used  
✅ **Module Documentation** - Callbacks, Components, Pages, Utils  
✅ **Class Documentation** - All classes with methods  
✅ **Examples** - Code examples for all functions  
✅ **Professional Formatting** - Page breaks, headers, code blocks  

---

## 📐 PDF Styling Features

### Print Optimizations:

- **A4 Page Size** with 2cm margins
- **Smart Page Breaks** - Headers avoid orphans
- **Code Block Formatting** - Monospace font, backgrounds
- **Section Organization** - Clear hierarchy
- **Table of Contents** - Navigation structure
- **Professional Typography** - Optimized for print

### What Gets Hidden:

- Navigation sidebars
- Instruction boxes
- Screen-only elements

### What's Enhanced:

- Function signatures in code font
- Parameters clearly formatted
- Return values highlighted
- Examples in gray boxes
- Cross-references maintained

---

## 🔧 Files Created

### 1. `create_pdf.py`
Main script that generates the print-friendly HTML.

**Features:**
- Collects all documentation pages
- Combines into single HTML
- Adds print CSS
- Opens in browser automatically

### 2. Updated `Makefile`
Added `make docs-pdf` command for easy access.

### 3. Updated `docs/README.md`
Added complete PDF generation instructions.

---

## 💻 Usage Examples

### Generate PDF
```bash
make docs-pdf
```

### Or run directly
```bash
python create_pdf.py
```

### Or from docs directory
```bash
cd /Users/josephsoukup/PycharmProjects/quality-of-prague
python create_pdf.py
```

---

## 📋 Step-by-Step Instructions

### Method 1: Using Make (Recommended)

```bash
# From project root
make docs-pdf

# Browser opens automatically
# Press Cmd+P
# Save as PDF
```

### Method 2: Manual

```bash
# 1. Generate the HTML
python create_pdf.py

# 2. Browser opens with the HTML
# 3. Press Cmd+P (or File → Print)
# 4. PDF dropdown → Save as PDF
# 5. Choose location and save
```

---

## 🎯 Output Location

### Print-Friendly HTML
```
docs/Quality_of_Prague_Documentation_Print.html
```

This file:
- Contains ALL your documentation
- Is optimized for printing
- Has instructions at the top (won't appear in PDF)
- Opens automatically in your browser

### Your PDF
You choose where to save it! Recommended name:
```
Quality_of_Prague_Documentation.pdf
```

---

## ✨ Advantages of This Method

✅ **No LaTeX Required** - Uses Mac's built-in PDF engine  
✅ **No Extra Software** - Just Python and your browser  
✅ **Simple** - One command: `make docs-pdf`  
✅ **Professional** - Proper formatting and page breaks  
✅ **Complete** - All documentation in one PDF  
✅ **Customizable** - Edit `create_pdf.py` to adjust styling  
✅ **Fast** - Generates in seconds  
✅ **Reliable** - Uses browser's print engine  

---

## 🎨 Customization

Want to customize the PDF appearance? Edit `create_pdf.py`:

### Change Page Size
```python
@page {
    size: Letter;  # or A4, Legal
    margin: 1.5cm;
}
```

### Adjust Fonts
```python
body {
    font-family: "Times New Roman", serif;
    font-size: 11pt;
}
```

### Modify Colors
```python
h1 {
    color: #1a1a1a;
}
```

---

## 🐛 Troubleshooting

### Browser doesn't open?
```bash
# Open manually
open docs/Quality_of_Prague_Documentation_Print.html
```

### Can't find the PDF option?
Make sure you're in the Print dialog, then look for a "PDF" button or dropdown in the bottom-left corner.

### PDF looks different?
Use Safari or Chrome for best results. Firefox may have different print rendering.

### Want higher quality?
In the print dialog, look for "Quality" or "Print Quality" settings and select "Best" or "High".

---

## 📊 What Your PDF Will Contain

### Main Sections:

1. **Project Overview**
   - Description
   - Technology stack

2. **Dependencies and Packages**
   - All packages used
   - Installation instructions
   - Version information

3. **API Reference**
   - Callbacks module
   - Components module
   - Pages module
   - Utilities module
   - Configuration module

4. **For Each Module:**
   - Module description
   - All functions with:
     - Signatures
     - Parameters
     - Return values
     - Examples

---

## 🎉 Summary

You now have a simple, one-command solution to create PDF documentation:

```bash
make docs-pdf
```

No LaTeX, no complex setup, just your Mac's built-in print-to-PDF feature!

**The print-friendly HTML has been created and opened in your browser.** 

Follow the on-screen instructions to save as PDF! 📄

---

*Created: December 21, 2025*  
*Method: Mac Print-to-PDF (No LaTeX Required)*  
*Documentation: Complete with 66+ functions*

