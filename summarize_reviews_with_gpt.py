from openai import OpenAI
import os, re, time
import json
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def summarize_by_gpt( comments ):
    chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages= [{"role": "system", "content": "You are a subjective summarizer and your task is to summarzie the students' comments (at least 3 comments) under a professor's Rate My Professor page. Your summarization should be brief but accurate, without changing the students' original message in the comments. Your summarization should be between 2-3 sentences long. You should not answer with anything unrelated to the comments themselves or any introduction. "}, 
                       {"role": "user", "content": comments}],
            temperature = 0
    )
    time.sleep(1.5)
    response= chat_completion.choices[0].message.content if chat_completion.choices[0].message.content else "No response received"
    if not response:
        print ("NO RESPONSE FROM CHATGPT")
    else:
        return response


def read_comments_and_id ():
    with open ("comments_by_prof.json", 'r') as f:
        all_comments = json.load(f)
    summarized_list = {}
    for number, comments in all_comments.items():
        # print ("number: ", number)
        comments_string = json.dumps(comments)
        response = summarize_by_gpt(comments_string)
    # print (response)
        summarized_list[number] = response
        
    with open ("summarized_comments.json", 'w')as f:
        json.dump(summarized_list, f, indent=4)


import json

def add_comments_to_professors(target_file, comments_file, output_file):
    # Load the target JSON file
    with open(target_file, 'r') as f:
        target_data = json.load(f)
    
    # Load the comments JSON file
    with open(comments_file, 'r') as f:
        comments_data = json.load(f)
    
    # Update the target data by matching legacyId with the comment keys
    for professor in target_data:
        legacy_id = str(professor.get("legacyId"))  # Convert legacyId to string for matching
        if legacy_id in comments_data:
            professor["comments_summarized_by_gpt"] = comments_data[legacy_id]
        else:
            professor["comments_summarized_by_gpt"] = None  # Add None if no comment found
    
    # Save the updated data to a new file
    with open(output_file, 'w') as f:
        json.dump(target_data, f, indent=4)

# Example usage
add_comments_to_professors(
    target_file='rmp_prof_clean.json', 
    comments_file='summarized_comments.json', 
    output_file='rmp_prof_with_summarized_comments.json'
)
