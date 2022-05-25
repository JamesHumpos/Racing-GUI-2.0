#! /usr/bin/python
from guizero import App, Text, PushButton, Window, ButtonGroup, Box, info, yesno, error, ListBox
import webbrowser
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import os as sysCmd
import time
from gpiozero import Button as PhsyicalButton
from signal import pause
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tkinter.font import names
import psutil
import shutil
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import subprocess
import http.client
import pathlib
import json
from datetime import date
from tabulate import tabulate as tb
from tkinter import ttk
import tkinter as tkintopt
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time as pause
import sys as sysname


def updateme():
    subprocess.Popen(['python', "/home/james/GUIGIT/autoupdate.py"])
    sysname.exit(0)

### Once AT TOP prices


quoteurl = "https://andruxnet-random-famous-quotes.p.rapidapi.com/"

quotequerystring = {"cat":"famous","count":"1"}

quoteheaders = {
    "X-RapidAPI-Host": "andruxnet-random-famous-quotes.p.rapidapi.com",
    "X-RapidAPI-Key": "5e3da382c8msh1e45f5a643c7123p16a959jsna7f55c284038"
}

quoteresponse = requests.get(quoteurl, headers=quoteheaders, params=quotequerystring)
quotejson_data = json.loads(quoteresponse.text)
famousquote = quotejson_data[0]['quote']
famousauthor = quotejson_data[0]['author']



today = date.today()
conn = http.client.HTTPSConnection("horse-racing.p.rapidapi.com")

APIheaders = {
    'X-RapidAPI-Host': "horse-racing.p.rapidapi.com",
    'X-RapidAPI-Key': "5e3da382c8msh1e45f5a643c7123p16a959jsna7f55c284038"
    }

conn.request("GET", "/racecards?date={}".format(today), headers=APIheaders)
res = conn.getresponse()
data = res.read()

pathlib.Path('/home/james/GUIGIT/data.json').write_bytes(data)
df = pd.read_json('/home/james/GUIGIT/data.json')
df['time'] = df["date"].astype(str).str.extract('(\d+:\d+:\d+)')
RacesAPI = df[["course", "time","id_race"]]

Courses = RacesAPI['course']
Courses = Courses.unique()

def HomePress2():
    Window4b_basic.hide()
    Window3_RaceCard.hide()
    Window2_TV.hide()
    Window5_mprice.hide()
    Window5a_rprice.hide()
    Window5b_rprice.hide()
    
   
def HomePress():
    Window4b_basic.hide()
    Window3_RaceCard.hide()
    Window2_TV.hide()
    Window5_mprice.hide()
    Window5a_rprice.hide()
    Window5b_rprice.hide()

def PricesPress():
    Window5_mprice.show(wait = True)
    Window2_TV.hide()
    Window3_RaceCard.hide()
    Window2_TV.hide()
    
### Each time prices clicked

#def maketkexample():
#    style = ttk.Style()
#    style.configure("Treeview.Heading", highlightthickness=4, bd=0, font=('Calibri', 50))
#    tv = ttk.Treeview(Window5b_rprice.tk,style="Treeview.Heading")
#    Window5b_rprice.add_tk_widget(tv)
#    Window5b_rprice.show()

def MPChoiceBut():
    global Choiceone
    Choiceone = MPChoice.value
    print(MPChoice.value)
    MeetingTimeProd(Choiceone)

def MeetingTimeProd(MeetingChosen):
    RacesAPIChoice=RacesAPI[RacesAPI.course == MeetingChosen]
    print(RacesAPIChoice)
    print(MeetingChosen)
    global RPChoice
    if 'RPChoice' in globals():
        RPChoice.destroy()
        RPChoice = ButtonGroup(Boxraceprice2, options=RacesAPIChoice["time"],command=RPChoiceBut,width="fill",height="fill",align="right")
        RPChoice.text_size = 25
        for radio_button in RPChoice.children:
            radio_button.tk.config(borderwidth=10)
            radio_button.tk.config(bg="gainsboro")
            radio_button.tk.config(relief="raised")
    else:
        RPChoice = ButtonGroup(Boxraceprice2, options=RacesAPIChoice["time"],command=RPChoiceBut,width="fill",height="fill",align="right")
        RPChoice.text_size = 25
        for radio_button in RPChoice.children:
            radio_button.tk.config(borderwidth=10)
            radio_button.tk.config(bg="gainsboro")
            radio_button.tk.config(relief="raised")
    #for times in RacesAPIChoice["time"]:
        #RPChoice.append(times)
    print(RacesAPIChoice["time"])
    Window5_mprice.hide()
    Window5a_rprice.show()
    
