from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import sys
import csv



def browser_init():
    #intiate a headless chrome browser
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    
    return driver

def check_pwned_passwords(browser):
    #check if the password is pwned
    browser.get('https://haveibeenpwned.com/Passwords')
    #wait for the page to load
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "Password")))
    #open file for input
    with open(sys.argv[1], "r") as input:
        #open file for output
        with open(sys.argv[2], "w") as output:
            read = csv.reader(input, delimiter=",")

            write = csv.writer(output, delimiter=",")
            #write the header
            write.writerow(["Password", "IsPwned", "Number of times Pwned"])

            #loop through the rows
            for row in read:
                pwd = row[0]
                if(pwd != "Password"):
                    #enter the password
                    Password = browser.find_element_by_id("Password")
                    Password.click()
                    Password.send_keys(pwd)
                    #click the search button
                    browser.find_element_by_id("searchPwnedPasswords").click()
                    #wait for the page to load
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-expanded="true"]')) or EC.text_to_be_present_in_element_attribute((By.ID, "loading"), "style", "display: none;"))
                    #check if the password is pwned
                    if browser.find_element(By.XPATH, '//div[@aria-expanded="true"]').get_attribute("id") == "noPwnage":
                        write.writerow([pwd, "False", "0"])
                    elif browser.find_element(By.XPATH, '//div[@aria-expanded="true"]').get_attribute("id") == "invalidAccount":
                        write.writerow([pwd])
                    else:
                        num = int(browser.find_element(By.ID, 'pwnedPasswordResult').text.split(" ")[5].replace(",", ""))
                        write.writerow([pwd, "True", num])
                    #clear the password
                    Password.clear()

browser=browser_init()
check_pwned_passwords(browser)

browser.close() #close the browser