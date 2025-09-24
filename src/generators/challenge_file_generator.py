from datetime import date, timedelta
from challenge_generator import generate_challenge
import json
import os
from dotenv import load_dotenv

load_dotenv()

#TODO: put it in a constants file
ROOT_DIR=os.path.abspath(os.curdir)

def check_if_file_exists_in_root_dir(file_name):
    
    if os.environ['CHALLENGE_FILE_CHECK'] == '1':
        return False
    
    return os.path.isfile(ROOT_DIR + "/challenges/" + file_name)

def generate_challenge_file( file_name):
    if not check_if_file_exists_in_root_dir(file_name):
        challenge_content = generate_challenge()
        
        with open( ROOT_DIR + "/" + "challenges/" + file_name, "w") as file:
            json.dump(challenge_content, file, indent=2, ensure_ascii=False)
    
    else:
        print(f"{file_name} already exists. Skipping this.")

def main():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    today_challenge_filename = today.strftime("%d-%m-%Y")+ ".json"
    tomorrow_challenge_filename = tomorrow.strftime("%d-%m-%Y") + ".json"
    
    print("Generating challenge for TODAY: " + today.strftime("%d-%m-%Y"))
    generate_challenge_file( today_challenge_filename )
    print("Generating challenge for TOMORROW: " + tomorrow.strftime("%d-%m-%Y"))
    generate_challenge_file( tomorrow_challenge_filename )

if __name__ == '__main__':
    main()