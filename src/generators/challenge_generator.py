import json
import random

import os
#TODO: put it in a constants file
ROOT_DIR=os.path.abspath(os.curdir)
print(ROOT_DIR)
print(os.environ.get('DOCKER_ENVIRONMENT'))
categories_path = 'categories.json' if os.environ.get('DOCKER_ENVIRONMENT') == None else '/app/categories.json'
def generate_challenge():
    positions: list = list(range(1, 17))  # create positions from 1-16
    
    def get_items_list(items: list[str]):
        items_list = []
        
        for item in items:
            position = random.choice(positions)
            positions.remove(position)
            items_list.append({"item": item, "position": position, "isGuessed": False})
            
        return items_list
    
    with open( categories_path, "r") as f:
        file_content: dict = json.load(f)
        keys = list(file_content.keys())
        random_categories = random.sample(keys, 4)
        
        categories = []
        for random_category in random_categories:
            items = random.sample(file_content[random_category], 4)
            
            category_contents = {
                "category": random_category,
                "items": get_items_list(items)
            }
            
            categories.append(category_contents)
            
        final_data = {
            "categories": categories
        }
        return final_data


def main():
    final_data = generate_challenge()
    with open( ROOT_DIR + "/" + "test.json", "w") as file:
        json.dump(final_data, file, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
