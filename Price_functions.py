#! /usr/bin/python

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
        RPChoice.text_size = 30
        for radio_button in RPChoice.children:
            radio_button.tk.config(borderwidth=12)
            radio_button.tk.config(bg="gainsboro")
            radio_button.tk.config(relief="raised")
    else:
        RPChoice = ButtonGroup(Boxraceprice2, options=RacesAPIChoice["time"],command=RPChoiceBut,width="fill",height="fill",align="right")
        RPChoice.text_size = 30
        for radio_button in RPChoice.children:
            radio_button.tk.config(borderwidth=12)
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
            pricebookielist.append(price)
    livepricedf = ({'Horse':horselist,'Number':numberlist,'Jockey / Trainer':jockeytrainerlist,'Age':agelist,
                'Weight':weightlist,'NR':nonrunnerlist})
    livepricedf = pd.DataFrame(data=livepricedf)
    horsepricedf = ({'Horse':horsepricelist,'Price':pricelist,'Bookie':bookielist,'Odds_Bet365':pricebookielist})
    horsepricedf = pd.DataFrame(data=horsepricedf)
    horsepricedf=horsepricedf[horsepricedf.Bookie == "Bet365"]
    global horseraceall
    horseraceall = pd.merge(livepricedf, horsepricedf, on="Horse", how="left")
    horseraceall['Price'] = horseraceall['Price'].fillna(0)
    horseraceall['Bookie'] = horseraceall['Bookie'].fillna(0)
    horseraceall['Running'] = horseraceall.NR.replace(to_replace=["0", "1"], value=['yes', 'no'])
    new_cols = ["Horse","Number","Odds_Bet365","Age","Weight","Jockey / Trainer","Running"]
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
    tv.column("Odds_Bet365",width=120)
    tv.column("Weight",width=60)
    tv.column("Running",width=70)
    tv.column("Number",width=50)
    tv.column("Jockey / Trainer",width=290)
    chosendata_rows = chosendata.to_numpy().tolist()
    for row in chosendata_rows:
        tv.insert("","end",values=row)
    Window5b_rprice.add_tk_widget(tv)
    Window5b_rprice.show()
