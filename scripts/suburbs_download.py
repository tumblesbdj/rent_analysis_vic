import os
import requests
from bs4 import BeautifulSoup
import json

# Mixed results with the following two lines, think its a linux vs windows thing
# output_relative_dir = '../../data/'
output_relative_dir = 'data/'

postcode_output = output_relative_dir + 'landing/postcode_mapping.json'

# check if it exists as it makedir will raise an error if it does exist
if not os.path.exists(output_relative_dir):
    os.makedirs(output_relative_dir)
    for sub_dir in ['landing', 'raw', 'curated', 'development']:
            if not os.path.exists(output_relative_dir  + sub_dir):
                os.makedirs(output_relative_dir + sub_dir)

def get_postcode_suburb_mapping(url):
    # Send a request to the website
    response = requests.get(url)
    
    # Check for a successful response
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialize an empty dictionary
    postcode_dict = {}
    
    # Find all the <li> elements that are direct children of the ul with class 'pclist'
    postcode_items = soup.select('ul.pclist > li')
    
    for item in postcode_items:
        # Extract the postcode from the <a> tag
        postcode_tag = item.find('a')
        if postcode_tag:
            postcode = postcode_tag.text.strip()
        
            # Extract the suburb names from the nested <ul> inside the current <li>
            suburb_list = item.find('ul')
            if suburb_list:
                suburb_names = [li.text.strip() for li in suburb_list.find_all('li')]
            else:
                suburb_names = []
            
            # Add the postcode and its suburbs to the dictionary
            postcode_dict[postcode] = suburb_names
    
    return postcode_dict

url = 'https://postcodes-australia.com/state-postcodes/vic'
postcode_mapping = get_postcode_suburb_mapping(url)

with open(postcode_output, 'w') as json_file:
        json.dump(postcode_mapping, json_file, indent=4)

print(f"Data successfully saved to {postcode_output}")