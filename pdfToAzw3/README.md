# PDF to AZW3 Converter

Convert PDF files to Amazon Kindle AZW3 format using Calibre's `ebook-convert` tool.

## Prerequisites

### Calibre Installation

This script requires **Calibre** to be installed on your system.

#### Windows
- **Option 1:** Download installer from https://calibre-ebook.com/download
- **Option 2:** Using Chocolatey: `choco install calibre`
- **Option 3:** Using WinGet: `winget install -e --id Calibre.Calibre`

#### macOS
```bash
brew install calibre
```

#### Linux
- **Ubuntu/Debian:** `sudo apt-get install calibre`
- **Fedora:** `sudo dnf install calibre`
- **Arch:** `sudo pacman -S calibre`

After installation, ensure `ebook-convert` is available in your PATH.

## Usage

### Method 1: Python Script - Batch Conversion (Recommended)

```bash
# Interactive mode - prompts for folder path
python convert_pdf_to_azw3.py

# Direct mode - pass folder path as argument
python convert_pdf_to_azw3.py "C:\Users\Me\Documents\PDFs"
```

The script will:
1. Ask for (or accept) the folder path
2. Verify the folder exists
3. Find all PDF files in the folder
4. Convert each PDF to AZW3
5. Display a summary of all converted files

### Method 2: Batch Script (Windows)

```cmd
REM Convert all PDFs in a folder
convert.cmd "C:\Users\Me\Documents\PDFs"
```

### Method 3: Command Line (Direct)

```bash
ebook-convert input.pdf output.azw3
```

## Examples

### Basic batch conversion (interactive)
```bash
python convert_pdf_to_azw3.py
# When prompted, enter: C:\Users\Me\Documents\PDFs
```

### Batch conversion with folder path
```bash
python convert_pdf_to_azw3.py "C:\Users\Me\Documents\PDFs"
```

### Output example
```
PDF to AZW3 Batch Converter
============================================================
Found 3 PDF file(s) to convert

============================================================

[1/3] Converting: book1.pdf
Converting: C:\Users\Me\Documents\book1.pdf
Output: C:\Users\Me\Documents\book1.azw3
--------------------------------------------------
✓ Conversion successful!
Output file: C:\Users\Me\Documents\book1.azw3

[2/3] Converting: book2.pdf
Converting: C:\Users\Me\Documents\book2.pdf
Output: C:\Users\Me\Documents\book2.azw3
--------------------------------------------------
✓ Conversion successful!
Output file: C:\Users\Me\Documents\book2.azw3

[3/3] Converting: book3.pdf
Converting: C:\Users\Me\Documents\book3.pdf
Output: C:\Users\Me\Documents\book3.azw3
--------------------------------------------------
✓ Conversion successful!
Output file: C:\Users\Me\Documents\book3.azw3

============================================================
CONVERSION SUMMARY
============================================================

✓ Successfully converted 3 file(s):

  1. book1.azw3
     Location: C:\Users\Me\Documents\book1.azw3
  2. book2.azw3
     Location: C:\Users\Me\Documents\book2.azw3
  3. book3.azw3
     Location: C:\Users\Me\Documents\book3.azw3
```

## Conversion Options

Both scripts use the following default options:
- **Paper Size:** A4
- **Margins:** 5mm on all sides

### Custom Options

To customize the conversion, edit the scripts and modify these parameters in the `ebook-convert` command:

| Option | Description | Example |
|--------|-------------|---------|
| `--paper-size` | Paper size (a4, letter, etc.) | `--paper-size=a4` |
| `--margin-left` | Left margin in mm | `--margin-left=10` |
| `--margin-right` | Right margin in mm | `--margin-right=10` |
| `--margin-top` | Top margin in mm | `--margin-top=10` |
| `--margin-bottom` | Bottom margin in mm | `--margin-bottom=10` |
| `--colors` | Colorize black & white PDFs | `--colors` |

For more options, run:
```bash
ebook-convert --help
```

## Examples

### Basic conversion
```bash
python convert_pdf_to_azw3.py "C:\Users\Me\Documents\book.pdf"
```

### With custom output location
```bash
python convert_pdf_to_azw3.py "C:\Users\Me\Documents\book.pdf" "C:\Users\Me\Kindle\book.azw3"
```

### Batch processing
```bash
for %%F in (*.pdf) do python convert_pdf_to_azw3.py "%%F"
```

## Troubleshooting

### "ebook-convert is not installed or not in PATH"
- Verify Calibre is installed: Open Calibre application
- Check PATH: Run `ebook-convert --version` in terminal/command prompt
- If command not found, add Calibre to PATH:
  - **Windows:** Usually at `C:\Program Files\Calibre2\` (add to System Environment Variables)

### Conversion quality issues
- Try reducing margins or adjusting paper size
- Some PDFs with complex layouts may not convert perfectly
- Consider OCR if the PDF is image-based

### Output file is empty or corrupted
- Check source PDF is valid and not encrypted
- Try converting with command line directly to see detailed error messages

## Technical Details

- **Conversion Engine:** Calibre (ebook-convert)
- **Output Format:** AZW3 (Amazon Kindle 8+ format)
- **Supported Input:** PDF, EPUB, MOBI, HTML, and many others
- **Performance:** Typical conversion takes 5-30 seconds depending on file size

## License

These scripts are provided as-is for personal use. Calibre is open-source under the GPLv3 license.

## Additional Resources

- [Calibre Documentation](https://calibre-ebook.com/help)
- [AZW3 Format Information](https://en.wikipedia.org/wiki/Kindle_File_Format)
- [ebook-convert Manual](https://manual.calibre-ebook.com/ebook-convert.html)