def RPChoiceBut():
    global chosen_race
    chosen_race = RacesAPI.loc[RacesAPI['time'] == RPChoice.value, 'id_race'].iloc[0]
    changeschoice(chosen_race)

def changeschoice(chosen_race):
    chosen_race = chosen_race
    #global chosen_race
    getodds(chosen_race)
    
def getodds(chosen_race):
    conn = http.client.HTTPSConnection("horse-racing.p.rapidapi.com")
    conn.request("GET", "/race/{}".format(chosen_race), headers=APIheaders)
    raceres = conn.getresponse()
    racedata = raceres.read()
    cleanracedata(json.loads(racedata.decode('utf-8')))
    
def cleanracedata(racedata):
    horselist=[]
    jockeytrainerlist=[]
    agelist=[]
    weightlist=[]
    numberlist=[]
    nonrunnerlist=[]
    pricelist=[]
    bookielist=[]
    horsepricelist=[]
    pricebookielist=[]
    for eachhorse in racedata["horses"]:
        horse = eachhorse["horse"]
        jockey = eachhorse["jockey"]
        trainer = eachhorse["trainer"]
        age = eachhorse["age"]
        weight = eachhorse["weight"]
        number = eachhorse["number"]
        non_runner = eachhorse["non_runner"]
        horselist.append(horse)
        jockeytrainerlist.append(jockey + " / " + trainer)
        agelist.append(age)
        weightlist.append(weight)
        numberlist.append(number)
        nonrunnerlist.append(non_runner)
        for eachodd in eachhorse["odds"]:
            bookie = eachodd["bookie"]
            price = eachodd["odd"]
            pricelist.append(price)
            bookielist.append(bookie)
            horseprice = horse
            horsepricelist.append(horseprice)
            pricebookielist.append(price + " at " + bookie)
    livepricedf = ({'Horse':horselist,'Number':numberlist,'Jockey / Trainer':jockeytrainerlist,'Age':agelist,
                'Weight':weightlist,'NR':nonrunnerlist})
    livepricedf = pd.DataFrame(data=livepricedf)
    horsepricedf = ({'Horse':horsepricelist,'Price':pricelist,'Bookie':bookielist,'Odds':pricebookielist})
    horsepricedf = pd.DataFrame(data=horsepricedf)
    horsepricedf=horsepricedf[horsepricedf.Bookie == "Bet365"]
    global horseraceall
    horseraceall = pd.merge(livepricedf, horsepricedf, on="Horse", how="left")
    horseraceall['Price'] = horseraceall['Price'].fillna(0)
    horseraceall['Bookie'] = horseraceall['Bookie'].fillna(0)
    horseraceall['Running'] = horseraceall.NR.replace(to_replace=["0", "1"], value=['yes', 'no'])
    new_cols = ["Horse","Number","Odds","Age","Weight","Jockey / Trainer","Running"]
    horseraceall=horseraceall[new_cols]
    Window5a_rprice.hide()
    showtable(horseraceall)
    
def showtable(chosendata):
    def HomePress2():
        Window5b_rprice.hide()
    Window5b_rprice = Window(app, title="Prices", visible=False, width=1500, height = 800)
    Homebuttonpricer = PushButton(Window5b_rprice, command=HomePress2,text="HOME", width=80, height = 2)
    Homebuttonpricer.text_color = "white"
    Homebuttonpricer.bg = "red"
    Homebuttonpricer.text_size = 20
    style = ttk.Style()
    style.configure("Treeview.Heading", highlightthickness=4, bd=0, font=('Calibri', 15))
    tv = ttk.Treeview(Window5b_rprice.tk,style="Treeview.Heading")
    tv["columns"]=list(chosendata.columns)
    tv["show"]="headings"
    for columns in tv["columns"]:
        tv.heading(columns,text=columns)
    tv.column("Horse",width=180)
    tv.column("Age",width=50)
    tv.column("Odds",width=120)
    tv.column("Weight",width=60)
    tv.column("Running",width=70)
    tv.column("Number",width=50)
    tv.column("Jockey / Trainer",width=290)
    chosendata_rows = chosendata.to_numpy().tolist()
    for row in chosendata_rows:
        tv.insert("","end",values=row)
    Window5b_rprice.add_tk_widget(tv)
    Window5b_rprice.show()




