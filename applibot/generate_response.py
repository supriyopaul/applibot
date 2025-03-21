import argparse
import sys
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from applibot.templates import (
    INPUT,
    EOI_DM_INITIATION_INSTRUCTIONS,
    EOI_EMAIL_INITIATION_INSTRUCTIONS,
    EOI_DM_REPLY_INSTRUCTIONS,
    EOI_DM_INITIATION_OUTPUT_TEMPLATE,
    EOI_EMAIL_INITIATION_OUTPUT_TEMPLATE,
    EOI_DM_REPLY_OUTPUT_TEMPLATE,
    JOB_SUMMARY_INSTRUCTIONS,
    COVER_LETTER_INSTRUCTIONS,
    COVER_LETTER_OUTPUT_TEMPLATE
)
from applibot.utils.misc import (
    get_resume,
    get_saved_info,
    log_interaction,
    RED,
    ORANGE,
    GREEN,
    PURPLE,
    YELLOW,
    RESET,
    color_text,
    get_multiline_input,
)

MODEL_NAME = "gpt-4"
TEMPERATURE = 0.0

def get_eoi_dm(job_description, resume, additional_info, user_llm):
    eoi_dm_generation_prompt = f"{INPUT}\n{EOI_DM_INITIATION_INSTRUCTIONS}\n{EOI_DM_INITIATION_OUTPUT_TEMPLATE}"
    eoi_dm_prompt = PromptTemplate.from_template(eoi_dm_generation_prompt)
    eoi_dm_prompt = eoi_dm_prompt.format(
        context_type="job description",
        context=job_description,
        resume=resume,
        additional_info=additional_info,
        max_characters=500,
    )
    print(color_text(eoi_dm_prompt, ORANGE))
    eoi_dm_text = user_llm.predict(eoi_dm_prompt)
    return eoi_dm_prompt, eoi_dm_text

def get_eoi_email(job_description, resume, additional_info, user_llm):
    eoi_email_generation_prompt = f"{INPUT}\n{EOI_EMAIL_INITIATION_INSTRUCTIONS}\n{EOI_EMAIL_INITIATION_OUTPUT_TEMPLATE}"
    eoi_email_prompt = PromptTemplate.from_template(eoi_email_generation_prompt)
    eoi_email_prompt = eoi_email_prompt.format(
        context_type="job description",
        context=job_description,
        resume=resume,
        additional_info=additional_info,
        max_characters=600,
    )
    print(color_text(eoi_email_prompt, ORANGE))
    eoi_email_text = user_llm.predict(eoi_email_prompt)
    return eoi_email_prompt, eoi_email_text

def get_eoi_dm_reply(context, resume, additional_info, user_llm):
    eoi_dm_reply_prompt = f"{INPUT}\n{EOI_DM_REPLY_INSTRUCTIONS}\n{EOI_DM_REPLY_OUTPUT_TEMPLATE}"
    dm_reply_prompt = PromptTemplate.from_template(eoi_dm_reply_prompt)
    dm_reply_prompt = dm_reply_prompt.format(
        context_type="recruiter's message",
        context=context,
        resume=resume,
        additional_info=additional_info,
        max_characters=500
    )
    print(color_text(dm_reply_prompt, ORANGE))
    dm_reply_text = user_llm.predict(dm_reply_prompt)
    return dm_reply_prompt, dm_reply_text

def get_job_summary(job_description, resume, additional_info, user_llm):
    job_summary_generation_prompt = f"{INPUT}\n{JOB_SUMMARY_INSTRUCTIONS}\n{JOB_SUMMARY_OUTPUT_TEMPLATE}"
    job_summary_prompt = PromptTemplate.from_template(job_summary_generation_prompt)
    job_summary_prompt = job_summary_prompt.format(
        context_type="job description",
        context=job_description,
        resume=resume,
        additional_info=additional_info,
        max_characters=500,
    )
    print(color_text(job_summary_prompt, ORANGE))
    job_summary_text = user_llm.predict(job_summary_prompt)
    return job_summary_prompt, job_summary_text

def get_cover_letter(job_description, resume, additional_info, user_llm):
    cover_letter_generation_prompt = f"{INPUT}\n{COVER_LETTER_INSTRUCTIONS}\n{COVER_LETTER_OUTPUT_TEMPLATE}"
    cover_letter_prompt = PromptTemplate.from_template(cover_letter_generation_prompt)
    cover_letter_prompt = cover_letter_prompt.format(
        context_type="job description",
        context=job_description,
        resume=resume,
        additional_info=additional_info,
        max_characters=1000,  # You can adjust the maximum characters as needed
    )
    print(color_text(cover_letter_prompt, ORANGE))
    cover_letter_text = user_llm.predict(cover_letter_prompt)
    return cover_letter_prompt, cover_letter_text

def main():
    parser = argparse.ArgumentParser(description='Script to get user input and call appropriate function.')
    
    # Adding arguments for file paths
    parser.add_argument('--resume-fpath', default='data/.myresume.txt', help='Path to the resume file')
    parser.add_argument('--info-fpath', default='data/.myinfo.txt', help='Path to the additional info file')
    parser.add_argument('--api-key', required=True, help='User OpenAI API key')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--summary', action='store_true', help='Call get_job_summary() function')
    group.add_argument('--cover-letter', action='store_true', help='Call get_cover_letter() function')
    group.add_argument('--email', action='store_true', help='Call get_eoi_email() function')
    group.add_argument('--dm', action='store_true', help='Call get_eoi_dm() function')
    group.add_argument('--reply', action='store_true', help='Call get_eoi_dm_reply() function')
    
    args = parser.parse_args()
    
    user_llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE, openai_api_key=args.api_key)
    
    print('Press "Ctrl+C" to exit.')
    output = ""
    context = ""
    saved_info = get_saved_info(args.info_fpath)
    
    try:
        resume = get_resume(args.resume_fpath)

        context = get_multiline_input("Enter context: Recruiter's Message / Job description (Type 'END' on a new line when done):")
        if not context.strip():
            print("Error: Recruiter's Message cannot be empty.")
            exit()
        
        additional_info = get_multiline_input("Enter Additional Information (Type 'END' on a new line when done):")
        
        if not additional_info.strip():
            print("No additional info provided, using saved info.")
            additional_info = saved_info
        else:
            additional_info = additional_info + '\n' + saved_info

        if args.email:
            prompt, output = get_eoi_email(context, resume, additional_info, user_llm)
        elif args.dm:
            prompt, output = get_eoi_dm(context, resume, additional_info, user_llm)
        elif args.reply:
            prompt, output = get_eoi_dm_reply(context, resume, additional_info, user_llm)
        elif args.summary:
            prompt, output = get_job_summary(context, resume, additional_info, user_llm)
        elif args.cover_letter:
            prompt, output = get_cover_letter(context, resume, additional_info, user_llm)
        
        print(color_text(output, PURPLE))
        log_interaction(prompt=prompt, response=output)


    except KeyboardInterrupt:
        print("\nExiting the program.")
        sys.exit(0)

if __name__ == "__main__":
    main()
