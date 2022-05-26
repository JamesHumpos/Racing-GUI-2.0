#! /usr/bin/python
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
    
def RaceCardPress():
    Window3_RaceCard.show(wait = True)
    Window2_TV.hide()
    Window5b_rprice.hide()

def WatchRacePress():
    Window2_TV.show(wait = True)
    Window4b_basic.hide()
    Window5b_rprice.hide()
    Window3_RaceCard.hide()

def ByRaceRC():
    Window4b_basic.show(wait = True)
    Window3_RaceCard.hide()
    Window2_TV.hide()
    Window5b_rprice.hide()

def updateme():
    subprocess.Popen(['python', "/home/james/GUIGIT/autoupdate.py"])

def gethelp():
    webbrowser.get('chromium-browser').open("https://www.jameshumphreys.xyz/help")
    Window4b_basic.hide()
    Window5b_rprice.hide()
    Window2_TV.hide()
    Window3_RaceCard.hide()

def pressed(button):
    if button.pin.number == 15:
        sysCmd.system('sudo killall chromium-browser')

