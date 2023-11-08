```curl -X 'POST' \
  'http://0.0.0.0:9000/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "rhendricks@piedpiper.com",
  "password": "password"
}'
```
```{
  "email": "rhendricks@piedpiper.com",
  "password": "password"
}
```
```curl -X 'POST' \
  'http://0.0.0.0:9000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=rhendricks%40piedpiper.com&password=password&scope=&client_id=&client_secret='
```
```
{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaGVuZHJpY2tzQHBpZWRwaXBlci5jb20iLCJleHAiOjE2OTk4NjMwNjl9.S2nWwUw8-VAe9baxC7mF403hwALdH8WTQFAPS5quZxU",
"token_type": "bearer"
}
```

```
curl -X 'POST' \
'http://0.0.0.0:9000/resume/' \
-H 'accept: application/json' \
-H 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaGVuZHJpY2tzQHBpZWRwaXBlci5jb20iLCJleHAiOjE2OTk4NjMwNjl9.S2nWwUw8-VAe9baxC7mF403hwALdH8WTQFAPS5quZxU' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'resume_content=RICHARD%20HENDRICKS%20San%20Francisco%2C%20CA%20Email%3A%20rhendricks%40piedpiper.com%20Phone%3A%20(555)%20123-4567%20%20Objective%3A%20Experienced%20software%20engineer%20and%20entrepreneur%20seeking%20to%20leverage%20my%20skills%20in%20algorithm%20development%2C%20team%20leadership%2C%20and%20tech%20innovation%20in%20a%20challenging%20environment.%20%20Experience%3A%20%20CEO%20%26%20Founder%2C%20Pied%20Piper%20San%20Francisco%2C%20CA%20%E2%80%94%202014-2021%20%20Led%20the%20development%20of%20a%20revolutionary%20data%20compression%20algorithm.%20Successfully%20pitched%20and%20secured%20funding%20from%20numerous%20venture%20capital%20firms.%20Navigated%20various%20business%20challenges%2C%20from%20intellectual%20property%20disputes%20to%20aggressive%20competitors.%20Managed%20a%20team%20of%20diverse%20engineers%20and%20professionals%2C%20cultivating%20a%20collaborative%20and%20innovative%20company%20culture.%20Pivoted%20company%20direction%20based%20on%20market%20needs%2C%20resulting%20in%20a%20new%20emphasis%20on%20decentralized%20internet%20technology.%20Software%20Engineer%2C%20Hooli%20San%20Francisco%2C%20CA%20%E2%80%94%202012-2014%20%20Developed%20and%20maintained%20code%20for%20Nucleus%2C%20a%20core%20product%20of%20Hooli'\''s%20platform.%20Collaborated%20with%20cross-functional%20teams%20to%20ensure%20seamless%20integration%20of%20new%20features.%20Identified%20and%20resolved%20numerous%20bugs%2C%20leading%20to%20a%2015%25%20improvement%20in%20software%20performance.%20Innovated%20new%20approaches%20to%20data%20compression%2C%20which%20later%20laid%20the%20foundation%20for%20Pied%20Piper.%20Education%3A%20%20M.S.%20in%20Computer%20Science%20Stanford%20University%20%E2%80%94%202010-2012%20%20Specialized%20in%20distributed%20systems%20and%20algorithms.%20Published%20a%20paper%20on%20a%20novel%20approach%20to%20data%20compression.%20B.S.%20in%20Computer%20Science%20California%20Institute%20of%20Technology%20(Caltech)%20%E2%80%94%202006-2010%20%20Graduated%20magna%20cum%20laude.%20Participated%20in%20various%20hackathons%2C%20securing%20first%20place%20in%20the%202009%20Caltech%20Coding%20Challenge.%20Skills%3A%20%20Expert%20in%20data%20compression%20algorithms.%20Proficient%20in%20multiple%20programming%20languages%2C%20including%20Python%2C%20Java%2C%20and%20C%2B%2B.%20Strong%20leadership%20and%20team%20management%20capabilities.%20Effective%20problem-solving%20skills.%20Excellent%20communication%20and%20negotiation%20capabilities.'```
```
```
{
"id": 2,
"content": "RICHARD HENDRICKS San Francisco, CA Email: rhendricks@piedpiper.com Phone: (555) 123-4567  Objective: Experienced software engineer and entrepreneur seeking to leverage my skills in algorithm development, team leadership, and tech innovation in a challenging environment.  Experience:  CEO & Founder, Pied Piper San Francisco, CA — 2014-2021  Led the development of a revolutionary data compression algorithm. Successfully pitched and secured funding from numerous venture capital firms. Navigated various business challenges, from intellectual property disputes to aggressive competitors. Managed a team of diverse engineers and professionals, cultivating a collaborative and innovative company culture. Pivoted company direction based on market needs, resulting in a new emphasis on decentralized internet technology. Software Engineer, Hooli San Francisco, CA — 2012-2014  Developed and maintained code for Nucleus, a core product of Hooli's platform. Collaborated with cross-functional teams to ensure seamless integration of new features. Identified and resolved numerous bugs, leading to a 15% improvement in software performance. Innovated new approaches to data compression, which later laid the foundation for Pied Piper. Education:  M.S. in Computer Science Stanford University — 2010-2012  Specialized in distributed systems and algorithms. Published a paper on a novel approach to data compression. B.S. in Computer Science California Institute of Technology (Caltech) — 2006-2010  Graduated magna cum laude. Participated in various hackathons, securing first place in the 2009 Caltech Coding Challenge. Skills:  Expert in data compression algorithms. Proficient in multiple programming languages, including Python, Java, and C++. Strong leadership and team management capabilities. Effective problem-solving skills. Excellent communication and negotiation capabilities.",
"created_at": "2023-11-06T09:32:11.065598Z"
}```

```

