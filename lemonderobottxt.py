import requests
from urllib.robotparser import RobotFileParser

# set up the user agent and URL
url = "https://www.lemonde.fr/robots.txt"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41"

# make the request to the website's robots.txt file
headers = {"User-Agent": user_agent}
response = requests.get(url, headers=headers)

# check if the response was successful
if response.status_code == 200:
    # parse the robots.txt file
    robot_parser = RobotFileParser()
    robot_parser.parse(response.text)

    # check if the user agent is allowed to access the target URL
    if robot_parser.can_fetch(user_agent, "https://www.lemonde.fr/"):
        print("User agent is allowed to access the target URL.")
    else:
        print("User agent is not allowed to access the target URL.")
else:
    print("Error retrieving the robots.txt file.")