horseraceall=[]


############################################ URLS WE'LL USE ####################################################

cardsurl = "https://www.attheraces.com"
betsurl = "https://m.skybet.com"

############################################ LISTS WE'LL POPULATE LATER ##########################################

namelist=[]
oddslinks=[]
oddsraces=[]
horsepricepairlist =[]
linkssimple=[]
meetinglist=[]
namedf=[]

############################## State which URL we're getting our race cards from ##################################

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

#If there is no such folder, the script will create one automatically
folder_location = r'/home/james/GUIGIT/CreatedPDFs'
if sysCmd.path.exists(folder_location):shutil.rmtree(folder_location)
if not sysCmd.path.exists(folder_location):sysCmd.mkdir(folder_location)


## Request info from the ATR races printout page
souplink = requests.get("https://www.attheraces.com/printouts/", headers=headers)
soup = BeautifulSoup(souplink.content,"lxml")

############################################## GET MEETING NAME LIST ##############################################

for meeting in soup.find_all("h3","h6"):
    name = meeting.get_text()
    namelist.append(name)

############################################ BUTTON TO KILL CHROMIUM ##############################################
    
home_button = PhsyicalButton(15)
off_button = PhsyicalButton(24)

def pressed(button):
    if button.pin.number == 15:
        sysCmd.system('sudo killall chromium-browser')

    
############################################## CARDS SET UP ######################################################

def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    file = open(filename, 'wb')
    file.write(response.read())
    file.close()

filenamelist=[]
linkssimple=[]
meetinglist=[]
for race in soup.find_all('section', {'class':'panel push--x-small'}):
    for link in race.select("a[href$='allcardsatrformracecard.pdf']"):
        links_full = urljoin(cardsurl,link['href'])
        linkssimple.append(links_full)
        meetingname = race.find("h3","h6")
        meetinglist.append(meetingname)
        print(links_full)
        filename = sysCmd.path.join(folder_location,link['href'].split('/')[-1])
        filenamelist.append(filename)
        download_file(links_full, filename)
        
merger = PdfFileMerger()

for pdf in filenamelist:
    merger.append(pdf)

merger.write("/home/james/GUIGIT/CreatedPDFs/TodaysRacesSimple.pdf")
merger.close()

filename = "/home/james/GUIGIT/CreatedPDFs/TodaysRacesSimple.pdf"
cmd = f"pdf-crop-margins -v -s -u {filename} -o /home/james/GUIGIT/CreatedPDFs/TodaysRaces.pdf"
proc = subprocess.Popen(cmd.split())
proc.wait()

output = PdfFileWriter() 
input = PdfFileReader(open("/home/james/GUIGIT/CreatedPDFs/TodaysRaces.pdf", 'rb')) 

n = input.getNumPages()

for i in range(n):
  page = input.getPage(i)
  page.cropBox.upperLeft = (577,750)
  page.cropBox.upperRight = (17,750)
  page.cropBox.lowerLeft = (577,30)
  page.cropBox.lowerRight = (17,30)
  output.addPage(page) 
  
outputStream = open("/home/james/GUIGIT/CreatedPDFs/Final.pdf",'wb') 
output.write(outputStream) 
outputStream.close()
        
linkssimple=[]
meetinglist=[]
namedf=[]

for race in soup.find_all('section', {'class':'panel push--x-small'}):
    for link in race.select("a[href$='atrformracecard.pdf']"):
        links_full = urljoin(cardsurl,link['href'])
        linkssimple.append(links_full)
        meetingname = race.find("h3","h6")
        meetinglist.append(meetingname)

for i in soup.find_all("h3", "h7"):
    if i.text != 'Printouts not yet available':
        namedf.append(i)

