import json
import pandas as pd
from collections import defaultdict

# Load professor data from the JSON file
with open("rmp_prof_clean.json", "r") as file:
    professor_data = json.load(file)

# Organize professors by department and identify potential duplicates by last name
departments = defaultdict(list)
potential_duplicates = []

# Categorize professors by department and last name
for prof in professor_data:
    department = prof["department"]
    last_name = prof["lastName"]
    # Append professor to department-specific list
    departments[(department, last_name)].append(prof)

# Check for potential duplicates
for (department, last_name), profs in departments.items():
    if len(profs) > 1:  # Only keep entries with duplicate last names
        for prof in profs:
            potential_duplicates.append({
                "Department": department,
                "First Name": prof["firstName"],
                "Last Name": last_name,
                "Average Difficulty": prof["avgDifficulty"],
                "Average Rating": prof["avgRating"],
                "Legacy ID": prof["legacyId"],
                "Number of Ratings": prof["numRatings"],
                "Would Take Again Percent": prof["wouldTakeAgainPercent"]
            })

# Convert the potential duplicates list to a DataFrame
duplicates_df = pd.DataFrame(potential_duplicates)

# Save to Excel file
duplicates_df.to_excel("potential_duplicate_professors.xlsx", index=False)

print("Potential duplicates have been saved to 'potential_duplicate_professors.xlsx'")
