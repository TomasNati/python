#!/usr/bin/env python3
"""
Convert PDF files to AZW3 format using Calibre's ebook-convert tool.
"""

import sys
import os
import subprocess
from pathlib import Path


def check_calibre_installed():
    """Check if Calibre's ebook-convert is installed."""
    try:
        result = subprocess.run(
            ["ebook-convert", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def convert_pdf_to_azw3(pdf_path, output_path=None):
    """
    Convert a PDF file to AZW3 format.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_path (str, optional): Path for the output AZW3 file.
                                    If not provided, uses same name with .azw3 extension
    
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    pdf_path = Path(pdf_path)
    
    # Validate input file exists
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return False
    
    if not pdf_path.suffix.lower() == ".pdf":
        print(f"Error: Input file must be a PDF: {pdf_path}")
        return False
    
    # Determine output path
    if output_path is None:
        output_path = pdf_path.with_suffix(".azw3")
    else:
        output_path = Path(output_path)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting: {pdf_path}")
    print(f"Output: {output_path}")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            [
                "ebook-convert",
                str(pdf_path),
                str(output_path),
                "--margin-left=5",
                "--margin-right=5",
                "--margin-top=5",
                "--margin-bottom=5",
            ],
            timeout=300
        )
        
        if result.returncode == 0:
            print("-" * 50)
            print(f"✓ Conversion successful!")
            print(f"Output file: {output_path}")
            return True
        else:
            print("-" * 50)
            print(f"✗ Conversion failed with return code: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ Conversion timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"✗ Error during conversion: {e}")
        return False


def batch_convert_folder(folder_path):
    """
    Convert all PDF files in a folder to AZW3 format.
    
    Args:
        folder_path (str): Path to the folder containing PDFs
    
    Returns:
        list: List of successfully converted files
    """
    folder_path = Path(folder_path)
    
    # Verify folder exists
    if not folder_path.exists():
        print(f"Error: Folder does not exist: {folder_path}")
        return []
    
    if not folder_path.is_dir():
        print(f"Error: Path is not a folder: {folder_path}")
        return []
    
    # Find all PDF files
    pdf_files = sorted(folder_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in: {folder_path}")
        return []
    
    print(f"Found {len(pdf_files)} PDF file(s) to convert\n")
    print("=" * 60)
    
    converted_files = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        output_file = pdf_file.with_suffix(".azw3")
        
        print(f"\n[{i}/{len(pdf_files)}] Converting: {pdf_file.name}")
        
        if convert_pdf_to_azw3(str(pdf_file), str(output_file)):
            converted_files.append(output_file)
        else:
            print(f"      ✗ Failed to convert: {pdf_file.name}")
    
    return converted_files


def main():
    """Main entry point."""
    if not check_calibre_installed():
        print("Error: Calibre's ebook-convert is not installed or not in PATH")
        print("\nTo install Calibre:")
        print("  - Windows: Download from https://calibre-ebook.com/download")
        print("  - Or use: choco install calibre (if using Chocolatey)")
        print("  - Or use: winget install -e --id Calibre.Calibre (if using WinGet)")
        sys.exit(1)
    
    # Check if folder path provided as argument
    if len(sys.argv) >= 2:
        folder_path = sys.argv[1]
    else:
        # Prompt user for folder path
        print("PDF to AZW3 Batch Converter")
        print("=" * 60)
        folder_path = input("Enter the folder path containing PDF files: ").strip()
        
        if not folder_path:
            print("Error: No path provided")
            sys.exit(1)
    
    # Convert all PDFs in the folder
    converted_files = batch_convert_folder(folder_path)
    
    # Display results
    print("\n" + "=" * 60)
    print("CONVERSION SUMMARY")
    print("=" * 60)
    
    if converted_files:
        print(f"\n✓ Successfully converted {len(converted_files)} file(s):\n")
        for i, file_path in enumerate(converted_files, 1):
            print(f"  {i}. {file_path.name}")
            print(f"     Location: {file_path}")
        print()
        sys.exit(0)
    else:
        print("\n✗ No files were successfully converted")
        sys.exit(1)


if __name__ == "__main__":
    main()