s = ({'Meeting':meetinglist,'Races':namedf,'LinksSimple':linkssimple})
s = pd.DataFrame(data=s)
name = s['Races'].iloc[0]
Races_By_Meetings = s.loc[s['Races'] == name]
Races_By_Times = s.loc[s['Races'] != name]

Races_By_Meetings = Races_By_Meetings.explode(column="Meeting",ignore_index=True)
MeetingListExc = Races_By_Meetings['Meeting']
unique_meeting_list = MeetingListExc.unique()
Races_By_Meetings = Races_By_Meetings.explode(column="Races",ignore_index=True)
Races_By_Meetings['Meeting'] ='All at ' + Races_By_Meetings['Meeting']
Races_By_Meetings = Races_By_Meetings[['Meeting', 'LinksSimple']]



Races_By_Times = Races_By_Times.explode(column="Races",ignore_index=True)
Races_By_Times = Races_By_Times.explode(column="Meeting",ignore_index=True)
Races_By_Times['Times'] = Races_By_Times.Races.str.extract('(\d+:\d+)')
Races_By_Times['Meeting-Time'] = Races_By_Times['Meeting'] + '  -  ' + Races_By_Times['Times']
Races_By_Times['Time1'] = pd.to_datetime(Races_By_Times['Times'], format='%H:%M').dt.time
Races_By_Times = Races_By_Times.sort_values(by='Time1')
Races_By_Times = Races_By_Times[['Meeting-Time', 'LinksSimple']]



   ########################################## BETS SET UP ############################################

    
    
## Request info from the SkyBet odds page
souplink = requests.get("https://m.skybet.com/horse-racing/meetings", headers=headers)
soup = BeautifulSoup(souplink.content,"lxml")


for racepanel in soup.find_all('div', {'class':'cell--link race-grid-col'}):
    for race in racepanel.find("b","cell-text__line"):
        meetingname = racepanel.text
        oddsraces.append(meetingname)
    for link in racepanel.select('a'):
        links = link['href']
        linksfull = urljoin(betsurl,links)
        oddslinks.append(linksfull)


## OLD
def RaceB1Open():
    webbrowser.get('chromium-browser').open(RaceOddsLinks.loc[RaceOddsLinks['Times'] == button1.text, 'Link'].iloc[0])
    Window5b_rprice.hide()
    Window3_RaceCard.hide()
    Window2_TV.hide()
        
def RaceCardPress():
    Window3_RaceCard.show(wait = True)
    Window2_TV.hide()
    Window5b_rprice.hide()

def WatchRacePress():
    Window2_TV.show(wait = True)
    Window4b_basic.hide()
    Window5b_rprice.hide()
    Window3_RaceCard.hide()

        
def OpenallRC():
    webbrowser.get('chromium-browser').open('file:///home/james/GUIGIT/CreatedPDFs/Final.pdf', new=0)
    Window4b_basic.hide()
    Window5b_rprice.hide()
    Window2_TV.hide()
    Window3_RaceCard.hide()
        
def ByRaceRC():
    Window4b_basic.show(wait = True)
    Window3_RaceCard.hide()
    Window2_TV.hide()
    Window5b_rprice.hide()

def SimpleMeetingOpen():
    webbrowser.get('chromium-browser').open(Races_By_Meetings.loc[Races_By_Meetings['Meeting'] == SimpleMChoices.value, 'LinksSimple'].iloc[0])
    Window4b_basic.hide()
    Window5b_rprice.hide()
    Window2_TV.hide()
    Window3_RaceCard.hide()
        
def watchpaddy():
    username = "timegan40"
    password = "Grandadbet123!"
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
    driver.get("https://identitysso.paddypower.com/view/login?product=registration-web&url=https%3A%2F%2Fwww.paddypower.com%2Fbet%3F")
    pause.sleep(4)
    button = driver.find_element_by_id("onetrust-accept-btn-handler")
    button.click()
    pause.sleep(2)
    driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div/form/fieldset/div[1]/div/input").send_keys(username)
    driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div/form/fieldset/div[2]/div/div/input").send_keys(password)
    pause.sleep(2)
    button = driver.find_element_by_id("login")
    button.click()
    pause.sleep(9)
    button = driver.find_element_by_xpath("/html/body/div/page-container/div/main/div/content-managed-page/div/div[2]/div/div[2]/card-next-races/div/abc-card/div/div/abc-card-content/div/div[2]/div[1]/abc-race-sub-header/section/a")
    button.click()
    pause.sleep(10)
    button = driver.find_element_by_id("videoController")
    button.click()
    Window4b_basic.hide()
    Window5b_rprice.hide()
    Window2_TV.hide()
    Window3_RaceCard.hide()
    
