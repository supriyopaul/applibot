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
Hi {{Fist name of Recruiter or Hiring Manager}},
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
Question: {{Additional information required from applicant}}
Answer:
Question: {{Additional information required from applicant}}
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

JOB_SUMMARY_INSTRUCTIONS = """\
Craft a concise and clear summary of the given job description,
The summary should not be more than {max_characters} characters long,
Highlight the main responsibilities, qualifications, and any specific skills or experiences required.
Do not include any skill that isn't present in the resume or information given above,
Instead, include {{placeholders}} for information that you are unsure about,
At the end, list any questions that might clarify the {{placeholders}}. Example: Is experience with a specific technology required?"""

JOB_SUMMARY_OUTPUT_TEMPLATE = """\
following is the output format that must strictly be followed:
=====Output start=====
{{Job Title}}
Responsibilities:
* {{Main responsibility}}
* {{Another responsibility}}
* {{And so on...}}

Qualifications:
* {{Main qualification}}
* {{Another qualification}}
* {{And so on...}}

Skills and Experiences:
* {{Specific skill or experience}}
* {{Another specific skill or experience}}
* {{And so on...}}

====
Required information to fill any placeholders in the summary:
Question: {{Additional information required from applicant}}
Answer:
Question: {{Additional information required from applicant}}
Answer:
...
====
=====Output end====="""

COVER_LETTER_INSTRUCTIONS = """\
Craft a professional and personalized cover letter expressing interest in the job,
The letter should be concise and clear and not be more than {max_characters} characters long.
Do not include any skill that isn't present in the resume or information given above,
Instead, include {{placeholders}} for information that you are unsure about,
At the end, ask questions that might answer the {{placeholders}}. Example: Years of experience in a skill"""

COVER_LETTER_OUTPUT_TEMPLATE = """\
following is the output format that must strictly be followed:
=====Output start=====
Dear {{Hiring Manager or Recruiter Name}},

{{Introduction Paragraph}}
- Briefly introduce yourself and mention how you heard about the job opening.

{{Why You're a Good Fit}}
- Detail why you are a good fit for this job, citing specific skills and experiences that align with the job description.
- Keyword for skills releveant to the Job description

{{Why You're Interested in This Job}}
- Explain why you are interested in this job and how it aligns with your career goals.

Sincerely,
{{Your Name}}
{{Your Contact Information}}
====
Required information to fill any placeholders in the letter:
Question: {{Additional information required from applicant}}
Answer:
Question: {{Additional information required from applicant}}
Answer:
...
====
=====Output end====="""


INFO_FORMATTING_TEMPLATE = """
From the given user information input, which may be poorly formatted, empty, or partially filled out:
=====Unformated Info start=====
{unformatted_info}
=====Unformated Info end=====
Reformat the information and values to adhere to the specified format: <Field: Value>.
Value any field not found in the above given information should be removed.
Your output should strictly follow the example provided below:
=====Info start=====
Name: John Doe
Total experience in years: 6
Highest Level of Education: Bachelor's Degree
Skills: Project Management, Agile Methodologies, Scrum
Previous Employer: TechCorp
Email: john.doe@example.com
...
=====Info end=====
"""

QUESTION_RESPONSE_TEMPLATE = """
Given the set of questions and user-provided information, extract and format the answers to the questions using the user's information:
=====Questions start=====
{questions}
=====Questions end=====
From the user's information:
=====Resume start=====
{resume}
=====Resume end=====
=====Info start=====
{info_text}
=====Info end=====
Format the answers to the questions in the format: <Question: Answer>. If an answer to a question is not found in the user's information, fill it as "Not sure!".
Your output should strictly follow the example provided below:
=====Answers start=====
What is your name?: John Doe
How many years of experience do you have?: 6
What's your highest level of education?: Bachelor's Degree
List some of your skills: Project Management, Agile Methodologies, Scrum
Who was your previous employer?: TechCorp
What's your email address?: john.doe@example.com
Do you have a passport?: Not sure!
...
=====Answers end=====
"""

QUESTION_EXTRACTION_TEMPLATE = """
From the provided unformatted Form:
=====Form start=====
{unformatted_info}
=====Form end=====
Extract key details and frame them as empty questions. Your output should help in understanding what kind of details can be extracted from the given unformatted information. Present the questions in a list format.
Your output should strictly follow the example provided below:
=====Questions start=====
- What is the name?
- How many years of experience does the individual have?
- What is the highest level of education achieved?
- Can you list some of the skills?
...
=====Questions end=====
"""