```
curl -X 'GET' \
  'http://0.0.0.0:9000/resumes/latest' \
  -H 'accept: application/json' \
  -H 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaGVuZHJpY2tzQHBpZWRwaXBlci5jb20iLCJleHAiOjE2OTk4NjMwNjl9.S2nWwUw8-VAe9baxC7mF403hwALdH8WTQFAPS5quZxU'
```
```
{
  "id": 2,
  "content": "RICHARD HENDRICKS San Francisco, CA Email: rhendricks@piedpiper.com Phone: (555) 123-4567  Objective: Experienced software engineer and entrepreneur seeking to leverage my skills in algorithm development, team leadership, and tech innovation in a challenging environment.  Experience:  CEO & Founder, Pied Piper San Francisco, CA — 2014-2021  Led the development of a revolutionary data compression algorithm. Successfully pitched and secured funding from numerous venture capital firms. Navigated various business challenges, from intellectual property disputes to aggressive competitors. Managed a team of diverse engineers and professionals, cultivating a collaborative and innovative company culture. Pivoted company direction based on market needs, resulting in a new emphasis on decentralized internet technology. Software Engineer, Hooli San Francisco, CA — 2012-2014  Developed and maintained code for Nucleus, a core product of Hooli's platform. Collaborated with cross-functional teams to ensure seamless integration of new features. Identified and resolved numerous bugs, leading to a 15% improvement in software performance. Innovated new approaches to data compression, which later laid the foundation for Pied Piper. Education:  M.S. in Computer Science Stanford University — 2010-2012  Specialized in distributed systems and algorithms. Published a paper on a novel approach to data compression. B.S. in Computer Science California Institute of Technology (Caltech) — 2006-2010  Graduated magna cum laude. Participated in various hackathons, securing first place in the 2009 Caltech Coding Challenge. Skills:  Expert in data compression algorithms. Proficient in multiple programming languages, including Python, Java, and C++. Strong leadership and team management capabilities. Effective problem-solving skills. Excellent communication and negotiation capabilities.",
  "created_at": "2023-11-06T09:32:11.065598Z"
}
```

