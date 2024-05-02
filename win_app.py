from flask import Flask, jsonify, request, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, TimeoutException
import openpyxl
import os
# from pyvirtualdisplay import Display

# display = Display(visible=0, size=(800, 600))
# display.start()

app = Flask(__name__)

# path of your chrome driver
driver_path ="/home/s-ubuntu/Music/flask/chromedriver.exe"


# Setting the path of the ChromeDriver executable
os.environ["webdriver.chrome.driver"] = driver_path

# Creating an instance of Options
options = Options()
options.binary_location = "/usr/bin/google-chrome"
options.add_experimental_option("detach", True)

# Initialize the Chrome driver with options
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 10)

@app.route("/memberdetails", methods=["GET"])
def scrape_members():
    try:
        all_member_info = []
        driver.get("https://admin.memberspace.com/sites/squarespace157/members?plan_status=free")
        if "sign_in" in driver.current_url:
            wait.until(EC.element_to_be_clickable((By.NAME, "email"))).send_keys("rgerber@angelbeat.com")
            wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys("UVA2027*hegron")
            overlay = wait.until(EC.invisibility_of_element_located((By.ID, "__memberspace_modal_protected_page")))
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//ms-button[text()='Log In']")))
            login_button.click()
        print("Reached the desired page after login")

        while True:
            try:
                all_member_info.extend(scrape_member_info())
                next_page_button = driver.find_elements(By.XPATH, "//span[@class='next']/a")
                if not next_page_button:
                    break
                go_to_next_page()
            except (NoSuchWindowException, NoSuchElementException) as e:
                print("An error occurred while scraping member info:", e)
                break
        
        excel_file = write_to_excel(all_member_info)
        print("Scraping and saving completed successfully.")
        return excel_file  # Return the file path
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def scrape_member_info():
    member_info = []
    try:
        member_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//span[@class='member-list-text']")))
        for member_element in member_elements:
            member_name = member_element.text.split('(')[0].strip()
            name_parts = member_name.split()
            first_name = name_parts[0]
            last_name = name_parts[-1] if len(name_parts) > 1 else ''
            text_node_script = "return arguments[0].nextSibling.textContent.trim();"
            
            phone_number_element = member_element.find_element(By.XPATH, ".//strong[contains(text(), 'Phone Number:')]")
            phone_number = driver.execute_script(text_node_script, phone_number_element)
            
            city_element = member_element.find_element(By.XPATH, ".//strong[contains(text(), 'City:')]")
            city = driver.execute_script(text_node_script, city_element)
            
            country_element = member_element.find_element(By.XPATH, ".//strong[contains(text(), 'Country or US State:')]")
            country = driver.execute_script(text_node_script, country_element)
            
            organization_element = member_element.find_element(By.XPATH, ".//strong[contains(text(), 'Organization:')]")
            organization = driver.execute_script(text_node_script, organization_element)
            
            job_title_element = member_element.find_element(By.XPATH, ".//strong[contains(text(), 'Job Title:')]")
            job_title = driver.execute_script(text_node_script, job_title_element)
            
            details_link = member_element.find_element(By.XPATH, ".//a[contains(@class, 'member-details-link')]")
            details_link.click()
            
            try:
                content_links_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//ms-button[text()='Content Links']")))
                content_links_button.click()
            except TimeoutException:
                print("The 'Content Links' button was not found or was not clickable within the specified time.")
                
            try:
                content_links_elements = WebDriverWait(driver, 2).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class, 'MemberSpaceWidgetInternal__MemberEventRow__3YZuZ__content')]")))
                content_links = [element.text.strip() for element in content_links_elements if element.text.strip() != '']
                content_dates_elements = driver.find_elements(By.XPATH, "//ms-typography[contains(@class, 'MemberSpaceWidgetInternal__MemberEventRow__3YZuZ__dateTime')]")
                content_dates = [element.text.strip() for element in content_dates_elements if element.text.strip() != '']
            except TimeoutException:
                content_links = ["Content link not found"]
                content_dates = ["Date not found "]
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                content_links = ["Error fetching content links"]
                content_dates = ["No date available"]
                
            content_details = list(zip(content_links, content_dates))
            driver.back()
            wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='member-list-text']")))
            member_info.append((first_name, last_name, phone_number, city, country, organization, job_title, content_details))
    except (NoSuchElementException, NoSuchWindowException) as e:
        print("An error occurred while scraping member info:", e)
    return member_info

def go_to_next_page():
    try:
        next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='next']/a")))
        next_page_button.click()
    except (NoSuchElementException, NoSuchWindowException) as e:
        print("An error occurred while navigating to the next page:", e)

def write_to_excel(member_info):
    excel_file = "member_info.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['First Name', 'Last Name', 'Phone Number', 'City', 'Country', 'Organization', 'Job Title', 'Content Details'])
    for info in member_info:
        first_name, last_name, phone_number, city, country, organization, job_title, content_details = info
        content_details_text = "\n".join([f"{link}: {date}" for link, date in content_details])
        ws.append([first_name, last_name, phone_number, city, country, organization, job_title, content_details_text])
    wb.save(excel_file)
    return excel_file  # Return the file path

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True) # You might need to set debug to False in production
    
    
# display.stop()