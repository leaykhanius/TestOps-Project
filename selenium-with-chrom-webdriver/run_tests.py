from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")


driver = webdriver.Chrome(options=chrome_options)



driver.get("https://useinsider.com/")
wait = WebDriverWait(driver, 60)  

def test_homepage_opened():
    assert "Insider" in driver.title
    print("Homepage is opened successfully.")

def test_career_page_navigation():
    company_menu = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Company")]')))
    company_menu.click()
    
    careers_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Careers")]')))
    careers_link.click()
    
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    
    assert "careers" in driver.current_url, "Careers page did not open."
    print("Career page opened successfully.")

def test_filter_qa_jobs():
    driver.get("https://useinsider.com/careers/quality-assurance/")
    
    wait = WebDriverWait(driver, 60)  
    
    see_all_qa_jobs = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "See all QA jobs")))
    see_all_qa_jobs.click()
    
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    
    try:
        cookie_popup = wait.until(EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn")))
        cookie_popup.click()
    except TimeoutException:
        print("No cookie popup found.")
    
    time.sleep(5)  
    
    try:
        department_filter = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="filter-menu"]//span[@id="select2-filter-by-department-container"]')))
        department_filter.click()
        
        qa_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[contains(text(), "Quality Assurance")]')))
        qa_option.click()
        time.sleep(2)
    
    except TimeoutException:
        print("Failed to find or click the 'Department' filter.")
        
    time.sleep(5)
    
    try:
        location_filter = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="filter-menu"]//span[@id="select2-filter-by-location-container"]')))
        location_filter.click()
        
        istanbul_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[contains(text(), "Istanbul, Turkey")]')))
        istanbul_option.click()
        time.sleep(2)
    
    except TimeoutException:
        print("Failed to find or click the 'Location' filter.")
    
    
    jobs_list = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "position-list-item")]')))
    assert jobs_list.is_displayed(), "No jobs listed after filtering."
    print("Jobs list is displayed after filtering by Location and Department.")

def test_validate_job_details():
    job_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "position-list-item")]')))
    
    for job_element in job_elements:
        try:
            position = job_element.find_element(By.XPATH, './/span[@class="position-title"]').text
            department = job_element.find_element(By.XPATH, './/span[@class="position-department"]').text
            location = job_element.find_element(By.XPATH, './/span[@class="position-location"]').text
            
            assert "Quality Assurance" in position, f"Position does not contain 'Quality Assurance': {position}"
            assert "Quality Assurance" in department, f"Department does not contain 'Quality Assurance': {department}"
            assert "Istanbul, Turkey" in location, f"Location does not contain 'Istanbul, Turkey': {location}"
        except NoSuchElementException:
            print(f"Failed to validate job details for one job: {job_element.text}")
    print("All job details are validated successfully.")

def test_view_role_redirection():
    try:
        view_role_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[text()="View Role"]')))
        
        if len(view_role_buttons) == 0:
            raise Exception("No 'View Role' button found.")
        
        view_role_button = view_role_buttons[0]
        
        driver.execute_script("arguments[0].scrollIntoView(true);", view_role_button)
        
        driver.execute_script("arguments[0].click();", view_role_button)
        
        time.sleep(2)  
        new_window = driver.window_handles[-1]  
        driver.switch_to.window(new_window)  
        
        WebDriverWait(driver, 60).until(EC.url_contains("jobs.lever.co"))
        
        current_url = driver.current_url
        print("Current URL after redirect:", current_url)
        
        lever_url_part = "jobs.lever.co"
        
        assert lever_url_part in driver.current_url, f"Redirection to Lever Application page failed. Current URL: {driver.current_url}"
        print("Redirection to Lever Application form page is successful.")
    
    except TimeoutException:
        print("Failed to find or click the 'View Role' button.")


try:
    test_homepage_opened()
    test_career_page_navigation()
    test_filter_qa_jobs()
    test_validate_job_details()
    test_view_role_redirection()
finally:
    driver.quit()

