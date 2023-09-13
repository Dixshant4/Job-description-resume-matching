import os
from pdfminer.high_level import extract_text
import openai
import sqlite3
import json
openai.api_key = "insert API key"

# A function to extract text from pdfs
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# Path to the folder containing resumes
resume_folder = "/Users/shree89330/Documents/UofT/Quest internship/Resumes"

# List all files in the folder
files = os.listdir(resume_folder)

### A for loop to go through all the resumes in a folder ###
for file in files:
    # Check if the file is a resume
    if file.endswith(".pdf") or file.endswith(".docx") or file.endswith(".txt"):
        # Process the resume file and extract the text
        resume_path = os.path.join(resume_folder, file)
        text = extract_text_from_pdf(resume_path)

        ### Beginning of call to GPT ###
        ## Defining the role of the AI ##
        messages = [{'role':'system', 'content': 'You are a recruitment assistant for a multi-million dollar company that parses resumes to extract key information'}]

        ## Defining what we want GPT to do ##
        prompt = f"Given a pool of resumes, your goal is to extract and list for me all of thier skills (technical and soft),current location, name, phone number, email, educational background, certifications and total years of work experience. ###" \
                 f"Give your answer in a dictionary format with the following keys (case sensitve): [skills, location, name, phone_number, email, educational_background, certifications and total_years_of_work_experience]. Your response to each of these will be the values. You can choose to organise the values for each key in a list format " \
                 f"###" \
                 f"use double quotes for keys and string values as I should be readily able to convert this to an actual dictionary by using the json.loads function" \
                 f"Give the value for the key 'total years of work experience' as a single number formatted as a string" \
                 f"Resume: ###{text}###"
        messages.append({'role': 'user', 'content': prompt})

        ## making a call to GPT using the following function ##

        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k',
            messages = messages

        )
        # the return statement of the GPT model
        response = completion.choices[0].message.content

        # Next I decided to store the data permanently in a database to prevent calling GPT again for the same data.

        ### SQL code begins here ###
        conn = sqlite3.connect('resume_database.db')
        cursor = conn.cursor()
        # cursor.execute('DROP TABLE IF EXISTS my_table') # need to delete this before deployment

        # creates a table with the specified column names and their data type
        cursor.execute('''CREATE TABLE IF NOT EXISTS my_table (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT,
                          skills TEXT,
                          location TEXT,
                          phone_number TEXT,
                          email TEXT,
                          educational_background TEXT,
                          certifications TEXT,
                          total_years_of_work_experience TEXT)''')

        # outputs = ['{\n  "skills": [\n    "Machine Learning",\n    "Python",\n    "Scientific Data Analysis",\n    "Leadership",\n    "Teamwork",\n    "Quantum Mechanics",\n    "Quantum Information",\n    "Advanced Classical Mechanics",\n    "Electromagnetic Theory",\n    "Partial Differential Equations",\n    "Intro to Machine Learning",\n    "Software Design",\n    "Multivariable Calculus",\n    "Linear Algebra",\n    "Thermal Physics",\n    "XRD",\n    "EXAFS",\n    "Computational Fluid Dynamics",\n    "Bravais Lattices",\n    "Crystal Structure Groups",\n    "GSAS Software",\n    "Lab Experience",\n    "Cryogenic Techniques",\n    "Four-Probe Method",\n    "Resistance Bridge",\n    "Thermoelectric Generators",\n    "Data Analysis",\n    "Fluid Dynamics",\n    "ANSYS CFX",\n    "Leadership Skills",\n    "Communication Skills",\n    "Problem-Solving",\n    "Critical Thinking",\n    "Inclusivity and Diversity",\n    "Astrophysics",\n    "Blackholes",\n    "General Relativity",\n    "Effective Communication",\n    "Collaboration",\n    "Scuba Diving",\n    "Film Making",\n    "Adobe Creative Suite",\n    "Bhangra Dancing",\n    "Mechatronics",\n    "Tinkering",\n    "Soldering",\n    "Model United Nations",\n    "Cricket",\n    "Football"\n  ],\n  "location": [\n    "Toronto",\n    "Canada",\n    "Singapore",\n    "Cincinnati",\n    "USA",\n    "Mae Sot",\n    "Thailand"\n  ],\n  "name": ["Dixshant Shreemal"],\n  "phone_number": ["+1778-839-3972"],\n  "email": ["dixshant.shree@mail.utoronto.ca"],\n  "educational_background": [\n    "University of Toronto St. George, Canada",\n    "Bachelor of Science: Physics Specialist, Computer Science and Math Minor. CGPA: 3.78/4.00",\n    "Relevant courses: Quantum Mechanics 1, Quantum information, Advanced Classical Mechanics, Electromagnetic Theory, Partial differential equations, Intro to Machine Learning, Software design, Multivariable Calculus, Linear algebra 1, Thermal Physics. Lab: Practical Physics 1, Practical Physics 2, Electronics.",\n    "United World College, Singapore",\n    "International Baccalaureate (IB) Diploma: 44/45 Points.",\n    "Subjects: (Higher Level): Physics, Chemistry, Mathematics; (Standard Level): English, Spanish, Psychology."\n  ],\n  "certifications": ["PADI Certified Scuba Diver"],\n  "total_years_of_work_experience": "2"\n}']

        # One major problem is GPT returns text values. It is in string format. Need to convert it ourselves into dict type
        item = json.loads(response)

        # temporary placeholder for values that will go in each column of the table
        insert_sql = '''INSERT INTO my_table (name, skills, location, phone_number,
                        email, educational_background, certifications, total_years_of_work_experience)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

        # used json.dumps to convert the type into TEXT as this is the format
        # sql database accepts. Can't accept a list which is the original output
        cursor.execute(insert_sql, (
                json.dumps(item['name']), json.dumps(item['skills']),
                json.dumps(item['location']), json.dumps(item['phone_number']),
                json.dumps(item['email']),
                json.dumps(item['educational_background']),
                json.dumps(item['certifications']),
                item['total_years_of_work_experience']))

        conn.commit()
        conn.close()

        # at the end of this, one row of our table is populated with a specific
        # resume's features. Loop will continue till the last file in the folder


