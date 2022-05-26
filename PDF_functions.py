#! /usr/bin/python
def OpenallRC():
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
    webbrowser.get('chromium-browser').open('file:///home/james/GUIGIT/CreatedPDFs/Final.pdf', new=0)
    Window4b_basic.hide()
    Window5b_rprice.hide()
    Window2_TV.hide()
    Window3_RaceCard.hide()

def SimpleMeetingOpen():
    webbrowser.get('chromium-browser').open(Races_By_Meetings.loc[Races_By_Meetings['Meeting'] == SimpleMChoices.value, 'LinksSimple'].iloc[0])
    Window4b_basic.hide()
    Window5b_rprice.hide()
    Window2_TV.hide()
    Window3_RaceCard.hide()
 
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    file = open(filename, 'wb')
    file.write(response.read())
    file.close()
