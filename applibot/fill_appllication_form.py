import argparse
import urllib3
import os

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from applibot.utils.misc import (
    get_resume,
    RED,
    ORANGE,
    GREEN,
    PURPLE,
    save_to_file,
    color_text,
    get_multiline_input,
    extract_output_block,
)

from applibot.utils.form_utils import (
    FORM_TO_QUESTION_TEMPLATE,
    FILL_FORM_TEMPLATE,
    remove_question_prefix,
    retrieve_information_by_similarity
)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MODEL_NAME = "gpt-4"
TEMPERATURE = 0.0
dummy_api_key = os.getenv("OPENAI_API_KEY", "sk-dummy")
llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE, openai_api_key=dummy_api_key)
embedding = OpenAIEmbeddings(openai_api_key=dummy_api_key)

def get_questions_in_form(application_form):
    form_to_question_template = PromptTemplate.from_template(FORM_TO_QUESTION_TEMPLATE)
    form_to_question_template = form_to_question_template.format(application_form=application_form)
    formatted_form_questions = llm.predict(form_to_question_template)
    questions = extract_output_block(formatted_form_questions)
    return remove_question_prefix(questions)

def get_relevant_information(questions, db_path, table):
    info_df = retrieve_information_by_similarity(questions, db_path, table)
    info_text = info_text = '\n\n'.join(info_df['text'])
    return info_text

def answer_form(empty_form, resume, additional_info):
    fill_form_template = PromptTemplate.from_template(FILL_FORM_TEMPLATE).format(empty_form=empty_form,
                                                                                 resume=resume,
                                                                                 additional_info=additional_info
                                                                                 )
    filled_form = llm.predict(fill_form_template)
    answers = extract_output_block(filled_form)
    return answers

def chat_interface(resume, lancedb_path, lancedb_table_name, saved_forms_dir):
    print(color_text("You can enter 'restart' at any time to restart the chat.", ORANGE))
    while True:
        user_input = get_multiline_input(color_text("Enter empty form: ", ORANGE))
        if user_input.lower() == "restart":
            print(color_text("Restarting chat...", ORANGE))
            continue
        empty_form = user_input
        questions = get_questions_in_form(empty_form)
        print(color_text(f"Questions in form:\n{questions}", PURPLE))
        additional_info = get_relevant_information(questions, db_path=lancedb_path, table=lancedb_table_name)
        answers = answer_form(empty_form, resume, additional_info)
        print(color_text(f"Filled up form:\n{answers}", GREEN))

        
        save_option = input(color_text("Save filled up form to file? (yes/no): ", ORANGE)).strip().lower()
        if save_option == 'yes':
            save_to_file(answers, saved_forms_dir)

def main():
    parser = argparse.ArgumentParser(description='Simple chat interface with restart functionality.')
    
    parser.add_argument('--lance-db', default="data/lancedb:info", type=str, 
                        help='Path to the LanceDB in the format "path:table". Default is "data/lancedb:info".')
    parser.add_argument('--resume-text-file', default="data/.myresume.txt", type=str, 
                        help='Path to the text file for resuming chat. Default is "data/.myresume.txt".')
    parser.add_argument('--saved-forms', default="data/formatted-forms", type=str, 
                        help='Directory to save the filled forms. Default is "data/formatted-forms".')
    
    args = parser.parse_args()

    print(color_text(f"Using LanceDB at: {args.lance_db}", ORANGE))
    resume = get_resume(args.resume_text_file)
    lancedb_path, lancedb_table_name = args.lance_db.split(":")
    chat_interface(resume, lancedb_path, lancedb_table_name, args.saved_forms)

if __name__ == "__main__":
    main()
