from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


def getGPAInfo(username="17020781", password="341997mok"):

    # Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('ignore-certificate-errors')
    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver = webdriver.Chrome(
        executable_path='./chromedriver', chrome_options=options)
    url = 'http://daotao.vnu.edu.vn'
    print("Loading url=", url)
    driver.get(url)

    username = driver.find_element_by_id("txtLoginId")
    password = driver.find_element_by_id("txtPassword")
    username.send_keys("17020781")
    password.send_keys("341997mok")

    driver.find_element_by_id("divLogin").submit()

    # try:
    # Get the review details here
    # WebDriverWait(driver, 5).until(
    #     EC.visibility_of_all_elements_located((By.ID, "divMain")))

    # driver.find_element_by_id('PortalModule_386').click()

    url2 = 'https://daotao.vnu.edu.vn/ListPoint/listpoint_Brc1.asp'
    driver.get(url2)

    # WebDriverWait(driver, 10).until(
    #     EC.visibility_of_all_elements_located((By.ID, "divList3")))

    table_id = driver.find_element(By.ID, 'divList3')
    data = []
    terms = []
    term = ''
    subjects = []
    # get all of the rows in the table
    rows = table_id.find_elements(By.TAG_NAME, "tr")
    for row in rows:

        # note: index start from 0, 1 is col 2
        cols = row.find_elements(By.TAG_NAME, "td")

        print(len(cols))
        if len(cols) == 2:
            if len(term) != 0:
                terms.append({term: subjects})
                print(terms)
                subjects = []
            term = cols[0].text[len(cols[0].text)-3: len(cols[0].text)]

        elif len(cols) == 8:

            subjects.append({"code": cols[1].text, "name": cols[2].text, "credit": cols[3].text,
                            "p1": cols[4].text, "p2": cols[5].text, "p3": cols[6].text})
            print(subjects)
        else:
            data.append(cols[0].text)
    data.append(terms)
    print("result :")
    print(len(data))
    print(data[3][0]['202'])

    driver.close()
    return data