```
curl -X 'GET' \
  'http://0.0.0.0:9000/users/2/resumes/' \
  -H 'accept: application/json' \
  -H 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaGVuZHJpY2tzQHBpZWRwaXBlci5jb20iLCJleHAiOjE2OTk4NjMwNjl9.S2nWwUw8-VAe9baxC7mF403hwALdH8WTQFAPS5quZxU'
```
```
[
  {
    "id": 2,
    "content": "RICHARD HENDRICKS San Francisco, CA Email: rhendricks@piedpiper.com Phone: (555) 123-4567  Objective: Experienced software engineer and entrepreneur seeking to leverage my skills in algorithm development, team leadership, and tech innovation in a challenging environment.  Experience:  CEO & Founder, Pied Piper San Francisco, CA — 2014-2021  Led the development of a revolutionary data compression algorithm. Successfully pitched and secured funding from numerous venture capital firms. Navigated various business challenges, from intellectual property disputes to aggressive competitors. Managed a team of diverse engineers and professionals, cultivating a collaborative and innovative company culture. Pivoted company direction based on market needs, resulting in a new emphasis on decentralized internet technology. Software Engineer, Hooli San Francisco, CA — 2012-2014  Developed and maintained code for Nucleus, a core product of Hooli's platform. Collaborated with cross-functional teams to ensure seamless integration of new features. Identified and resolved numerous bugs, leading to a 15% improvement in software performance. Innovated new approaches to data compression, which later laid the foundation for Pied Piper. Education:  M.S. in Computer Science Stanford University — 2010-2012  Specialized in distributed systems and algorithms. Published a paper on a novel approach to data compression. B.S. in Computer Science California Institute of Technology (Caltech) — 2006-2010  Graduated magna cum laude. Participated in various hackathons, securing first place in the 2009 Caltech Coding Challenge. Skills:  Expert in data compression algorithms. Proficient in multiple programming languages, including Python, Java, and C++. Strong leadership and team management capabilities. Effective problem-solving skills. Excellent communication and negotiation capabilities.",
    "created_at": "2023-11-06T09:32:11.065598Z"
  }
]
```

```
curl -X 'DELETE' \
  'http://0.0.0.0:9000/resume/2/' \
  -H 'accept: application/json' \
  -H 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaGVuZHJpY2tzQHBpZWRwaXBlci5jb20iLCJleHAiOjE2OTk4NjMwNjl9.S2nWwUw8-VAe9baxC7mF403hwALdH8WTQFAPS5quZxU'
```
```
{
  "message": "Resume with id 2 deleted successfully."
}
```

