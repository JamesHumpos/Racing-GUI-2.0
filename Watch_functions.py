#! /usr/bin/python

from Import_modules import * ## import external functions
def watchpaddy2():
    username = "SECRET"
    password = "SECRET"
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
    driver.get("https://identitysso.paddypower.com/view/login?product=registration-web&url=https%3A%2F%2Fwww.paddypower.com%2Fbet%3F")
    Window4b_basic.hide()
    Window5b_rprice.hide()
    Window2_TV.hide()
    Window3_RaceCard.hide()
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


def watchpaddy():
    username = "SECRET"
    password = "SECRET"
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
    wait=WebDriverWait(driver,20)
    driver.get("https://identitysso.paddypower.com/view/login?product=registration-web&url=https%3A%2F%2Fwww.paddypower.com%2Fbet%3F")
    buttonpath1 = "onetrust-accept-btn-handler"
    button1 = wait.until(EC.element_to_be_clickable((By.ID, buttonpath1)))
    button1.click()
    pause.sleep(2)
    driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div/form/fieldset/div[1]/div/input").send_keys(username)
    driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div/form/fieldset/div[2]/div/div/input").send_keys(password)
    pause.sleep(2)
    buttonpath2 = "login"
    button2 = wait.until(EC.element_to_be_clickable((By.ID, buttonpath2)))
    button2.click()
    buttonpath3 = "/html/body/div/page-container/div/main/div/content-managed-page/div/div[2]/div/div[2]/card-next-races/div/abc-card/div/div/abc-card-content/div/div[2]/div[1]/abc-race-sub-header/section/a"
    button3 = wait.until(EC.element_to_be_clickable((By.XPATH, buttonpath3)))
    button3.click()
    while True:
        if len(driver.find_elements(By.XPATH,"/html/body/div/iframe")) > 0:
            break
        driver.refresh()
    frame = driver.find_element_by_xpath("/html/body/div/iframe")
    driver.switch_to.frame(frame)
    xpath = "/html/body/div[1]/div"
    #tab = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    tab = driver.find_element(By.CSS_SELECTOR("iconPlayPause"))
    tab.click()
    
