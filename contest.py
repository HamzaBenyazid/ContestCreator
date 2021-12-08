from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import enum
import  time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class ParticipationType(enum.Enum):
    PERSONS_ONLY = 1
    PERSONS_AND_TEAMS = 2
    TEAMS_ONLY=3


class Contest :
    
    def __init__(self,name:str,problems:list,start_date,start_time,participation_type:ParticipationType,duration):
        self.name = name
        self.problems=problems
        self.start_date=start_date
        self.start_time=start_time
        self.participation_type=participation_type
        self.duration=duration

    def login(self,browser,handle,password):
        browser.get("https://codeforces.com/enter")
        enter = browser.find_element(By.CSS_SELECTOR,"#header > div.lang-chooser > div:nth-child(2) > a:nth-child(1)")
        enter.click()
        handle_field = browser.find_element(By.ID,"handleOrEmail")
        password_field = browser.find_element(By.ID,"password")
        handle_field.send_keys(handle)
        password_field.send_keys(password)
        password_field.submit()
        WebDriverWait(browser,60).until(EC.url_to_be("https://codeforces.com/"))

    def createMashupContest(self,browser):
        browser.get("https://codeforces.com/mashup/new")
        browser.find_element(By.ID,"contestName").send_keys(self.name)
        browser.find_element(By.ID,"contestDuration").send_keys(self.duration)
        problem_box = browser.find_elements(By.CLASS_NAME,"ac_input")[-1]

        for problem in self.problems:
            problem_box.send_keys(problem)
            problem_box = browser.find_elements(By.CLASS_NAME,"ac_input")[-1]
            WebDriverWait(browser,60).until(EC.element_to_be_clickable(problem_box))
        
        button = browser.find_elements(By.CLASS_NAME,"submit")[-1]
        WebDriverWait(browser,10).until(EC.element_to_be_clickable(button))
        button.click()
        time.sleep(1)

    def addOtherParameters(self,browser):
        url = browser.current_url
        self.id = url.split('/')[-1]
        browser.get("https://codeforces.com/gym/edit/"+self.id)
        rows = browser.find_elements(By.CLASS_NAME,"contest-profile-row")
        start_date_and_time = rows[3]
        start_date_and_time.find_element(By.CLASS_NAME,"hasDatepick").send_keys(self.start_date)
        start_date_and_time.find_element(By.CLASS_NAME,"hasTimeEntry").send_keys(self.start_time)
        participation_type_field = rows[8]
        participation_type_field=Select(participation_type_field.find_element(By.TAG_NAME,"select"))
        participation_type_field.select_by_value(self.participation_type.name)
        browser.find_element(By.ID,"generic").click()
        time.sleep(1)
        print("contest created.")

    def addContestToGroup(self,browser,group_id):
        browser.get("https://codeforces.com/group/"+group_id+"/contests/add")
        browser.find_element(By.ID,"contestIdAndName").send_keys(self.id)
        WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.ID,"submit"))).click()
        WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.NAME,"codeforces-dialog-ok-button"))).click()
        print("contest added to your group.")
        time.sleep(3)
        
    def create(self,browser,handle:str,password:str,group_id):
        self.login(browser,handle,password)
        self.createMashupContest(browser)
        self.addOtherParameters(browser)
        if group_id!=None:
            self.addContestToGroup(browser,group_id)
        




