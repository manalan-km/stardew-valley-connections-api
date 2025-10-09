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
IDs = []
def check_if_file_exists_in_root_dir(file_name):
    if os.environ['CHALLENGE_FILE_CHECK'] == '1':
        return False
    
    return os.path.isfile(ROOT_DIR + "/challenges/" + file_name)

def get_challenges_id_data():
    global IDs
    try:        
        ids =  database_client.table("challenges").select("id").execute()
        IDs = ids.data
        return IDs 
    except:  # noqa: E722
        print("Error fetching the ID column from Challenges table")
        raise
        
def get_id_for_challenge(date_to_check) -> int:
    data = get_challenges_id_data()
    
    return  data[len(data) - 1]["id"] + 1 if len(data) !=0 else 1

def write_to_database(json_content, current_date):
    challenge_id = get_id_for_challenge(current_date)
    does_challenge_exist = False 
    
    json_content["id"] = int(challenge_id)    

    if len(IDs) != 0:
        try :
            dates = database_client.table("challenges").select("date").execute().data
        except:  # noqa: E722
            print("Error fetching the Date column from Challenges Table")
            raise
        
        for date in dates:
            if date["date"] == current_date:
                does_challenge_exist = True 

    if does_challenge_exist:
        try:
            print("Updating record for ", current_date)
            response = database_client.table("challenges").update({"challenge": json_content}).eq("date", current_date).execute()
            
            json_content["id"] = response.data[0]["id"]
            
            print("Updated for ", current_date)
            
        except:  # noqa: E722
            print("Error updating for challenge for: ", current_date)
            raise
        
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
            raise 
    return json_content  

def generate_challenge_file( file_name : str):
    try:
        
        if not check_if_file_exists_in_root_dir(file_name):
                challenge_content = generate_challenge()
                date = file_name.split(".")[0]
            
                challenge_content_json = write_to_database(challenge_content, date)

                with open( ROOT_DIR + "/" + "challenges/" + file_name, "w") as file:
                    json.dump(challenge_content_json, file, indent=2, ensure_ascii=False)
                
        else:
            print(f"{file_name} already exists. Skipping this.")   
    except Exception as e:
            print(f"Error while generating the challenge file {file_name}: " , e)
            

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