import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Firefox(executable_path="C:/Users/Florin's PC/Desktop/Web Scrappying/geckodriver.exe")
driver.get("https://www.flashscore.com/match/pjF0g0Um/#match-summary/match-statistics/0")
time.sleep(5)
content = driver.page_source
soup = BeautifulSoup(content,features="html.parser")
driver.quit()
homeTeam = []
awayTeam = []
leagueNameTest = []
homeGoal = []
awayGoal = []
referee = ["Gigi"]
seasonStartDate ="18-06-2020"
date = []
homeStats = []
awayStats = []
allFields = []
defaultHomeStats ={"Ball Possession":"0", "Shots on Goal" : "0", "Shots off Goal" : "0", "Corner Kicks" : "0", "Fouls" : "0", "Red Cards" : "0", "Yellow Cards":"0", "Total Passes": "0" }
defaultAwayStats = {"Ball Possession":"0", "Shots on Goal" : "0", "Shots off Goal" : "0", "Corner Kicks" : "0", "Fouls" : "0", "Red Cards" : "0", "Yellow Cards":"0", "Total Passes": "0" }
awayDic = {}

for element in soup.find_all(attrs="home___bh-s_QB"):
    name = element.find("a", class_="participantName___3lRDM1i")
    if name not in homeTeam:
        homeTeam.append(name.text)

for element in soup.find_all(attrs="away___gdWyBHk"):
    name = element.find("a", class_="participantName___3lRDM1i")
    if name not in awayTeam:
        awayTeam.append(name.text)

for element in soup.find_all(attrs="score___1Gi2Zt8"):
    name = element.find("div",class_="wrapper___3rU3Jah")
    if name not in homeGoal:
        homeGoal.append(name.span.extract().text)

for element in soup.find_all(attrs="score___1Gi2Zt8"):
    name = element.find("div",class_="wrapper___3rU3Jah")
    for s in name:
        awayGoal.append(s.string)
    del awayGoal[0]

for element in soup.find_all(attrs="statCategory___33LOZ_7"):
    name = element.find("div",class_="homeValue___Al8xBea")
    if name not in homeStats:
        homeStats.append(name.text)

for element in soup.find_all(attrs="description___3_uvNAG tournamentHeaderDescription"):
    name = element.find("span",class_="country___24Qe-aj")
    if name not in leagueNameTest:
        leagueNameTest.append(name.text)
    
for element in soup.find_all(attrs="statCategory___33LOZ_7"):
    name = element.find("div", class_="awayValue___SXUUfSH")
    detail = element.find("div", class_="categoryName___3Keq6yi")
    if name not in awayStats:
        awayStats.append(name.text)
    if detail not in allFields:
        allFields.append(detail.text)

for element in soup.find_all(attrs="startTime___2oy0czV"):
    name = element.find("div",class_="")
    if name not in date:
        date.append(name.text)



homeDic = dict(zip(allFields, homeStats))
awayDic = dict(zip(allFields, awayStats))

for key, value in defaultHomeStats.items():
    for k, v in homeDic.items():
        if key == k:
            defaultHomeStats[key] = homeDic[k]

for key, value in defaultAwayStats.items():
    for k, v in awayDic.items():
        if key == k:
            defaultAwayStats[key] = awayDic[k]

        

homeTeamPosessionWithPrecent=homeStats[0]
homeTeamPosession = homeTeamPosessionWithPrecent.replace('%','')
awayTeamPosessionWithPrecent=awayStats[0]
awayTeamPosession = awayTeamPosessionWithPrecent.replace('%','')
dateWithClass = date[0]
normalDate = dateWithClass.replace('.','-')
finalDate = normalDate[0:10]
leagueString = leagueNameTest[0]
finalLeagueName = leagueString[leagueString.find(": ")+2:leagueString.find(" -")]



raw_data={'homeTeam':homeTeam[0],'awayTeam':awayTeam[0], 'leagueName':finalLeagueName,
        'seasonStartDate':seasonStartDate, 'referee':referee, 'homeGoal':homeGoal[0],
        'awayGoal':awayGoal[0], 'homeFault':defaultHomeStats["Fouls"], 'awayFault':defaultAwayStats["Fouls"],
        'homeShotsOnGoal':defaultHomeStats["Shots on Goal"], 'awayShotsOnGoal':defaultAwayStats["Shots on Goal"], 'date':finalDate,
        'homeCorner':defaultHomeStats["Corner Kicks"], 'awayCorner':defaultAwayStats["Corner Kicks"], 'homeRedCard':defaultHomeStats["Red Cards"],
        'awayRedCard':defaultAwayStats["Red Cards"], 'homeYellowCard':defaultHomeStats["Yellow Cards"], 'awayYellowCard':defaultAwayStats["Yellow Cards"],
        'homePosession':homeTeamPosession, 'awayPosession':awayTeamPosession, 'homeTotalPass':defaultHomeStats["Total Passes"],
        'awayTotalPass':defaultAwayStats["Total Passes"],'homeShotsOffGoal':defaultHomeStats["Shots off Goal"], 'awayShotsOffGoal':defaultAwayStats["Shots off Goal"]}
df = pd.DataFrame(raw_data, columns=['homeTeam', 'awayTeam', 'leagueName', 'seasonStartDate','referee',
'homeGoal', 'awayGoal', 'homeFault', 'awayFault', 'homeShotsOnGoal', 'awayShotsOnGoal', 'date', 'homeCorner',
'awayCorner', 'homeRedCard', 'awayRedCard', 'homeYellowCard', 'awayYellowCard', 'homePosession', 'awayPosession',
'homeTotalPass', 'awayTotalPass', 'homeShotsOffGoal', 'awayShotsOffGoal'])
df.to_csv("singleMatchData.csv", index=False, encoding='utf-8',errors="ignore")
