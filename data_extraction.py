# reference https://www.tutorialspoint.com/fetch-all-href-link-using-selenium-in-python

import time,pandas as pd,ast
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

def href_ext(url):
    driver.get(url)
    lnks_1 = driver.find_elements(By.TAG_NAME,'div')
    found_link = False
    for a in lnks_1:
         lnks_2 = a.find_elements(By.CLASS_NAME,'vn-sheduleList')
         for b in lnks_2:
            lnks=b.find_elements(By.TAG_NAME,"li")
            for lnk in lnks:
                ln = lnk.find_element(By.CLASS_NAME,'vn-schedule-head')
                _num = lnk.find_element(By.CLASS_NAME,'w20')
                ln = lnk.find_element(By.CLASS_NAME,'vn-ticnbtn')
                l = ln.find_elements(By.TAG_NAME,"a")
                found_link = True
                for h_ref in l:
                    if 'match/' in h_ref.get_attribute('href'):return str(_num.text),h_ref.get_attribute('href')
                    # return str(_num.text),str(l[2].get_attribute('href'))
            if found_link:break
         if found_link:break

def get_match_res(url):
    driver.get(url)
    div_ele= driver.find_elements(By.TAG_NAME,"div")
    for links_ in div_ele:
        lnks = links_.find_elements(By.CLASS_NAME,"ap-match-innerwrp")
        match_result=set()
        for lnk in lnks:
            try:
                stad_name = lnk.find_element(By.CLASS_NAME,"matGround")
                stad_name = stad_name.text
                match_date = lnk.find_element(By.CLASS_NAME,"ms-matchdate")
                match_date = match_date.text
                match_time = lnk.find_element(By.CLASS_NAME,"ms-matchtime")
                match_time = match_time.text
                liinks=lnk.find_elements(By.CLASS_NAME,"ms-matchComments")
                for i in liinks:
                    if len(i.text)>1:
                        match_result.add(i.text)
                    else:continue
            except StaleElementReferenceException:continue
            except NoSuchElementException:continue
        if len(match_result)>1:
            for match_res in match_result:
                if "D/L Method" in i: return stad_name,match_date,match_time,match_res
        else:
            for match_res in match_result: return stad_name,match_date,match_time,match_res

def hm_tm_aw_tm(url):
   driver = webdriver.Chrome(options=options)
   driver.get(url)
   lnks=driver.find_elements(By.TAG_NAME,"li")
   for lnk in lnks:
      teams=[]
      try:
         nams = lnk.find_element(By.CLASS_NAME,'live-score')
         nam = nams.find_elements(By.CLASS_NAME,'vn-shedTeam')
         ln = lnk.find_element(By.CLASS_NAME,'vn-schedule-head')
         _num = lnk.find_element(By.CLASS_NAME,'w20')
      except:continue
      for na in nam:
         n = na.find_element(By.CLASS_NAME,'vn-teamTitle')
         i = n.text.split('\n')
         teams.append(i[0])
      if len(teams)==2:return teams[0],teams[1]

def ball_by_ball(_num,stad_name,match_date,match_time,match_res,url,hm_tm,aw_tm):
   innings_num = 0
   ball_values = []
   driver.get(url)
   cookie_button = driver.find_element(By.CLASS_NAME,"cookie__accept_btn")
   cookie_button.click()
   atags_list = driver.find_elements(By.CLASS_NAME,"ap-outer-tb-wrp")
   for atags in atags_list:
      button_list = atags.find_elements(By.CLASS_NAME,"ap-inner-tb-click")
      time.sleep(10)
      for button in range(len(button_list)):
         driver.execute_script("arguments[0].click();", button_list[button])
         time.sleep(10)
         bat_innings = button_list[button].text
         innings_num += 1
         if innings_num>2:break
         wait = WebDriverWait(driver, 10)
         ball_elements = wait.until(presence_of_all_elements_located((By.CSS_SELECTOR, "p.cmdOver.mcBall")))
         commentary_start = wait.until(presence_of_all_elements_located((By.CSS_SELECTOR, "div.commentaryStartText.ng-binding.ng-scope")))
         commentary_text = wait.until(presence_of_all_elements_located((By.CSS_SELECTOR, "div.commentaryText.ng-binding")))
         for i in range(len(ball_elements)):
            data = {}
            ball_number = ball_elements[i].text.split('\n')[0]
            ball_value = ball_elements[i].text.split('\n')[1]
            start = commentary_start[i].text
            text = commentary_text[i].text
            bowler,batsmen = start.split("bowling to")
            # print(_num,stad_name,match_date,match_time,match_res)
            data['Match Number']=_num
            data['Stadium']=stad_name
            data['Date']=match_date
            data['Time']=match_time
            data['Home Team']=hm_tm
            data['Away Team']=aw_tm
            data['Innings']=str(innings_num)
            data['Batting Team']=bat_innings
            data['Over']=ball_number
            data['Runs']=ball_value
            data['Bowler']=bowler
            data['Batsmen']=batsmen
            data['Commentary']=text
            data['Result']=match_res
            ball_values.append(data)
            
      with open(r'C:\Users\Satardhan\OneDrive\Projects\scraping\matche_data.txt',"a") as appf:
            for ball in ball_values:
                     s = str(ball)
                     appf.write(s)
                     appf.write("\n")
def match_data():
    yr = str(date.today().year)
    url_ ="https://www.iplt20.com/matches/results/"
    _num,_url = href_ext(url_+yr)
    while(True):
        try:
            hm_tm,aw_tm =hm_tm_aw_tm(url_+yr)
            if hm_tm != None:
                break
        except TypeError:
            driver.quit()
    stad_name,match_date,match_time,match_res = get_match_res(_url)
    ball_by_ball(_num,stad_name,match_date,match_time,match_res,_url,hm_tm,aw_tm)

if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    driver = webdriver.Chrome(options=options)
    match_data()
    driver.quit()
    df = pd.DataFrame(columns=['Match Number', 'Stadium', 'Date', 'Time', 'Home Team', 'Away Team', 'Innings', 'Batting Team', 'Over', 'Runs', 'Bowler', 'Batsmen', 'Commentary', 'Result'])
    with open(r'C:\Users\Satardhan\OneDrive\Projects\scraping\matche_data.txt', 'r') as rf:
        data = rf.readlines()
        for i in range(len(data)):
            dct = data[i].split('\n')[0]
            data_dict = ast.literal_eval(dct)
            # print(data_dict)
            df.loc[i] = data_dict
    df.to_csv(r'C:\Users\Satardhan\OneDrive\Projects\scraping\data.csv')