import argparse
import os
import fitz  # PyMuPDF
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Define constants
MAX_FILE_SIZE_MB = 5  # Maximum allowed file size in MB
MAX_PAGES = 5  # Maximum allowed number of pages in the PDF
MODEL_NAME="gpt-4"
TEMPRATURE=0.0

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a given PDF file.

    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"{pdf_path} does not exist.")
    
    file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"The file size ({file_size_mb:.2f} MB) exceeds the allowed limit of {MAX_FILE_SIZE_MB} MB.")
    
    with fitz.open(pdf_path) as pdf_document:
        if pdf_document.page_count > MAX_PAGES:
            raise ValueError(f"The number of pages ({pdf_document.page_count}) exceeds the allowed limit of {MAX_PAGES}.")
        
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
    return text

def smart_convert_resume(text: str, openai_api_key: str) -> str:
    """
    Formats the text as though it is a resume using LLM and langchain.

    :param text: Text to be formatted.
    :param openai_api_key: API key for OpenAI.
    :return: Formatted text as a string.
    """
    llm = ChatOpenAI(model=MODEL_NAME)
    prompt_template = PromptTemplate.from_template("Format the following text as a beautiful resume:\n{text}")
    formatted_prompt = prompt_template.format(text=text)
    formatted_text = llm.predict(formatted_prompt)
    return formatted_text

def main():
    parser = argparse.ArgumentParser(description='Extract text from a given PDF file.')
    parser.add_argument('--pdf-fpath', required=True, help='Path to the PDF file.')
    parser.add_argument('--smart-convert-resume', action='store_true', help='Format the text as though it is a resume using LLM and langchain.')
    parser.add_argument('--openai-api-key', type=str, help='API key for OpenAI.')
    
    args = parser.parse_args()
    pdf_path = args.pdf_fpath
    smart_convert = args.smart_convert_resume
    openai_api_key = args.openai_api_key or os.getenv("OPENAI_API_KEY")
    
    try:
        extracted_text = extract_text_from_pdf(pdf_path)
        if smart_convert:
            if not openai_api_key:
                raise ValueError("OpenAI API key is required for smart convert resume.")
            extracted_text = smart_convert_resume(extracted_text, openai_api_key)
        print(extracted_text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
