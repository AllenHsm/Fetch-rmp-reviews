import json
import pandas as pd

# Load professor data from the JSON file
with open("rmp_prof_clean.json", "r") as file:
    professor_data = json.load(file)

# Organize and sort professors by department and last name
departments = {}

# Categorize professors by department
for prof in professor_data:
    department = prof["department"]
    if department not in departments:
        departments[department] = []
    departments[department].append(prof)

# Sort each department's professors by last name
for department in departments:
    departments[department].sort(key=lambda x: x["lastName"])

# Prepare data for Excel
excel_data = []

for department, professors in departments.items():
    for prof in professors:
        excel_data.append({
            "Department": department,
            "First Name": prof["firstName"],
            "Last Name": prof["lastName"],
            "Average Difficulty": prof["avgDifficulty"],
            "Average Rating": prof["avgRating"],
            "Legacy ID": prof["legacyId"],
            "Number of Ratings": prof["numRatings"],
            "Would Take Again Percent": prof["wouldTakeAgainPercent"]
        })

# Convert data to a DataFrame
df = pd.DataFrame(excel_data)

# Save to Excel file
df.to_excel("organized_professors.xlsx", index=False)

print("Data has been organized and saved to 'organized_professors.xlsx'")
