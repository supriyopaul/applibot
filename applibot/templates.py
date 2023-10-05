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