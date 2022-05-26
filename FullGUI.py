#! /usr/bin/python
from Import_modules import * ## import external functions
from Navigation_buttons import * ## buttons that dictate user's movement through GUI
from Price_functions import * ## buttons that relate to fetching prices
from Watch_functions import * ## buttons that relate to live streaming
from PDF_functions import * ## buttons that relate to PDF creation


### Create famous quote for homepage from API
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

## Get a list of each race on today with respective UIDs 
today = date.today()
conn = http.client.HTTPSConnection("horse-racing.p.rapidapi.com")

APIheaders = {
    'X-RapidAPI-Host': "horse-racing.p.rapidapi.com",
    'X-RapidAPI-Key': "cf6e098d1bmsh3d8cf5fffc03b52p153d87jsn3bae94c34116"
    }

conn.request("GET", "/racecards?date={}".format(today), headers=APIheaders)
res = conn.getresponse()
data = res.read()

## Download and parse response JSON
pathlib.Path('/home/james/GUIGIT/data.json').write_bytes(data)
df = pd.read_json('/home/james/GUIGIT/data.json')
df['time'] = df["date"].astype(str).str.extract('(\d+:\d+:\d+)')
RacesAPI = df[["course", "time","id_race"]]

Courses = RacesAPI['course']
Courses = Courses.unique()
horseraceall=[]


############################################ URL FOR RACE CARDS WE'LL USE ####################################################

cardsurl = "https://www.attheraces.com"

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

############################################## GET MEETING NAME LIST IN REQ FORMAT ##############################################

for meeting in soup.find_all("h3","h6"):
    name = meeting.get_text()
    namelist.append(name)

############################################ BUTTON TO KILL CHROMIUM ##############################################
    
home_button = PhsyicalButton(15)
off_button = PhsyicalButton(24)
    
############################################## CARDS SET UP ######################################################



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

## merge all PDFs
for pdf in filenamelist:
    merger.append(pdf)
    
## merge all PDFs
merger.write("/home/james/GUIGIT/CreatedPDFs/TodaysRacesSimple.pdf")
merger.close()
        
       
linkssimple=[]
meetinglist=[]
namedf=[]

## Create meeting by meeting option list with links to respective PDFs if all together not required
for race in soup.find_all('section', {'class':'panel push--x-small'}):
    for link in race.select("a[href$='atrformracecard.pdf']"):
        links_full = urljoin(cardsurl,link['href'])
        linkssimple.append(links_full)
        meetingname = race.find("h3","h6")
        meetinglist.append(meetingname)
        
## in case these are not uploaded yet
for i in soup.find_all("h3", "h7"):
    if i.text != 'Printouts not yet available':
        namedf.append(i)

s = ({'Meeting':meetinglist,'Races':namedf,'LinksSimple':linkssimple})
s = pd.DataFrame(data=s)
name = s['Races'].iloc[0]
Races_By_Meetings = s.loc[s['Races'] == name]
Races_By_Times = s.loc[s['Races'] != name]

## clean race/meeting names
Races_By_Meetings = Races_By_Meetings.explode(column="Meeting",ignore_index=True)
MeetingListExc = Races_By_Meetings['Meeting']
unique_meeting_list = MeetingListExc.unique()
Races_By_Meetings = Races_By_Meetings.explode(column="Races",ignore_index=True)
Races_By_Meetings['Meeting'] ='All at ' + Races_By_Meetings['Meeting']
Races_By_Meetings = Races_By_Meetings[['Meeting', 'LinksSimple']]



                                    ## Simple GUI for navigating the days races


                                            ## Window 0 -  Home page

app = App(title="RacePad", bg="white", width=1300, height = 800)
MeetingsTodaytitle = Text(app, text= "Meetings Today:", size=25)
MeetingNames = Text(app, text=namelist, size=25)
MeetingNames.text_color = "green"

ButtonsBtnBox = Box(app,align="top",height="fill",width="fill")

RaceCardBtnBox = Box(ButtonsBtnBox,align="left",height="fill",width="fill")
LivePriceBtnBox = Box(ButtonsBtnBox,align="left",height="fill",width="fill")  
WatchBtnBox = Box(ButtonsBtnBox,align="left",height="fill",width="fill")

RaceCardButton = PushButton(RaceCardBtnBox, command=RaceCardPress, image="/home/james/GUIGIT/HomePageImages/CArds.png")
LivePriceButton = PushButton(LivePriceBtnBox, command=PricesPress, image="/home/james/GUIGIT/HomePageImages/PRices.png")
WatchRaceButton = PushButton(WatchBtnBox, command=WatchRacePress, image="/home/james/GUIGIT/HomePageImages/Watch.png")

QuoteBox = Box(app,align="top",height="fill",width="fill")
QuoteText = Text(QuoteBox,text=famousquote,align="bottom")
QuoteText.text_size=21
AuthorBox = Box(app,align="top",height="fill",width="fill")
AuthorText= Text(AuthorBox,align="top",text=famousauthor)
AuthorText.text_size=18

HelpBox = Box(app,align="bottom",height="fill",width="fill")
UpdateButton = PushButton(HelpBox,command=updateme,text="UPDATE",align="bottom")
UpdateButton.text_size=20
UpdateButton.bg="green"
UpdateButton.text_color = "white"

HelpButton = PushButton(HelpBox,command=gethelp,text="HELP",align="bottom")
HelpButton.text_size=20
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
MPChoice.text_size = 32
MPChoice.text_color = "black"
MPChoice.bg = "white"

for radio_button in MPChoice.children:
    radio_button.tk.config(borderwidth=12)
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

PPbutton = PushButton(Window2_TV, command=watchpaddy,text="Press to Watch Live, be patient", width=60, height = 3)
PPbutton.text_size = 32
PPbutton.text_color = "black"

PPbutton.tk.config(borderwidth=12)
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
SimpleMChoices.text_size = 32
SimpleMChoices.text_color = "black"
SimpleMChoices.bg = "white"
for radio_button in SimpleMChoices.children:
    radio_button.tk.config(borderwidth=12)
    radio_button.tk.config(bg="gainsboro")
    radio_button.tk.config(relief="raised")


## Show app

app.display()
