import argparse
import urllib3
import os

import lancedb
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from applibot.utils.misc import compute_sha256, extract_output_block, read_text_file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MODEL_NAME = "gpt-4"
TEMPERATURE = 0.0
dummy_api_key = os.getenv("OPENAI_API_KEY", "sk-dummy")
llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE, openai_api_key=dummy_api_key)
embedding = OpenAIEmbeddings(openai_api_key=dummy_api_key)
DB_PATH = "data/lancedb"
INFO_TABLE = "info"

FORM_FORMATTING_TEMPLATE = """
From the given job application form, which may be poorly formatted, empty, or partially filled out:
{application_form}
Reformat the fields and values to adhere to the specified format: <Field: Value>.
Value any field not found in the above given information should be filled as "Not sure!".
Your output should strictly follow the example provided below:
=====Output start=====
Name: John Doe
Total experience in years: 6
Highest Level of Education: Bachelor's Degree
Skills: Project Management, Agile Methodologies, Scrum
Previous Employer: TechCorp
Email: john.doe@example.com
Passport: Not sure!
...
=====Output end=====
"""

FORM_TO_QUESTION_TEMPLATE = """
From the Job application Form, that is either empty or partially filled:
{application_form} 
Extract all the Fields present in the form.
The output should be a list of fields, each prefixed by 'Question: ', and presented within a block defined by '=====Output start=====' and '=====Output end======='.
Your output should strictly follow the example provided below:

=====Output start=====
Question: Name
Question: Total experience in years
Question: Highest Level of Education
...
=====Output end=======
"""

FILL_FORM_TEMPLATE = """
Populate Empty Form:
{empty_form}
Using Resume:
{resume}
And Additional Information:
{additional_info}

Fill up the Empty Form in a way that adheres to the specified format: <Field: Value> and encapsulated within '=====Output start=====' and '=====Output end======='.
Value any field not found in the above given information should be filled as "Not sure!".
Your output should strictly follow the example provided below:

=====Output start=====
Name: John Doe
Total experience in years: 6
Email: john.doe@example.com
Passport: Not sure!
...
=====Output end=======
"""

def remove_question_prefix(text):
    lines = text.split("\n")
    cleaned_lines = [line.replace("Question: ", "", 1) for line in lines]
    return "\n".join(cleaned_lines)

def format_information(text_file):
    text = read_text_file(text_file)
    form_formatting_template = PromptTemplate.from_template(FORM_FORMATTING_TEMPLATE)
    form_formatting_template = form_formatting_template.format(application_form=text)
    formatted_form_text = llm.predict(form_formatting_template)
    output = extract_output_block(formatted_form_text)
    print(output)

def save_information(text_file):
    loader = TextLoader(text_file)
    documents = loader.load()
    documents = CharacterTextSplitter().split_documents(documents)
    db = lancedb.connect(DB_PATH)
    data = [
        {
            "vector": embedding.embed_query(doc.page_content),
            "text": doc.page_content,
            "id": compute_sha256(doc.page_content),
        }
        for doc in documents
    ]
    if INFO_TABLE not in db.table_names():
        table = db.create_table(
            INFO_TABLE,
            data=data,
            mode="overwrite",
        )
    else:
        table = db.open_table(INFO_TABLE)
        table.add(data)

def retrieve_information_by_similarity(query,
                                       db_path=DB_PATH,
                                       table=INFO_TABLE,
                                       k=5
                                       ):
    db = lancedb.connect(db_path)
    table = db.open_table(table)
    query_vector = embedding.embed_query(query)
    results = table.search(query_vector).limit(k).to_df()
    return results

def main():
    parser = argparse.ArgumentParser(description='Script to save and retrieve information.')
    subparsers = parser.add_subparsers()
    
    parser_save = subparsers.add_parser('save', help='Save information to LanceDB.')
    parser_save.add_argument('--text-file', required=True, type=str, help='Path to the text file to be saved.')
    parser_save.set_defaults(func=save_information)
    
    parser_retrieve = subparsers.add_parser('retrieve', help='Retrieve saved information using similarity from LanceDB.')
    parser_retrieve.add_argument('--query', required=True, type=str, help='Query to search for in the saved documents.')
    parser_retrieve.set_defaults(func=retrieve_information_by_similarity)

    parser_format = subparsers.add_parser('format', help='Format the information from a text file.')
    parser_format.add_argument('--text-file', required=True, type=str, help='Path to the text file to be formatted.')
    parser_format.set_defaults(func=format_information)

    args = parser.parse_args()
    
    if 'func' in args:
        if 'text_file' in args:
            args.func(args.text_file)
        elif 'query' in args:
            args.func(args.query)
    else:
        print("Please specify a sub-command (save, retrieve, or format).")

if __name__ == "__main__":
    main()
