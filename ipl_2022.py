# print ("9381380561")
import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')
driver = webdriver.Chrome(options=options)

def get_match_res(url):
    driver.get(url)
    div_ele= driver.find_elements(By.TAG_NAME,"div")
    for links_ in div_ele:
            try:
                lnks = links_.find_elements(By.CLASS_NAME,"ap-match-innerwrp")
                match_result=set()
                for lnk in lnks:
                        stad_name = lnk.find_element(By.CLASS_NAME,"matGround")
                        stad_name = stad_name.text
                        match_date = lnk.find_element(By.CLASS_NAME,"ms-matchdate")
                        match_date = match_date.text
                        # print(stad_name,match_date)
                        liinks=lnk.find_elements(By.CLASS_NAME,"ms-matchComments")
                        for i in liinks:
                            if len(i.text)>1:
                                match_result.add(i.text)
                            else:continue
                        if len(match_result)>1:
                            for match_res in match_result:
                                if "D/L Method" in match_res: return stad_name,match_date,match_res
                        else:
                            for match_res in match_result: return stad_name,match_date,match_res
            except StaleElementReferenceException:continue
            except NoSuchElementException:continue

def hm_tm_aw_tm(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    driver = webdriver.Chrome(options=options)
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

def ball_by_ball(_num,stad_name,match_date,match_res,url,hm_tm,aw_tm):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    driver = webdriver.Chrome(options=options)
    innings_num = 0
    ball_values = []
    driver.get(url)
    # cookie_button = driver.find_element(By.CLASS_NAME,"cookie__accept_btn")
    # cookie_button.click()
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
                try:start = commentary_start[i].text
                except:start = commentary_start[i-1].text
                text = commentary_text[i].text
                try:
                    bowler,batsmen = start.split("bowling to")
                except:
                    bowler = start
                    batsmen = ''
                data['Match Number']=_num
                data['Stadium']=stad_name
                data['Date']=match_date
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
        with open(r'C:\Users\Satardhan\OneDrive\Projects\scraping\matches_data2022.txt',"a") as appf:
            for ball in ball_values:
                s = str(ball)
                appf.write(s)
                appf.write("\n")
            return

hm_tm_aw_tm_lst = [{'Match Number': 'FINAL', 'Home Team': 'GT', 'Away Team': 'RR'}, {'Match Number': 'QUALIFIER 2', 'Home Team': 'RR', 'Away Team': 'RCB'}, {'Match Number': 'ELIMINATOR', 'Home Team': 'LSG', 'Away Team': 'RCB'}, {'Match Number': 'QUALIFIER 1', 'Home Team': 'GT', 'Away Team': 'RR'}, {'Match Number': 'MATCH 70', 'Home Team': 'SRH', 'Away Team': 'PBKS'}, {'Match Number': 'MATCH 69', 'Home Team': 'MI', 'Away Team': 'DC'}, {'Match Number': 'MATCH 68', 'Home Team': 'RR', 'Away Team': 'CSK'}, {'Match Number': 'MATCH 67', 'Home Team': 'RCB', 'Away Team': 'GT'}, {'Match Number': 'MATCH 66', 'Home Team': 'KKR', 'Away Team': 'LSG'}, {'Match Number': 'MATCH 65', 'Home Team': 'MI', 'Away Team': 'SRH'}, {'Match Number': 'MATCH 64', 'Home Team': 'PBKS', 'Away Team': 'DC'}, {'Match Number': 'MATCH 63', 'Home Team': 'LSG', 'Away Team': 'RR'}, {'Match Number': 'MATCH 62', 'Home Team': 'CSK', 'Away Team': 'GT'}, {'Match Number': 'MATCH 61', 'Home Team': 'KKR', 'Away Team': 'SRH'}, {'Match Number': 'MATCH 60', 'Home Team': 'RCB', 'Away Team': 'PBKS'}, {'Match Number': 'MATCH 59', 'Home Team': 'CSK', 'Away Team': 'MI'}, {'Match Number': 'MATCH 58', 'Home Team': 'RR', 'Away Team': 'DC'}, {'Match Number': 'MATCH 57', 'Home Team': 'LSG', 'Away Team': 'GT'}, {'Match Number': 'MATCH 56', 'Home Team': 'MI', 'Away Team': 'KKR'}, {'Match Number': 'MATCH 55', 'Home Team': 'CSK', 'Away Team': 'DC'}, {'Match Number': 'MATCH 54', 'Home Team': 'SRH', 'Away Team': 'RCB'}, {'Match Number': 'MATCH 53', 'Home Team': 'LSG', 'Away Team': 'KKR'}, {'Match Number': 'MATCH 52', 'Home Team': 'PBKS', 'Away Team': 'RR'}, {'Match Number': 'MATCH 51', 'Home Team': 'GT', 'Away Team': 'MI'}, {'Match Number': 'MATCH 50', 'Home Team': 'DC', 'Away Team': 'SRH'}, {'Match Number': 'MATCH 49', 'Home Team': 'RCB', 'Away Team': 'CSK'}, {'Match Number': 'MATCH 48', 'Home Team': 'GT', 'Away Team': 'PBKS'}, {'Match Number': 'MATCH 47', 'Home Team': 'KKR', 'Away Team': 'RR'}, {'Match Number': 'MATCH 46', 'Home Team': 'SRH', 'Away Team': 'CSK'}, {'Match Number': 'MATCH 45', 'Home Team': 'DC', 'Away Team': 'LSG'}, {'Match Number': 'MATCH 44', 'Home Team': 'RR', 'Away Team': 'MI'}, {'Match Number': 'MATCH 43', 'Home Team': 'GT', 'Away Team': 'RCB'}, {'Match Number': 'MATCH 42', 'Home Team': 'PBKS', 'Away Team': 'LSG'}, {'Match Number': 'MATCH 41', 'Home Team': 'DC', 'Away Team': 'KKR'}, {'Match Number': 'MATCH 40', 'Home Team': 'GT', 'Away Team': 'SRH'}, {'Match Number': 'MATCH 39', 'Home Team': 'RCB', 'Away Team': 'RR'}, {'Match Number': 'MATCH 38', 'Home Team': 'PBKS', 'Away Team': 'CSK'}, {'Match Number': 'MATCH 37', 'Home Team': 'LSG', 'Away Team': 'MI'}, {'Match Number': 'MATCH 36', 'Home Team': 'RCB', 'Away Team': 'SRH'}, {'Match Number': 'MATCH 35', 'Home Team': 'KKR', 'Away Team': 'GT'}, {'Match Number': 'MATCH 34', 'Home Team': 'DC', 'Away Team': 'RR'}, {'Match Number': 'MATCH 33', 'Home Team': 'MI', 'Away Team': 'CSK'}, {'Match Number': 'MATCH 32', 'Home Team': 'DC', 'Away Team': 'PBKS'}, {'Match Number': 'MATCH 31', 'Home Team': 'LSG', 'Away Team': 'RCB'},{'Match Number': 'MATCH 30', 'Home Team': 'RR', 'Away Team': 'KKR'}, {'Match Number': 'MATCH 29', 'Home Team': 'GT', 'Away Team': 'CSK'}, {'Match Number': 'MATCH 28', 'Home Team': 'PBKS', 'Away Team': 'SRH'}, {'Match Number': 'MATCH 27', 'Home Team': 'DC', 'Away Team': 'RCB'}, {'Match Number': 'MATCH 26', 'Home Team': 'MI', 'Away Team': 'LSG'}, {'Match Number': 'MATCH 25', 'Home Team': 'SRH', 'Away Team': 'KKR'}, {'Match Number': 'MATCH 24', 'Home Team': 'RR', 'Away Team': 'GT'}, {'Match Number': 'MATCH 23', 'Home Team': 'MI', 'Away Team': 'PBKS'}, {'Match Number': 'MATCH 22', 'Home Team': 'CSK', 'Away Team': 'RCB'}, {'Match Number': 'MATCH 21', 'Home Team': 'SRH', 'Away Team': 'GT'}, {'Match Number': 'MATCH 20', 'Home Team': 'RR', 'Away Team': 'LSG'}, {'Match Number': 'MATCH 19', 'Home Team': 'KKR', 'Away Team': 'DC'}, {'Match Number': 'MATCH 18', 'Home Team': 'RCB', 'Away Team': 'MI'}, {'Match Number': 'MATCH 17', 'Home Team': 'CSK', 'Away Team': 'SRH'}, {'Match Number': 'MATCH 16', 'Home Team': 'PBKS', 'Away Team': 'GT'}, {'Match Number': 'MATCH 15', 'Home Team': 'LSG', 'Away Team': 'DC'}, {'Match Number': 'MATCH 14', 'Home Team': 'KKR', 'Away Team': 'MI'}, {'Match Number': 'MATCH 13', 'Home Team': 'RR', 'Away Team': 'RCB'}, {'Match Number': 'MATCH 12', 'Home Team': 'SRH', 'Away Team': 'LSG'}, {'Match Number': 'MATCH 11', 'Home Team': 'CSK', 'Away Team': 'PBKS'}, {'Match Number': 'MATCH 10', 'Home Team': 'GT', 'Away Team': 'DC'}, {'Match Number': 'MATCH 9', 'Home Team': 'MI', 'Away Team': 'RR'}, {'Match Number': 'MATCH 8', 'Home Team': 'KKR', 'Away Team': 'PBKS'}, {'Match Number': 'MATCH 7', 'Home Team': 'LSG', 'Away Team': 'CSK'}, {'Match Number': 'MATCH 6', 'Home Team': 'RCB', 'Away Team': 'KKR'}, {'Match Number': 'MATCH 5', 'Home Team': 'SRH', 'Away Team': 'RR'}, {'Match Number': 'MATCH 4', 'Home Team': 'GT', 'Away Team': 'LSG'}, {'Match Number': 'MATCH 3', 'Home Team': 'RCB', 'Away Team': 'PBKS'}, {'Match Number': 'MATCH 2', 'Home Team': 'DC', 'Away Team': 'MI'}, {'Match Number': 'MATCH 1', 'Home Team': 'CSK', 'Away Team': 'KKR'}]
lis = [{'num': 'FINAL', 'url': 'https://www.iplt20.com/match/2022/531'}, {'num': 'QUALIFIER 2', 'url': 'https://www.iplt20.com/match/2022/530'}, {'num': 'ELIMINATOR', 'url': 'https://www.iplt20.com/match/2022/529'}, {'num': 'QUALIFIER 1', 'url': 'https://www.iplt20.com/match/2022/528'}, {'num': 'MATCH 70', 'url': 'https://www.iplt20.com/match/2022/525'}, {'num': 'MATCH 69', 'url': 'https://www.iplt20.com/match/2022/524'}, {'num': 'MATCH 68', 'url': 'https://www.iplt20.com/match/2022/523'}, {'num': 'MATCH 67', 'url': 'https://www.iplt20.com/match/2022/522'}, {'num': 'MATCH 66', 'url': 'https://www.iplt20.com/match/2022/521'}, {'num': 'MATCH 65', 'url': 'https://www.iplt20.com/match/2022/520'}, {'num': 'MATCH 64', 'url': 'https://www.iplt20.com/match/2022/519'}, {'num': 'MATCH 63', 'url': 'https://www.iplt20.com/match/2022/518'}, {'num': 'MATCH 62', 'url': 'https://www.iplt20.com/match/2022/517'}, {'num': 'MATCH 61', 'url': 'https://www.iplt20.com/match/2022/516'}, {'num': 'MATCH 60', 'url': 'https://www.iplt20.com/match/2022/515'}, {'num': 'MATCH 59', 'url': 'https://www.iplt20.com/match/2022/514'}, {'num': 'MATCH 58', 'url': 'https://www.iplt20.com/match/2022/513'}, {'num': 'MATCH 57', 'url': 'https://www.iplt20.com/match/2022/512'}, {'num': 'MATCH 56', 'url': 'https://www.iplt20.com/match/2022/511'}, {'num': 'MATCH 55', 'url': 'https://www.iplt20.com/match/2022/510'}, {'num': 'MATCH 54', 'url': 'https://www.iplt20.com/match/2022/509'}, {'num': 'MATCH 53', 'url': 'https://www.iplt20.com/match/2022/508'}, {'num': 'MATCH 52', 'url': 'https://www.iplt20.com/match/2022/507'}, {'num': 'MATCH 51', 'url': 'https://www.iplt20.com/match/2022/506'}, {'num': 'MATCH 50', 'url': 'https://www.iplt20.com/match/2022/505'}, {'num': 'MATCH 49', 'url': 'https://www.iplt20.com/match/2022/504'}, {'num': 'MATCH 48', 'url': 'https://www.iplt20.com/match/2022/503'}, {'num': 'MATCH 47', 'url': 'https://www.iplt20.com/match/2022/502'}, {'num': 'MATCH 46', 'url': 'https://www.iplt20.com/match/2022/501'}, {'num': 'MATCH 45', 'url': 'https://www.iplt20.com/match/2022/500'}, {'num': 'MATCH 44', 'url': 'https://www.iplt20.com/match/2022/499'}, {'num': 'MATCH 43', 'url': 'https://www.iplt20.com/match/2022/498'}, {'num': 'MATCH 42', 'url': 'https://www.iplt20.com/match/2022/497'}, {'num': 'MATCH 41', 'url': 'https://www.iplt20.com/match/2022/496'}, {'num': 'MATCH 40', 'url': 'https://www.iplt20.com/match/2022/495'}, {'num': 'MATCH 39', 'url': 'https://www.iplt20.com/match/2022/494'}, {'num': 'MATCH 38', 'url': 'https://www.iplt20.com/match/2022/493'}, {'num': 'MATCH 37', 'url': 'https://www.iplt20.com/match/2022/492'}, {'num': 'MATCH 36', 'url': 'https://www.iplt20.com/match/2022/491'}, {'num': 'MATCH 35', 'url': 'https://www.iplt20.com/match/2022/490'}, {'num': 'MATCH 34', 'url': 'https://www.iplt20.com/match/2022/489'}, {'num': 'MATCH 33', 'url': 'https://www.iplt20.com/match/2022/488'}, {'num': 'MATCH 32', 'url': 'https://www.iplt20.com/match/2022/487'}, {'num': 'MATCH 31', 'url': 'https://www.iplt20.com/match/2022/486'},{'num': 'MATCH 30', 'url': 'https://www.iplt20.com/match/2022/485'}, {'num': 'MATCH 29', 'url': 'https://www.iplt20.com/match/2022/484'}, {'num': 'MATCH 28', 'url': 'https://www.iplt20.com/match/2022/483'}, {'num': 'MATCH 27', 'url': 'https://www.iplt20.com/match/2022/482'}, {'num': 'MATCH 26', 'url': 'https://www.iplt20.com/match/2022/481'}, {'num': 'MATCH 25', 'url': 'https://www.iplt20.com/match/2022/480'}, {'num': 'MATCH 24', 'url': 'https://www.iplt20.com/match/2022/479'}, {'num': 'MATCH 23', 'url': 'https://www.iplt20.com/match/2022/478'}, {'num': 'MATCH 22', 'url': 'https://www.iplt20.com/match/2022/477'}, {'num': 'MATCH 21', 'url': 'https://www.iplt20.com/match/2022/476'}, {'num': 'MATCH 20', 'url': 'https://www.iplt20.com/match/2022/475'}, {'num': 'MATCH 19', 'url': 'https://www.iplt20.com/match/2022/474'}, {'num': 'MATCH 18', 'url': 'https://www.iplt20.com/match/2022/473'}, {'num': 'MATCH 17', 'url': 'https://www.iplt20.com/match/2022/472'}, {'num': 'MATCH 16', 'url': 'https://www.iplt20.com/match/2022/471'}, {'num': 'MATCH 15', 'url': 'https://www.iplt20.com/match/2022/470'}, {'num': 'MATCH 14', 'url': 'https://www.iplt20.com/match/2022/469'}, {'num': 'MATCH 13', 'url': 'https://www.iplt20.com/match/2022/468'}, {'num': 'MATCH 12', 'url': 'https://www.iplt20.com/match/2022/467'}, {'num': 'MATCH 11', 'url': 'https://www.iplt20.com/match/2022/466'}, {'num': 'MATCH 10', 'url': 'https://www.iplt20.com/match/2022/465'}, {'num': 'MATCH 9', 'url': 'https://www.iplt20.com/match/2022/464'}, {'num': 'MATCH 8', 'url': 'https://www.iplt20.com/match/2022/463'}, {'num': 'MATCH 7', 'url': 'https://www.iplt20.com/match/2022/462'}, {'num': 'MATCH 6', 'url': 'https://www.iplt20.com/match/2022/461'}, {'num': 'MATCH 5', 'url': 'https://www.iplt20.com/match/2022/460'}, {'num': 'MATCH 4', 'url': 'https://www.iplt20.com/match/2022/459'}, {'num': 'MATCH 3', 'url': 'https://www.iplt20.com/match/2022/458'}, {'num': 'MATCH 2', 'url': 'https://www.iplt20.com/match/2022/457'}, {'num': 'MATCH 1', 'url': 'https://www.iplt20.com/match/2022/456'}]




hm_tm_aw_tm_lst.reverse()
lis.reverse()
with open(r'C:\Users\Satardhan\OneDrive\Projects\data_2022.txt','r+') as rwf:
    urls = rwf.readlines()
    url_lst = [line.rstrip() for line in urls]
    for i in lis:
        _num = i['num']
        _url = i['url']
        # print(_url)
        if _url in url_lst:continue
        for ele in hm_tm_aw_tm_lst:
            if ele['Match Number'] ==_num:
                driver.quit()
                driver = webdriver.Chrome(options=options)
                hm_tm = ele['Home Team']
                aw_tm = ele['Away Team']
                stad_name,match_date,match_res = get_match_res(_url)
                print(i)
                ball_by_ball(_num,stad_name,match_date,match_res,_url,hm_tm,aw_tm)
                with open(r'C:\Users\Satardhan\OneDrive\Projects\scraping\matches_data2022.txt',"r") as rdf:
                    lins = rdf.readlines()
                    for i in lins:
                        if str(_num) in i:
                            print(_num+" Data written")
                            rwf.write(_url)
                            rwf.write("\n")
                            break
                # input()