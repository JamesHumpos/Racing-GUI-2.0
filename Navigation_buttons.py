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
