import argparse
import sys
from utils.misc import get_resume, get_saved_info, log_interaction
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

MODEL_NAME = "gpt-4"
TEMPERATURE = 0.0
llm = ChatOpenAI(model=MODEL_NAME)

# ANSI color codes
RED = '\033[91m'
ORANGE = '\033[93m'
GREEN = '\033[92m'
PURPLE = '\033[95m'
YELLOW = '\033[93m'
RESET = '\033[0m'

INPUT = """\
You are applicant GPT
For a {context_type}:
{context}\n\n
And resume:
{resume}\n\n
and additional information:
{additional_info}\n\n"""

EOI_DM_INITIATION_INSTRUCTIONS = """\
Craft a casual direct message expressing interest in the job,
the message should not be more than {max_characters} characters long,
Do not include any skill that isn't present in the resume or information given above,
Instead include {{placeholders}} for information that you are unsure about,
At the end ask questions that might answer the {{placeholders}}. Example: Years of experience in a skill"""

EOI_EMAIL_INITIATION_INSTRUCTIONS = """\
Craft a professional email expressing interest in the job,
The email should be concise and clear and not be more than {max_characters} characters long.
Do not include any skill that isn't present in the resume or information given above,
Instead, include {{placeholders}} for information that you are unsure about,
At the end, ask questions that might answer the {{placeholders}}. Example: Years of experience in a skill"""

EOI_DM_REPLY_INSTRUCTIONS = """\
Craft a professional and polite response expressing your gratitude and interest in the potential job role.
The message should not be more than {max_characters} characters long,
Ensure to address any points or questions raised by the recruiter and provide any additional information requested.
Keep the message concise and focused on expressing your interest and availability for further discussions.
Do not include any skill that isn't present in the resume or information given above,
Instead include {{placeholders}} for information that you are unsure about,
At the end ask questions that might answer the {{placeholders}}. Example: Expected CTC"""

EOI_DM_INITIATION_OUTPUT_TEMPLATE = """\
following is the output format that must strictly be followed:
=====Output start=====
Hi {{Fisr name of Recruiter or Hiring Manager}},
{{Expression of interest}}
{{Reasons applicant good match:}}
* {{The main skill that I have in my resume and is also mentioned in the job description}}
* {{Other relevant skills required in the job description that I posess}}
* {{More bullet points}}
...
Attaching my resume for your reference.

====
Required information to fill any placeholders in the message:
Question: {{Additional information required from applicant}}
Answer:
Question: {{Additional information required from applicant}}
Answer:
...
====
=====Output end====="""

EOI_EMAIL_INITIATION_OUTPUT_TEMPLATE = """\
following is the output format that must strictly be followed:
=====Output start=====
Send to: {{Email of Recruiter or Hiring Manager}}
Subject: Expression of Interest: {{Job Title}} - {{Your Name}}

Hi {{Fist name of Recruiter or Hiring Manager}},
{{Greetings or context if Recruiter or Hiring Manager initiated the conversation}}

{{Expression of interest}}
{{Reasons why I am a good match:}}
* {{The main skill that I have in my resume and is also mentioned in the job description}}
* {{Other relevant skills required in the job description that I possess}}
* {{Address any points or questions raised by the recruiter}}
...

I have attached my resume for your reference and would welcome the opportunity to discuss how I can contribute to {{Company Name}}.
Thank you for considering my application. I look forward to the opportunity to speak with you to discuss my application further.

Best Regards,
{{Applicant Name}}
{{Applicant Contact Information}}
====
Required information to fill any placeholders in the email:
Question: {{Additional information}}
Answer:
Question: {{Additional information}}
Answer:
...
====
=====Output end====="""

EOI_DM_REPLY_OUTPUT_TEMPLATE = """\
following is the output format that must strictly be followed:
=====Output start=====
Hi {{Fist name of Recruiter or Hiring Manager}},

Thank you for reaching out and considering me for the {{Job role}}.
I am grateful for the opportunity and very interested in learning more about it.

* {{Address any points or questions raised by the recruiter}}
* {{Address any points or questions raised by the recruiter}}
{{Provide any additional information requested}}

I am looking forward to discussing this opportunity further and exploring how I can contribute to {{Company Name}}.
Please let me know a convenient time for you when we can arrange a meeting or a call.

Best Regards,
{{Applicant name}}

====
Required information to fill any placeholders in the reply:
Question: {{Additional information required from applicant}}
Answer:
Question: {{Additional information required from applicant}}
Answer:
...
====
=====Output end====="""

def color_text(text, color_code):
    return f"{color_code}{text}{RESET}"

def get_multiline_input(prompt):
    print(color_text(prompt, GREEN))
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        except KeyboardInterrupt:
            print(color_text("\nInput interrupted. Proceeding with the entered text.", GREEN))
            break
    return '\n'.join(lines)

def get_eoi_dm(job_description, resume, additional_info):
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
    eoi_dm_text = llm.predict(eoi_dm_prompt)
    return eoi_dm_prompt, eoi_dm_text

def get_eoi_email(job_description, resume, additional_info):
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
    eoi_email_text = llm.predict(eoi_email_prompt)
    return eoi_email_prompt, eoi_email_text

def get_eoi_dm_reply(context, resume, additional_info):
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
    dm_reply_text = llm.predict(dm_reply_prompt)
    return dm_reply_prompt, dm_reply_text

def main():
    parser = argparse.ArgumentParser(description='Script to get user input and call appropriate function.')
    
    # Adding arguments for file paths
    parser.add_argument('--resume-fpath', default='data/.myresume.txt', help='Path to the resume file')
    parser.add_argument('--info-fpath', default='data/.myinfo.txt', help='Path to the additional info file')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--email', action='store_true', help='Call get_eoi_email() function')
    group.add_argument('--dm', action='store_true', help='Call get_eoi_dm() function')
    group.add_argument('--reply', action='store_true', help='Call get_eoi_dm_reply() function')
    
    args = parser.parse_args()
    
    print('Press "Ctrl+C" to exit.')
    output = ""
    context = ""
    saved_info = get_saved_info(args.info_fpath)
    
    try:
        resume = get_resume(args.resume_fpath)

        context = get_multiline_input("Enter Recruiter's Message (Type 'END' on a new line when done):")
        if not context.strip():
            print("Error: Recruiter's Message cannot be empty.")
            exit()
        
        additional_info = get_multiline_input("Enter Additional Information (Type 'END' on a new line when done):")
        
        if not additional_info.strip():
            additional_info = saved_info
        else:
            additional_info = additional_info + '\n' + saved_info

        if args.email:
            promt, output = get_eoi_email(context,resume, additional_info)
        elif args.dm:
            promt, output = get_eoi_dm(context, resume, additional_info)
        elif args.reply:
            promt, output = get_eoi_dm_reply(context, resume, additional_info)
        
        print(color_text(output, PURPLE))
        log_interaction(prompt=promt, response=output)


    except KeyboardInterrupt:
        print("\nExiting the program.")
        sys.exit(0)

if __name__ == "__main__":
    main()