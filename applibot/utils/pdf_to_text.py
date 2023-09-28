import argparse
import os
import fitz  # PyMuPDF

# Define constants
MAX_FILE_SIZE_MB = 5  # Maximum allowed file size in MB
MAX_PAGES = 5  # Maximum allowed number of pages in the PDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a given PDF file.

    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"{pdf_path} does not exist.")
    
    # Check file size
    file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"The file size ({file_size_mb:.2f} MB) exceeds the allowed limit of {MAX_FILE_SIZE_MB} MB.")
    
    with fitz.open(pdf_path) as pdf_document:
        # Check number of pages
        if pdf_document.page_count > MAX_PAGES:
            raise ValueError(f"The number of pages ({pdf_document.page_count}) exceeds the allowed limit of {MAX_PAGES}.")
        
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
    return text

def main():
    parser = argparse.ArgumentParser(description='Extract text from a given PDF file.')
    parser.add_argument('--pdf-fpath', required=True, help='Path to the PDF file.')
    
    args = parser.parse_args()
    pdf_path = args.pdf_fpath
    
    try:
        extracted_text = extract_text_from_pdf(pdf_path)
        print(extracted_text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