```
curl -X 'POST' \
  'http://0.0.0.0:9000/format-info/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'unformatted_info_text=My%20Information%20Have%20you%20previously%20worked%20for%20TechSphere%20Innovations%3F%20No%20Legal%20Name%20Mr.%20Richard%20Hendricks%20I%20have%20a%20preferred%20name%20No%20Address%20324%20Aviato%20Blvd%2C%20San%20Francisco%2C%20CA%2094105%20USA%20Email%20rhendricks%40piedpiper.com%20Phone%20%2B1%20555-321-9876%20(Private%20Phone)%20%20My%20Experience%20%20Work%20Experience%201%20Job%20Title%20CEO%20%26%20Founder%20Company%20Pied%20Piper%20Location%20San%20Francisco%2C%20CA%20I%20currently%20work%20here%20Yes%20From%202014%20Role%20Description%20Founded%20and%20led%20the%20development%20of%20a%20revolutionary%20data%20compression%20algorithm.%20Navigated%20multiple%20business%20challenges%2C%20secured%20VC%20funding%2C%20and%20led%20a%20team%20of%20engineers.%20%20Work%20Experience%202%20Job%20Title%20Software%20Engineer%20Company%20Hooli%20Location%20San%20Francisco%2C%20CA%20I%20currently%20work%20here%20No%20From%202012%20To%202014%20Role%20Description%20Developed%20and%20maintained%20code%20for%20Nucleus%2C%20collaborated%20with%20cross-functional%20teams%2C%20and%20innovated%20new%20data%20compression%20methods.%20%20Work%20Experience%203%20Job%20Title%20Freelance%20Developer%20Company%20Self-Employed%20Location%20San%20Francisco%2C%20CA%20I%20currently%20work%20here%20No%20From%202010%20To%202012%20Role%20Description%20Worked%20on%20various%20freelance%20projects%2C%20specializing%20in%20back-end%20development%20and%20system%20design.%20%20Education%201%20School%20or%20University%20Stanford%20University%20Degree%20M.S.%20Field%20of%20Study%20Computer%20Science%20Overall%20Result%20(GPA)%203.9%20From%202010%20To%20(Actual%20or%20Expected)%202012%20%20Education%202%20School%20or%20University%20California%20Institute%20of%20Technology%20(Caltech)%20Degree%20B.S.%20Field%20of%20Study%20Computer%20Science%20Overall%20Result%20(GPA)%203.8%20From%202006%20To%20(Actual%20or%20Expected)%202010%20%20Languages%201%20Language%20English%20I%20am%20fluent%20in%20this%20language.%20Yes%20Overall%20Excellent%20%20Resume%2FCV%20Richard%2BHendricks.pdf%20435.98%20KB%20%20Websites%201%20URL%20https%3A%2F%2Fgithub.com%2Frhendricks%20%20Websites%202%20URL%20https%3A%2F%2Fpiedpiper.com%2Frichard%20%20Application%20Questions%201%20of%202%20Have%20you%20applied%20to%20TechSphere%20Innovations%20before%3F%20No%20Would%20you%20be%20willing%20to%20relocate%20if%20the%20company%20required%3F%20Yes%20Do%20you%20have%20relatives%20or%20friends%20currently%20working%20with%20TechSphere%20Innovations%3F%20No%20Do%20you%20have%20the%20Right%20to%20work%20in%20the%20country%20where%20the%20job%20is%20located%3F%20Yes%20%20Application%20Questions%202%20of%202%20Please%20confirm%20if%20you%20have%20a%20valid%20Aadhar%20card.%20No%2C%20I%20don'\''t%20Please%20confirm%20if%20you%20have%20a%20valid%20PAN%20card.%20No%2C%20I%20don'\''t%20I%20confirm%20that%20I%20am%2018%2B%20years%20of%20age%20Yes%2C%20I%20do%20%20Voluntary%20Disclosures%20Personal%20information%20Please%20specify%20your%20Gender%20Male%20Please%20specify%20your%20Date%20of%20Birth%204%2F12%2F1985%20Please%20specify%20your%20Country%20of%20Birth%20USA%20Please%20specify%20your%20City%20of%20Birth%20San%20Francisco%20Please%20specify%20your%20Marital%20Status%20Single%20Please%20specify%20your%20Citizenship%20Status%20Citizen%20(USA)%20Please%20specify%20your%20Primary%20Nationality%20USA%20Please%20specify%20your%20Additional%20Nationalities%20No%20Response%20%20Terms%20and%20Conditions%20Yes%2C%20I%20confirm%20that%20I%20have%20read%20and%20understood%20the%20Privacy%20Policy.%20Yes'
```
```
"Name: Mr. Richard Hendricks
Total experience in years: 10
Highest Level of Education: M.S. Computer Science, Stanford University
Skills: Data Compression, Back-end Development, System Design
Previous Employer: Pied Piper, Hooli, Self-Employed
Email: rhendricks@piedpiper.com
Phone: +1 555-321-9876
Address: 324 Aviato Blvd, San Francisco, CA 94105 USA
Worked for TechSphere Innovations before: No
Applied to TechSphere Innovations before: No
Willing to relocate: Yes
Relatives or friends at TechSphere Innovations: No
Right to work in job location country: Yes
Valid Aadhar card: No
Valid PAN card: No
Age confirmation: 18+ years
Gender: Male
Date of Birth: 4/12/1985
Country of Birth: USA
City of Birth: San Francisco
Marital Status: Single
Citizenship Status: Citizen (USA)
Primary Nationality: USA
Additional Nationalities: No Response
Read and understood the Privacy Policy: Yes
Resume/CV: Richard+Hendricks.pdf
Websites: https://github.com/rhendricks, https://piedpiper.com/richard"
```


