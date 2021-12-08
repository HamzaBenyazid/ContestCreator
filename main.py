from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from contest import *


def initialize_selenium():
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    return webdriver.Chrome(options=chrome_options)

if __name__ == "__main__":
    handle =input("handle or email:")
    password =getpass()
    name = input("name :")
    duration = int(input("duration (in minutes) : "))
    start_date =input("start date Mmm/dd/yyyy (example Dec/14/2021) : ")
    start_time =input("start time hour:min (example 21:00) : ")
    participation_type =ParticipationType(int(input("participation type ? \n1 - persons only\n2- persons and teams\n3 - teams only\n")))
    problems_file = open(input("problems file's path :"),"r")
    problems = problems_file.readlines()
    add_to_group = (input("Do you want to add it to a group ?(y/n) : ")=="y")
    group_id = None
    if add_to_group :
        group_id = input("group id (you can find the id in group's url ,ex : for https://codeforces.com/group/xxxxxxxx/contests \nthe 'xxxxxxxx' is the id.) :")

    browser = initialize_selenium()

    contest = Contest(name,problems,start_date,start_time,participation_type,duration)
    contest.create(browser,handle,password,group_id)
    print("Done :)")
    browser.close()