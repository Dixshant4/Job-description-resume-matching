import sqlite3
import json
import numpy as np
from job_description import jd_skills
import re

candidate_scores = []

# Open a connection to the SQLite database
conn = sqlite3.connect('/Users/shree89330/Documents/UofT/Quest internship/test/resume_database.db')
cursor = conn.cursor()


# Execute a SELECT query to retrieve all rows from the table
cursor.execute("SELECT * FROM my_table")

# Fetch all the rows as a list of tuples
rows = cursor.fetchall()

# Iterate through the rows and access each row's data
for row in rows:
    # Each row is a tuple where you can access the values by index
    id = row[0]
    name = json.loads(row[1])
    resume_skills = json.loads(row[2])
    location = json.loads(row[3])
    phone_number = json.loads(row[4])
    email = json.loads(row[5])
    educational_backgroun = json.loads(row[6])
    certification = json.loads(row[7])
    total_years_of_work_experience = json.loads(row[8])
    print(id)


    ## extracting the matching criteria ##
    def experiece(years):
        try:
            string = re.findall(r'\d+\.\d+|\d+', years[0])
            if len(string) == 0:
                numeric = 0
            else:
                numeric = float(string[0])
            return numeric
        except:
            return years


    yrs_of_exp = experiece(total_years_of_work_experience)

    # determine how many skills from the resume_skills list match with those in
    # the jd_skills list as a percentage of the total number of skills in the
    # jd_skills list.
    def skills_matched(resume_skills, jd_skills):
        resume_skills = [skill.lower() for skill in resume_skills]
        jd_skills = [skill.lower() for skill in jd_skills]
        count = len(
            [element for element in resume_skills if element in jd_skills])
        percentage_match = (count / len(jd_skills)) * 100
        return percentage_match


    ## scoring the candidate ##
    candidate_score = 0

    # if location == 'bangalore' or 'Bangalore':
    if yrs_of_exp > 10:
        candidate_score += 1
    elif 2 <= yrs_of_exp < 10:
        candidate_score += 0.3
    else:
        pass

    if skills_matched(resume_skills, jd_skills) > 50:
        candidate_score += 1
    elif 10 < skills_matched(resume_skills, jd_skills) < 50:
        candidate_score += 0.5
    elif 1 < skills_matched(resume_skills, jd_skills) < 10:
        candidate_score += 0.1
    else:
        pass
    # else:
    #     candidate_score -= -10

    candidate_scores.append(candidate_score)
print(candidate_scores)

## Normalize the scores ##
np_candidate_scores = np.array(candidate_scores)

np_candidate_scores = np_candidate_scores - np.min(np_candidate_scores)
np_candidate_scores = np_candidate_scores / np.max(np_candidate_scores)

print(np_candidate_scores)

# Close the database connection
conn.close()
