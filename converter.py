import os
import argparse
from typing import List

from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze


def process_pdf(pdf_file_path: str, output_dir: str = "output") -> None:
    """
    Process a single PDF file and convert it to markdown
    
    Args:
        pdf_file_path: Path to the PDF file
        output_dir: Directory to save output files
    """
    pdf_file_name = os.path.basename(pdf_file_path)
    name_without_suff = pdf_file_name.split(".")[0]
    
    # Check if output file already exists
    output_file = os.path.join(output_dir, f"{name_without_suff}.md")
    if os.path.exists(output_file):
        print(f"Skipping {pdf_file_name} - already processed")
        return
    
    # prepare env
    local_image_dir = os.path.join(output_dir, "images")
    local_md_dir = output_dir
    image_dir = os.path.basename(local_image_dir)
    
    os.makedirs(local_image_dir, exist_ok=True)
    
    image_writer = FileBasedDataWriter(local_image_dir)
    md_writer = FileBasedDataWriter(local_md_dir)
    
    # read bytes
    reader = FileBasedDataReader(os.path.dirname(pdf_file_path))
    pdf_bytes = reader.read(os.path.basename(pdf_file_path))
    
    # process
    ds = PymuDocDataset(pdf_bytes)
    ds.apply(doc_analyze, ocr=True).pipe_ocr_mode(image_writer).dump_md(
        md_writer, f"{name_without_suff}.md", image_dir
    )
    print(f"Processed: {pdf_file_name}")


def process_folder(folder_path: str, output_dir: str = "output") -> None:
    """
    Process all PDF files in a folder
    
    Args:
        folder_path: Path to folder containing PDF files
        output_dir: Directory to save output files
    """
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return
        
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {folder_path}")
        return
        
    print(f"Found {len(pdf_files)} PDF files to process")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        process_pdf(pdf_path, output_dir)
    
    print(f"All {len(pdf_files)} PDF files processed successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF files to markdown")
    parser.add_argument("--input", "-i", type=str, help="Single PDF file path to process")
    parser.add_argument("--folder", "-f", type=str, help="Folder path containing PDF files to process")
    parser.add_argument("--output", "-o", type=str, default="output", help="Output directory for markdown files")
    
    args = parser.parse_args()
    
    if args.input and args.folder:
        print("Error: Please specify either --input or --folder, not both")
    elif args.folder:
        process_folder(args.folder, args.output)
    elif args.input:
        process_pdf(args.input, args.output)
    else:
        parser.print_help()
