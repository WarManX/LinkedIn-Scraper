from libraries import *

import requests
import re
from dotenv import load_dotenv

from selenium import webdriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def signal_handler(signal, frame):
    logo()
    print(O + "[" + C + "*" + O + "] " +
          C + "Thank you" + W)
    exit()


signal.signal(signal.SIGINT, signal_handler)


class LinkedIn_Menu():
    def __init__(self):
        logo()

        print(O + "[" + C + "*" + O + "] " +
              C + "Select Option" + W)
        print("")
        print(O + "[" + C + "1" + O + "] " +
              C + "Job Search" + W)
        print(O + "[" + C + "2" + O + "] " +
              C + "Profile Details" + W)
        print("")
        option = input(O + "[" + C + "*" + O + "] " + W)

        if option == "1":
            Search_Job()
        elif option == "2":
            Profile_Search()
        else:
            print("")
            print(R + "Wrong Option" + W)
            sleep(1)
            LinkedIn_Menu()


class Profile_Search():
    def __init__(self):
        self.s = requests.Session()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97"
        }
        logo()
        print(O + "[" + C + "*" + O + "] " +
              C + "Login to LinkedIn" + W)
        load_dotenv()
        EMAIL = os.getenv('EMAIL')
        PASSWORD = os.getenv('PASSWORD')

        loadPrevSession = False

        if EMAIL != "" and PASSWORD != "":
            print(O + "[" + C + "*" + O + "] " +
                  C + "Previous Session Found! " + O + EMAIL + W)
            user_output = input(O + "[" + C + "*" + O + "] " + C +
                                "Would you like to load your previous session (Y/n): " + W)
            if user_output.lower() == "y":
                loadPrevSession = True
                email = EMAIL
                password = PASSWORD

        print("")
        if loadPrevSession == False:
            email = input(O + "[" + C + "*" + O + "] " + C +
                          "Enter your LinkedIn Email: " + W)
            password = input(O + "[" + C + "*" + O + "] " + C +
                             "Enter your LinkedIn Password: " + W)

        print("")
        print(O + "[" + C + "*" + O + "] " +
              C + "Checking Credentials..." + W)
        if self.login(email, password):
            self.search_menu()
        else:
            print(O + "[" + C + "*" + O + "] " + R +
                  "Login Failed, please recheck login credentials" + W)
            sleep(1.5)
            Profile_Search()

    def searchAgain(self):
        print("")
        user_input = input(O + "[" + C + "*" + O + "] " +
                           C + "Would you like to search again?(Y/n): " + W)
        if user_input == "Y" or user_input == "y":
            self.search_menu()
        else:
            LinkedIn_Menu()

    def login(self, email, password):
        try:
            sc = self.s.get("https://www.linkedin.com/login",
                            headers=self.headers).text
        except:
            return False
        csrfToken = sc.split('csrfToken" value="')[1].split('"')[0]
        sid = sc.split('sIdString" value="')[1].split('"')[0]
        pins = sc.split('pageInstance" value="')[1].split('"')[0]
        lcsrf = sc.split('loginCsrfParam" value="')[1].split('"')[0]
        data = {
            'csrfToken': csrfToken,
            'session_key': email,
            'ac': '2',
            'sIdString': sid,
            'parentPageKey': 'd_checkpoint_lg_consumerLogin',
            'pageInstance': pins,
            'trk': 'public_profile_nav-header-signin',
            'authUUID': '',
            'session_redirect': 'https://www.linkedin.com/feed/',
            'loginCsrfParam': lcsrf,
            'fp_data': 'default',
            '_d': 'd',
            'showGoogleOneTapLogin': 'true',
            'controlId': 'd_checkpoint_lg_consumerLogin-login_submit_button',
            'session_password': password,
            'loginFlow': 'REMEMBER_ME_OPTIN'
        }
        try:
            after_login = self.s.post(
                "https://www.linkedin.com/checkpoint/lg/login-submit", headers=self.headers, data=data).text
        except:
            return False
        is_logged_in = after_login.split('<title>')[1].split('</title>')[0]
        if is_logged_in == "LinkedIn":
            return True
        else:
            return False

    def companyScan(self):
        logo()
        target_company_link = input(O + "[" + C + "*" + O + "] " + C +
                                    "Enter Company URL: " + W)
        print("")
        company_id = self.getCompanyID(target_company_link)
        if company_id is not None:
            print(O + "[" + C + "*" + O + "] " + C +
                  "Collecting all company member profiles up to 10000!")
            print("")
            self.listProfiles(company_id, 1)
        print(O + "[" + C + "*" + O + "] " + C +
              "All Records have been saved to " + G + "leads.csv")
        sleep(2)
        self.searchAgain()

    def singleScan(self):
        logo()
        target_profile = input(O + "[" + C + "*" + O + "] " + C +
                                   "Enter Target Profile URL: " + W)
        print("")
        target_profile = target_profile + "/detail/contact-info/"
        sc = self.s.get(target_profile, headers=self.headers,
                        allow_redirects=True).text
        emails_found = re.findall('[a-zA-Z0-9\.\-\_i]+@[\w.]+', sc)
        print(emails_found)
        self.searchAgain()

    def saveRecord(self, data):
        with open('leads.csv', mode='a+', encoding='utf-8', newline='') as csvFile:
            fieldnames = ["Profile Link", "Full Name", "Headline", "Country"]
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            if os.stat('leads.csv').st_size == 0:
                writer.writeheader()
            writer.writerow(
                {"Profile Link": data[0], "Full Name": data[1], "Headline": data[2], "Country": data[3]})

    def listProfiles(self, company_id, page_no):
        resp = self.s.get('https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22{}%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH&page={}'.format(
            company_id, page_no), headers=self.headers).text
        token = self.s.cookies.get_dict().get('JSESSIONID').replace('"', '')
        headers = {
            'csrf-token': token,
            'referer': 'https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22{}%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH&page={}'.format(company_id, page_no),
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        resp = self.s.get('https://www.linkedin.com/voyager/api/search/blended?count=10&filters=List(currentCompany-%3E{},resultType-%3EPEOPLE)&origin=COMPANY_PAGE_CANNED_SEARCH&q=all&queryContext=List(spellCorrectionEnabled-%3Etrue)&start={}'.format(
            company_id, (int(page_no)-1) * 10), headers=headers).json()
        all_profile_links = []
        profiles = resp.get('elements')[0].get('elements')
        page_count = resp.get('paging').get('total')
        print(O + "[" + C + "*" + O + "] " + G +
              "Number of Employees: " + O + str(page_count))
        print("")
        counter = 1
        for profile in profiles:
            print(O + "[" + C + str(counter) + O + "]")
            counter = counter + 1
            try:
                person_name = profile.get('title').get('text')
                print(O + "[" + C + "*" + O + "] " + G +
                      "Full Name: " + O + "{}".format(person_name))
            except:
                person_name = "Unknown"
            try:
                profile_link = profile.get('navigationUrl')
                print(O + "[" + C + "*" + O + "] " + G +
                      "Profile Link: " + O + "{}".format(profile_link))
            except:
                profile_link = "Unknown"
            try:
                headline = profile.get('headline').get('text')
                print(O + "[" + C + "*" + O + "] " + G +
                      "Headline: " + O + "{}".format(headline))
            except:
                headline = "Unknown"
            try:
                country = profile.get('subline').get('text')
                print(O + "[" + C + "*" + O + "] " + G +
                      "Country: " + O + "{}".format(country))
            except:
                country = "Unknown"
            print("")
            data = []
            data.append(profile_link)
            data.append(person_name)
            data.append(headline)
            data.append(country)
            self.saveRecord(data)
        return all_profile_links

    def getCompanyID(self, company_link):
        try:
            company_username = company_link.split(
                '.com/company/')[1].replace('/', '')
        except:
            print(
                O + "[" + C + "*" + O + "] " + R + "Use company link like https://www.linkedin.com/company/unilever/ only!")
            sleep(2)
            return None
        resp = self.s.get(company_link, headers=self.headers).text
        token = self.s.cookies.get_dict().get('JSESSIONID').replace('"', '')
        headers = {
            'csrf-token': token,
            'referer': 'https://www.linkedin.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        api_link = 'https://www.linkedin.com/voyager/api/organization/companies?decorationId=com.linkedin.voyager.deco.organization.web.WebCompanyStockQuote-2&q=universalName&universalName={}'.format(
            quote(company_username))
        resp = self.s.get(api_link, headers=headers).json()
        company_id = resp.get('elements')[0].get('entityUrn').split(':')[-1]
        return company_id

    def search_menu(self):
        logo()
        print(O + "[" + C + "*" + O + "] " +
              C + "Select Option" + W)
        print("")
        print(O + "[" + C + "1" + O + "] " +
              C + "Profile Search" + W)
        print(O + "[" + C + "2" + O + "] " +
              C + "Company Search" + W)
        print(O + "[" + C + "0" + O + "] " +
              C + "Back" + W)
        print("")
        option = input(O + "[" + C + "*" + O + "] " + W)

        if option == "1":
            self.singleScan()
        elif option == "2":
            self.companyScan()
        elif option == "0":
            LinkedIn_Menu()
        else:
            print("")
            print(R + "Wrong Option" + W)
            sleep(1)
            self.search_menu()


class Search_Job():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = uc.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)
        self.url = 'https://www.linkedin.com/jobs/'
        self.driver.get(self.url)

        logo()

        user_major = input(O + "[" + C + "*" + O + "] " +
                           C + "Please Enter The Major: " + W)

        print("")
        print(O + "[" + C + "*" + O + "] " + C + "Starting")

        self.getTheMajor(user_major)
        self.searchAgain()

    def getTheMajor(self, major):
        print(O + "[" + C + "*" + O + "] " + C +
              "Searching for " + O + major + C + " Major in " + O + "LinkedIn")
        self.driver.find_element(
            by=By.XPATH, value='//*[@id="JOBS"]/section[1]/input').send_keys(major)
        sleep(2)
        self.driver.find_element(
            by=By.XPATH, value='/html/body/main/section[1]').click()
        sleep(1)
        self.driver.find_element(
            by=By.XPATH, value='/html/body/main/section[1]/div/section/div[2]/button[2]').click()
        sleep(2)
        print(O + "[" + C + "*" + O + "] " + C +
              "Loading data...")
        self.scrolldown()
        jobs_number = self.driver.find_element(
            by=By.XPATH, value='/html/body/div[1]/div/main/div/h1/span[1]').text
        jobs_location = self.driver.find_element(
            by=By.XPATH, value='/html/body/div[1]/div/main/div/h1/span[2]').text
        new_jobs = self.driver.find_element(
            by=By.XPATH, value='/html/body/div[1]/div/main/div/h1/span[3]').text
        print("")
        print(O + "[" + C + "*" + O + "] " + C +
              "Found " + G + jobs_number + " " + C + jobs_location)
        print(O + "[" + C + "*" + O + "] " + C +
              "New Jobs: " + G + new_jobs + W)
        print("")
        sleep(3.5)
        self.ShowingAllJobs()

    def ShowingAllJobs(self):
        print(O + "[" + C + "*" + O + "] " + C + "Showing All The Majors")
        print("")
        try:
            jobs_list = self.driver.find_element(
                by=By.XPATH, value='/html/body/div[1]/div/main/section[2]/ul')
            jobs = jobs_list.find_elements(by=By.TAG_NAME, value="li")

            i = 1
            for job in jobs:
                text = job.text
                job_link = job.find_element(
                    by=By.TAG_NAME, value='a').get_attribute("href")
                job_title = text.split("\n")[0]
                job_location = text.split("\n")[3]
                company_name = text.split("\n")[2]

                print()
                print(
                    G + "--<>--<>--<>--<>--<>--<>--<>--<>--<>--<>--<>--<>--<>--<>--<>--<>--")
                print("")
                print(O + "[" + C, i, O + "]" + W)
                print(O + "Company Name: " + C + company_name)
                print(O + "Job Name: " + C + job_title)
                print(O + "Company Location: " + C + job_location)
                print()
                print(O + "Job Link: " + C + job_link)
                print("")
                i = i + 1
                data = []
                data.append(company_name)
                data.append(job_title)
                data.append(job_location)
                data.append(job_link)
                self.saveRecord(data)
        except:
            print(O + "[" + C + "*" + O + "] " + R + "No Jobs Found" + W)
            sleep(1.5)
            self.searchAgain()

    def searchAgain(self):
        print("")
        user_input = input(O + "[" + C + "*" + O + "] " +
                           C + "Would you like to search again?(Y/n): " + W)
        if user_input == "Y" or user_input == "y":
            Search_Job()
        else:
            self.driver.close()
            LinkedIn_Menu()

    def saveRecord(self, data):
        with open('jobs.csv', mode='a+', encoding='utf-8', newline='') as csvFile:
            fieldnames = ["Company Name", "Job Name",
                          "Company Location", "Job Link"]
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            if os.stat('jobs.csv').st_size == 0:
                writer.writeheader()
            writer.writerow(
                {"Company Name": data[0], "Job Name": data[1], "Company Location": data[2], "Job Link": data[3]})

    def scrolldown(self):
        element = self.driver.find_element(
            by=By.XPATH, value='/html/body')
        for x in range(20):
            element.send_keys(Keys.PAGE_DOWN)
            sleep(0.5)


def logo():
    system("clear")
    print(O)
    print("   ___       _      ______ _           _           ")
    print("  |_  |     | |     |  ___(_)         | |          ")
    print("    | | ___ | |__   | |_   _ _ __   __| | ___ _ __ ")
    print("    | |/ _ \| '_ \  |  _| | | '_ \ / _` |/ _ \ '__|")
    print("/\__/ / (_) | |_) | | |   | | | | | (_| |  __/ |   ")
    print("\____/ \___/|_.__/  \_|   |_|_| |_|\__,_|\___|_|   ")
    print("")
    print("              Done By: " + C + "Marwan Aljasmi" + W)
    print("           https://github.com/ShyGorilla")
    print("")


if __name__ == '__main__':
    LinkedIn_Menu()