def gethelp():
    webbrowser.get('chromium-browser').open("https://www.jameshumphreys.xyz/help")
    Window4b_basic.hide()
    Window5b_rprice.hide()
    Window2_TV.hide()
    Window3_RaceCard.hide()

                                    ## Simple GUI for navigating the days races


                                            ## Window 0 -  Home page

app = App(title="RacePad", bg="white", width=1500, height = 800)
MeetingsTodaytitle = Text(app, text= "Meetings Today:", size=25)
MeetingNames = Text(app, text=namelist, size=25)
MeetingNames.text_color = "green"

RaceCardBtnBox = Box(app,align="left",height="fill",width="fill")
LivePriceBtnBox = Box(app,align="left",height="fill",width="fill")  
WatchBtnBox = Box(app,align="left",height="fill",width="fill")
QuoteBox = Box(app,align="bottom",height="fill",width="fill")
HelpBox = Box(app,align="bottom",height="fill",width="fill")

RaceCardButton = PushButton(RaceCardBtnBox, command=RaceCardPress, image="/home/james/GUIGIT/HomePageImages/CArds.png")
LivePriceButton = PushButton(LivePriceBtnBox, command=PricesPress, image="/home/james/GUIGIT/HomePageImages/PRices.png")
WatchRaceButton = PushButton(WatchBtnBox, command=WatchRacePress, image="/home/james/GUIGIT/HomePageImages/Watch.png")

QuoteText = Text(app,align="top",text=famousquote)
QuoteText.text_size=15
AuthorText= Text(app,align="bottom",text=famousauthor)
AuthorText.text_size=8

UpdateButton = PushButton(HelpBox,command=updateme,text="UPDATE",align="bottom")
UpdateButton.text_size=25
UpdateButton.bg="green"
UpdateButton.text_color = "white"

HelpButton = PushButton(HelpBox,command=gethelp,text="HELP",align="bottom")
HelpButton.text_size=25
HelpButton.bg="red"
HelpButton.text_color = "white"
home_button.when_pressed = pressed
##home_button.wait_for_press()

                    ######################### Window 2a - Meeting price choice ################################
Window5_mprice = Window(app, title="Prices: Which meeting?", visible=False, width=1500, height = 800)
Window5_mprice.bg="white"
Homebutton0 = PushButton(Window5_mprice, command=HomePress,text="HOME", width=80, height = 2)
Homebutton0.text_color = "white"
Homebutton0.bg = "red"
Homebutton0.text_size = 20

buttons_mpricebox = Box(Window5_mprice, height="fill",width="fill")

## Button by meeting
MPChoiceb1 = Box(buttons_mpricebox,align="left",width="fill",height="fill")
MPChoiceb3 = Box(buttons_mpricebox,align="left",width="fill",height="fill")
MPChoice = ButtonGroup(buttons_mpricebox, options=Courses, command=MPChoiceBut,width="fill",height="fill",align="left")
MPChoice.text_size = 30
MPChoice.text_color = "black"
MPChoice.bg = "white"

for radio_button in MPChoice.children:
    radio_button.tk.config(borderwidth=10)
    radio_button.tk.config(bg="gainsboro")
    radio_button.tk.config(relief="raised")


MPChoiceb3 = Box(buttons_mpricebox,align="left",width="fill",height="fill")




                 ######################## Window 5b - Race price choice ###################################
Window5a_rprice = Window(app, title="Prices: which race?", visible=False, width=1500, height = 800)
Homebuttonprice = PushButton(Window5a_rprice, command=HomePress,text="HOME", width=80, height = 2)
Homebuttonprice.text_color = "white"
Homebuttonprice.bg = "red"
Homebuttonprice.text_size = 20

