import argparse
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import Field
from pydantic_core._pydantic_core import ValidationError

from resume_model import Resume  # Assuming Resume model has already been imported

class ResumeParser:
    def __init__(self, model_name="gpt-3.5-turbo", temperature=0.0):
        self.model = OpenAI(model_name=model_name, temperature=temperature)
        self.parser = PydanticOutputParser(pydantic_object=Resume)
        self.text2json_template = """Convert the given resume text:
        \n{query}\n
        Into structured JSON format:
        \n{format_instructions}\n
        If the fields are empty in the text, Feel free to put Default values.
        """
        self.text2json_template = """Convert the given resume text:
        \n{query}\n
        Into structured JSON format:
        \n{format_instructions}\n
        If the fields are empty in the text, Feel free to put Default values.
        """
        
    def text2json(self, resume_text: str) -> Resume:
        prompt = PromptTemplate(
            template=self.text2json_template,
            input_variables=["query"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        
        _input = prompt.format_prompt(query=resume_text)
        output = self.model(_input.to_string())
        
        # Parse the output to get a Resume object
        parsed_resume = self.parser.parse(output)
        
        return parsed_resume
    
    def pdf2text(self, pdf_fpath: str) -> str:
        
        return "Converted text from PDF at " + pdf_fpath


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse unstructured resume into structured format.')
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')
    
    # Sub-command for text2json
    parser_text2json = subparsers.add_parser('text2json', help='Convert text to JSON.')
    parser_text2json.add_argument('--txt-fpath', type=str, required=True, help='Path to the text file containing unstructured resume.')
    
    # Sub-command for pdf2text
    parser_pdf2text = subparsers.add_parser('pdf2text', help='Convert PDF to text.')
    parser_pdf2text.add_argument('--pdf-fpath', type=str, required=True, help='Path to the PDF file containing unstructured resume.')
    
    args = parser.parse_args()
    resume_parser = ResumeParser()
    
    if args.command == 'text2json':
        with open(args.txt_fpath, 'r') as file:
            resume_text = file.read()
        parsed_resume = resume_parser.text2json(resume_text)
        print(parsed_resume)
    elif args.command == 'pdf2text':
        converted_text = resume_parser.pdf2text(args.pdf_fpath)
        print(converted_text)
    else:
        print("Invalid command. Use 'text2json' or 'pdf2text'.")
