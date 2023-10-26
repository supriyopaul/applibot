**About "Applibot"**

Applibot is a tool designed to simplify the job application process. By storing details from past applications, it aids users in quickly filling out new job forms. Its capabilities extend to auto-filling applications, creating Expression-of-Interest messages, and assisting in responses to recruiter inquiries. Through Applibot's API, users can manage their resumes and personal information, and even receive suggestions on matching skills with job descriptions. It's a practical approach to the modern job application process.

## Usage Guide

Navigating the world of job applications can be daunting. With Applibot, we've streamlined the process, making it more efficient and less tedious. Follow the steps below to make the most of our tool:

### 1. **Storing Your Resume**

Before anything else, begin by uploading your resume. This will serve as the foundation for many of the functionalities that Applibot offers.

```python
response = applibot_api.post_resume("Your resume text here...")
print(response['message'])  # Should confirm the successful upload of the resume.
```

### 2. **Storing Additional Information**

While your resume is essential, many application forms require specific details that might not be present in your resume. For this, the `post_info` method comes into play. You can input text directly copied from previous application forms, even if it's unformatted. Applibot takes care of the formatting for you.

```python
info_text = """Unformatted text copied directly from a previous job application form"""
response = applibot_api.post_info(info_text)
print(response['formatted_info'])  # Displays the stored and formatted information.
```

Typically, after storing information from about 10 application forms, Applibot will have a robust set of details about you, making the auto-filling process even more accurate.

### 3. **Filling Out Application Forms**

Got a new job application form and find it too tedious to fill? Use the `post_questions` API. Simply provide the empty form as a text input (which you can copy directly from the application page), and Applibot will use the information it has stored to populate the answers.

```python
empty_form_text = """Empty form fields copied directly from a new job application form"""
response = applibot_api.post_questions(empty_form_text)
print(response['filled_form'])  # Shows the populated form.
```

### 4. **Generating Cover Letters and EOIs**

If a job posting catches your eye and you need to draft a compelling cover letter or an Expression of Interest (EOI), Applibot has you covered. Provide the job description to Applibot, and it will craft a personalized response for you.

- **For Cover Letters**:

  ```python
  job_desc = """Detailed job description copied from the job posting"""
  response = applibot_api.generate_cover_letter(job_desc)
  print(response['cover_letter'])  # Your personalized cover letter.
  ```

- **For EOIs**:

  ```python
  job_desc = """Detailed job description copied from the job posting"""
  response = applibot_api.generate_eoi(job_desc)
  print(response['eoi'])  # Your personalized EOI.
  ```

Remember, while Applibot aims to simplify the job application process, always review the generated content to ensure it aligns with your personal touch and the specific nuances of the job you're applying for. Best of luck in your job search!


## API Endpoint Overview

The Applibot system provides several API endpoints to facilitate job application-related processes. Below is a brief explanation of the available endpoints and their usage.

1. **Resume Management**
   - `post_resume(resume_text: str)`: Uploads a new resume. The method calculates a unique ID using SHA256 for the resume and saves it with the current timestamp.
   - `get_resumes(limit: int)`: Fetches a list of resumes up to the provided limit.
   - `delete_resume(resume_id: str)`: Deletes a specified resume using its ID.

2. **Information Management**
   - `format_info(info_text: str)`: Takes unformatted info and returns a formatted version using a pre-defined template.
   - `post_info(info_text: str)`: Posts the given information after formatting it.
   - `get_all_info()`: Fetches all stored information.
   - `delete_info(info_id: str)`: Deletes a specific piece of information using its ID.

3. **Question & Answers**
   - `post_questions(question_text: str)`: Given a text containing questions, the method extracts the questions, fetches the latest resume, retrieves relevant info texts, and finally, responds to the questions.

4. **Job Matching & Analysis**
   - `skill_match(job_description: str)`: Analyzes how well the skills in the latest resume match with a given job description.

5. **Cover Letter Generation**
   - `generate_cover_letter(job_description: str)`: Produces a cover letter based on the job description, utilizing the latest resume and any relevant information.

6. **Direct Messages (DM) Replies**
   - `reply_to_dm(dm: str, job_description: str)`: Generates a reply to a direct message, leveraging the latest resume and job description, as well as other relevant info.

7. **Expression of Interest (EOI)**
   - `generate_eoi(job_description: str)`: Generates an Expression of Interest (EOI) based on a given job description.