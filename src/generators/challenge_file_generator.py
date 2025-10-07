from datetime import date, timedelta
from challenge_generator import generate_challenge
import json
import os
from dotenv import load_dotenv
# challenge_file_generator.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.database.database import database_client

load_dotenv()

#TODO: put it in a constants file
ROOT_DIR=os.path.abspath(os.curdir)

def check_if_file_exists_in_root_dir(file_name):
    
    if os.environ['CHALLENGE_FILE_CHECK'] == '1':
        return False
    
    return os.path.isfile(ROOT_DIR + "/challenges/" + file_name)

def write_to_database(json_content, current_date):
    previous_challenge_id = database_client.table("challenges").select("id").execute()
    data = previous_challenge_id.data     
    challenge_id : int = 1
    does_challenge_exist = False 
    
    if len(data) != 0:
        challenge_id = data[len(data) - 1]["id"] + 1

        dates = database_client.table("challenges").select("date").execute().data
        
        
        for date in dates:
            if date["date"] == current_date:
                does_challenge_exist = True 

    if does_challenge_exist:
        try:
            print("Updating record for ", current_date)
            database_client.table("challenges").update({"challenge": json_content}).eq("date", current_date).execute()
            print("Updated for ", current_date)
            
        except:  # noqa: E722
            print("Error updating for challenge for: ", current_date)
        
    else:
        try:    
            print("Creating a new Challenge for: ", current_date ) 
            database_client.table("challenges").insert(
                {
                    "id": challenge_id,
                    "date": current_date,
                    "challenge": json_content,
                }
            ).execute() 
            
        except:  # noqa: E722
            print("Error inserting new value for Challenge:" ,current_date) 
        

def generate_challenge_file( file_name : str):
    if not check_if_file_exists_in_root_dir(file_name):
        challenge_content = generate_challenge()
        challenge_content_json = json.dumps(challenge_content)

       
        with open( ROOT_DIR + "/" + "challenges/" + file_name, "w") as file:
            json.dump(challenge_content, file, indent=2, ensure_ascii=False)
        date = file_name.split(".")[0]
        write_to_database(challenge_content_json,date)
    else:
        print(f"{file_name} already exists. Skipping this.")

def main():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    today_challenge_filename = today.strftime("%Y-%d-%m")+ ".json"
    tomorrow_challenge_filename = tomorrow.strftime("%Y-%d-%m") + ".json"
    
    print("Generating challenge for TODAY: " + today.strftime("%d-%m-%Y"))
    generate_challenge_file( today_challenge_filename )
    print("Generating challenge for TOMORROW: " + tomorrow.strftime("%d-%m-%Y"))
    generate_challenge_file( tomorrow_challenge_filename )

if __name__ == '__main__':
    main()