COVER_LETTER_TEMPLATE = """
Based on the provided Job Description:
=====Job Description start=====
{job_description}
=====Job Description end=====
Generate a cover letter template that highlights the applicant's fit for the given job description.
The output should be within a well-defined block with placeholders for the recruiter's name, the applicant's name, and the reasons why the applicant is a good fit for the job.
Your output should strictly follow the example provided below:
=====Cover Letter start=====

[Place Recipient's Name, e.g., "Dear Mr. Smith," or "Hello Recruiting Team,"]

I am writing to express my interest in the [Specific Job Title from the job description] position at [Company Name from the job description]. My name is [Applicant's Name] and I believe my qualifications and experience align well with the requirements outlined in the job description.

Here are some reasons why I believe I'm a strong fit for this role:

[Reason 1: e.g., "I have over 5 years of experience in..."]
[Reason 2: e.g., "My educational background in... has equipped me with..."]
[Reason 3: e.g., "In my previous role at..."]
...
[You can continue to add more reasons or bullet points as needed]

Sincerely,
[Applicant's Name]
=====Cover Letter end=====
"""

COVER_LETTER_FILL_TEMPLATE = """
Given the provided cover letter template and user-provided information, generate a tailored cover letter using the user's credentials:
=====Cover Letter Template start=====
{cover_template}
=====Cover Letter Template end=====
From the user's information:
=====Resume start=====
{resume}
=====Resume end=====
=====Info start=====
{info_text}
=====Info end=====

Use the resume and info text to fill in the placeholders within the cover letter template to create a cover letter tailored to the user's qualifications and the specific job description.

Your output should be:

=====Filled Cover Letter start=====

[Filled up cover letter template based on the provided user information]

=====Cover Letter end=====
"""

DM_REPLY_TEMPLATE = """
Based on the provided Recruiter's Direct Message:
=====DM start=====
{dm}
=====DM end=====
Generate a response that addresses the recruiter's message while highlighting the applicant's fit for the mentioned position.
The output should be within a well-defined block with placeholders for the applicant's name,
and the answers to questions that the recruiter has asked (if any).
Make the template so that it can be filled under 1000 characters.
Rather than paragraphs make it bullet short points wherever you can.
Do not include any unnecessary placeholders whose information wouldn't be relevant in making the Expression of Interest short, crisp and precise.
Your output should inside the block as mentioned below:
=====DM Response start=====
Hi [Recruiter's name if present in DM],
[Template for replying to the dm]
=====DM Response end=====
"""

DM_REPLY_FILL_TEMPLATE = """
Given the provided template and user-provided information, generate a response:
=====Response Template start=====
{dm_reply_template}
=====Response Template end=====
From the user's information:
=====Resume start=====
{resume}
=====Resume end=====
=====Info start=====
{info_text}
=====Info end=====

Use the resume and info text to fill in the placeholders within the response template.
Do not lie about anything. Remove points for which information not present in the above resume and information. 
Make sure to make it under 1000 characters. Short and precise.
Rather than paragraphs make it bullet short points wherever you can.
Your output should be:

=====Response start=====
[Filled up EOI template based on the provided user information]
=====Response end=====
"""


EXPRESSION_OF_INTEREST_TEMPLATE = """
Based on the provided Job description:
=====Job description start=====
{job_description}
=====Job description end=====
Generate an Expression of Interest (EOI) template.
The output should have placeholders for the applicant's name,
reason why the applicant is interested in the company or field and reasons why applicant is a good fit.
Make the template so that it can be filled under 1000 characters.
Rather than paragraphs make it bullet short points wherever you can.
Do not include any unnecessary placeholders whose information wouldn't be relevant in making the Expression of Interest short, crisp and precise.
Your output should inside the block as mentioned below:
=====Expression of Interest start=====
[Job role name as subject]
Hi [Recruiter's name if in Job description],
[Expression of Interest (EOI) template]
=====Expression of Interest end=====
"""

EOI_FILL_TEMPLATE = """
Given the provided EOI template and user-provided information, generate a tailored Expression of Interest letter:
=====Expression of Interest Template start=====
{eoi_template}
=====Expression of Interest Template end=====
From the user's information:
=====Resume start=====
{resume}
=====Resume end=====
=====Info start=====
{info_text}
=====Info end=====

Use the resume and info text to fill in the placeholders within the EOI template.
Do not lie about anything. Remove points for which information not present in the above resume and information. 
Make sure to make it under 1000 characters. Short and precise.
Rather than paragraphs make it bullet short points wherever you can.
Your output should be:

=====Expression of Interest start=====
[Filled up EOI template based on the provided user information]
=====Expression of Interest end=====
"""