Boxraceprice1 = Box(Window5a_rprice,height="fill",width="fill",align="left")
Boxraceprice1a = Box(Window5a_rprice,height="fill",width="fill",align="left")
Boxraceprice2 = Box(Window5a_rprice,height="fill",width="fill",align="left")
Boxraceprice3 = Box(Window5a_rprice,height="fill",width="fill",align="left")


                 ######################## Window 5c - Race price result ###################################
Window5b_rprice = Window(app, title="Prices", visible=False, width=1500, height = 800)
Homebuttonpricer = PushButton(Window5b_rprice, command=HomePress2,text="HOME", width=80, height = 2)
Homebuttonpricer.text_color = "white"
Homebuttonpricer.bg = "red"
Homebuttonpricer.text_size = 20




                                                      ## Window 2 - Racing TV choice

Window2_TV = Window(app, title="Watch the latest race on Paddy power", visible=False, width=1500, height = 800)
Window2_TV.bg="white"
Homebutton1 = PushButton(Window2_TV, command=HomePress,text="HOME", width=80, height = 2)
Homebutton1.text_color = "white"
Homebutton1.bg = "red"
Homebutton1.text_size = 20

PPbutton = PushButton(Window2_TV, command=watchpaddy,text="Press to Watch Live, be patient", width=80, height = 5)
PPbutton.text_size = 40
PPbutton.text_color = "black"

PPbutton.tk.config(borderwidth=10)
PPbutton.tk.config(bg="gainsboro")
PPbutton.tk.config(relief="raised")




                                                     ## Window 3 - Card level choice
Window3_RaceCard = Window(app, title="ChooseRaceCards",visible=False, width=1500, height = 800)
Window3_RaceCard.bg="white"

Homebutton2 = PushButton(Window3_RaceCard, command=HomePress,text="HOME", width=80, height = 2)
Homebutton2.text_color = "white"
Homebutton2.bg = "red"
Homebutton2.text_size = 20

WhichCardsTitle = Text(Window3_RaceCard, text= "Do you want to see all races today or one at a time?", size=30)

DetailedCardsButton = PushButton(Window3_RaceCard, command=OpenallRC,text="ALL racecards in one", width=40, height = 4)
DetailedCardsButton.text_size = 35
DetailedCardsButton.bg = "white"

DetailedCardsButton.tk.config(borderwidth=7)
DetailedCardsButton.tk.config(bg="gainsboro")
DetailedCardsButton.tk.config(relief="raised")

BasicCardsButton = PushButton(Window3_RaceCard, command=ByRaceRC,text="ONE race at a time", width=40, height = 4)
BasicCardsButton.text_size = 35
BasicCardsButton.bg = "white"

BasicCardsButton.tk.config(borderwidth=7)
BasicCardsButton.tk.config(bg="gainsboro")
BasicCardsButton.tk.config(relief="raised")



                                                    ## Window 4b - Basic Card choice
    
Window4b_basic = Window(app, title="Racecards", visible=False, width=1500, height = 800)
Window4b_basic.hide()

Homebutton4 = PushButton(Window4b_basic, command=HomePress,text="HOME", width=80, height = 2)
Homebutton4.text_size = 20
Homebutton4.text_color = "white"
Homebutton4.bg = "red"

buttons_box0 = Box(Window4b_basic, height="fill",width="fill",align="left")
buttons_box0b = Box(Window4b_basic, height="fill",width="fill",align="left")
buttons_box1 = Box(Window4b_basic, height="fill",width="fill",align="left")
buttons_box2 = Box(Window4b_basic, height="fill",width="fill",align="left")

## BUtton by meeting
SimpleMChoices = ButtonGroup(buttons_box1, options=Races_By_Meetings['Meeting'], selected=Races_By_Meetings['Meeting'].iloc[0], command=SimpleMeetingOpen,width="fill",height="fill")
SimpleMChoices.text_size = 25
SimpleMChoices.text_color = "black"
SimpleMChoices.bg = "white"
for radio_button in SimpleMChoices.children:
    radio_button.tk.config(borderwidth=7)
    radio_button.tk.config(bg="gainsboro")
    radio_button.tk.config(relief="raised")


## Show app

app.display()