```
curl -X 'POST' \
  'http://0.0.0.0:9000/info/' \
  -H 'accept: application/json' \
  -H 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaGVuZHJpY2tzQHBpZWRwaXBlci5jb20iLCJleHAiOjE2OTk4NjMwNjl9.S2nWwUw8-VAe9baxC7mF403hwALdH8WTQFAPS5quZxU' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'info_text=My%20Information%20Have%20you%20previously%20worked%20for%20TechSphere%20Innovations%3F%20No%20Legal%20Name%20Mr.%20Richard%20Hendricks%20I%20have%20a%20preferred%20name%20No%20Address%20324%20Aviato%20Blvd%2C%20San%20Francisco%2C%20CA%2094105%20USA%20Email%20rhendricks%40piedpiper.com%20Phone%20%2B1%20555-321-9876%20(Private%20Phone)%20%20My%20Experience%20%20Work%20Experience%201%20Job%20Title%20CEO%20%26%20Founder%20Company%20Pied%20Piper%20Location%20San%20Francisco%2C%20CA%20I%20currently%20work%20here%20Yes%20From%202014%20Role%20Description%20Founded%20and%20led%20the%20development%20of%20a%20revolutionary%20data%20compression%20algorithm.%20Navigated%20multiple%20business%20challenges%2C%20secured%20VC%20funding%2C%20and%20led%20a%20team%20of%20engineers.%20%20Work%20Experience%202%20Job%20Title%20Software%20Engineer%20Company%20Hooli%20Location%20San%20Francisco%2C%20CA%20I%20currently%20work%20here%20No%20From%202012%20To%202014%20Role%20Description%20Developed%20and%20maintained%20code%20for%20Nucleus%2C%20collaborated%20with%20cross-functional%20teams%2C%20and%20innovated%20new%20data%20compression%20methods.%20%20Work%20Experience%203%20Job%20Title%20Freelance%20Developer%20Company%20Self-Employed%20Location%20San%20Francisco%2C%20CA%20I%20currently%20work%20here%20No%20From%202010%20To%202012%20Role%20Description%20Worked%20on%20various%20freelance%20projects%2C%20specializing%20in%20back-end%20development%20and%20system%20design.%20%20Education%201%20School%20or%20University%20Stanford%20University%20Degree%20M.S.%20Field%20of%20Study%20Computer%20Science%20Overall%20Result%20(GPA)%203.9%20From%202010%20To%20(Actual%20or%20Expected)%202012%20%20Education%202%20School%20or%20University%20California%20Institute%20of%20Technology%20(Caltech)%20Degree%20B.S.%20Field%20of%20Study%20Computer%20Science%20Overall%20Result%20(GPA)%203.8%20From%202006%20To%20(Actual%20or%20Expected)%202010%20%20Languages%201%20Language%20English%20I%20am%20fluent%20in%20this%20language.%20Yes%20Overall%20Excellent%20%20Resume%2FCV%20Richard%2BHendricks.pdf%20435.98%20KB%20%20Websites%201%20URL%20https%3A%2F%2Fgithub.com%2Frhendricks%20%20Websites%202%20URL%20https%3A%2F%2Fpiedpiper.com%2Frichard%20%20Application%20Questions%201%20of%202%20Have%20you%20applied%20to%20TechSphere%20Innovations%20before%3F%20No%20Would%20you%20be%20willing%20to%20relocate%20if%20the%20company%20required%3F%20Yes%20Do%20you%20have%20relatives%20or%20friends%20currently%20working%20with%20TechSphere%20Innovations%3F%20No%20Do%20you%20have%20the%20Right%20to%20work%20in%20the%20country%20where%20the%20job%20is%20located%3F%20Yes%20%20Application%20Questions%202%20of%202%20Please%20confirm%20if%20you%20have%20a%20valid%20Aadhar%20card.%20No%2C%20I%20don'\''t%20Please%20confirm%20if%20you%20have%20a%20valid%20PAN%20card.%20No%2C%20I%20don'\''t%20I%20confirm%20that%20I%20am%2018%2B%20years%20of%20age%20Yes%2C%20I%20do%20%20Voluntary%20Disclosures%20Personal%20information%20Please%20specify%20your%20Gender%20Male%20Please%20specify%20your%20Date%20of%20Birth%204%2F12%2F1985%20Please%20specify%20your%20Country%20of%20Birth%20USA%20Please%20specify%20your%20City%20of%20Birth%20San%20Francisco%20Please%20specify%20your%20Marital%20Status%20Single%20Please%20specify%20your%20Citizenship%20Status%20Citizen%20(USA)%20Please%20specify%20your%20Primary%20Nationality%20USA%20Please%20specify%20your%20Additional%20Nationalities%20No%20Response%20%20Terms%20and%20Conditions%20Yes%2C%20I%20confirm%20that%20I%20have%20read%20and%20understood%20the%20Privacy%20Policy.%20Yes'
```
```
{
  "text": "Name: Mr. Richard Hendricks\nTotal experience in years: 10\nHighest Level of Education: M.S. Computer Science, Stanford University\nSkills: Data Compression, Back-end Development, System Design\nPrevious Employer: Pied Piper, Hooli, Self-Employed\nEmail: rhendricks@piedpiper.com\nPhone: +1 555-321-9876\nAddress: 324 Aviato Blvd, San Francisco, CA 94105 USA\nWorked for TechSphere Innovations before: No\nApplied to TechSphere Innovations before: No\nWilling to relocate: Yes\nRelatives or friends at TechSphere Innovations: No\nRight to work in job location country: Yes\nValid Aadhar card: No\nValid PAN card: No\nAge confirmation: 18+ years\nGender: Male\nDate of Birth: 4/12/1985\nCountry of Birth: USA\nCity of Birth: San Francisco\nMarital Status: Single\nCitizenship Status: Citizen (USA)\nPrimary Nationality: USA\nAdditional Nationalities: No Response\nRead and understood the Privacy Policy: Yes\nResume/CV: Richard+Hendricks.pdf\nWebsites: https://github.com/rhendricks, https://piedpiper.com/richard",
  "id": "b14ba3216eacc4c42b91cd53f20744a0b4d1b75390c1182e9eb0ffa923d6832e",
  "user_id": 2
}
```


