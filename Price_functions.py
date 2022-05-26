#! /usr/bin/python
from Import_modules import * ## import external functions
def changeschoice(chosen_race):
    chosen_race = chosen_race
    #global chosen_race
    getodds(chosen_race)
    
APIheaders = {
    'X-RapidAPI-Host': "horse-racing.p.rapidapi.com",
    'X-RapidAPI-Key': "cf6e098d1bmsh3d8cf5fffc03b52p153d87jsn3bae94c34116"
    }

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
    