```
curl -X 'DELETE' \
  'http://0.0.0.0:9000/info/9e1e778df50a8f89a4cf73e721a3b20d68972c8e8db7d5d5631b88827d60095a/' \
  -H 'accept: application/json' \
  -H 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaGVuZHJpY2tzQHBpZWRwaXBlci5jb20iLCJleHAiOjE2OTk4NjMwNjl9.S2nWwUw8-VAe9baxC7mF403hwALdH8WTQFAPS5quZxU'
```
```
{
  "status": "Info deleted successfully"
}
```

```
curl -X 'POST' \
  'http://localhost:9000/questions/' \
  -H 'accept: application/json' \
  -H 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaGVuZHJpY2tzQHBpZWRwaXBlci5jb20iLCJleHAiOjE2OTk4NjMwNjl9.S2nWwUw8-VAe9baxC7mF403hwALdH8WTQFAPS5quZxU' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'question=Skills%20Inventory%20%26%20Training%20Programming%20Languages%20you%20are%20proficient%20in%3F%20Databases%20technologies%3F%20Certifications%3A%20Workshops%20Attended%3A%20Expected%20ctc%3A%20Current%20ctc%3A'
```
```
"Programming Languages: Java, Go, Python, C++\nDatabases technologies: MySQL, PostgreSQL, MongoDB\nCertifications: Advanced Computer Science (Stanford), Data Compression Specialist (MIT)\nWorkshops Attended: Global Tech Leaders Summit, 2021, Compression Algorithms Symposium, 2020\nExpected ctc: $260,000 + Equity\nCurrent ctc: $200,000"
```