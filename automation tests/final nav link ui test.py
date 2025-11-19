from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

index_pages = ["file:///C:/Users/brent/Desktop/webproject/webproject/index.htm",
                      "file:///C:/Users/brent/Desktop/webproject/webproject/ps4.htm",
                      "file:///C:/Users/brent/Desktop/webproject/webproject/xbox.htm"]

class test:
    def run (browser,index_pages):
        # Initialize a counter for iterating through the links on a page
        fails=0
        # Initialize a counter for iterating through the web pages

        # List of local file paths (URLs) to be tested

        # Initialize the Firefox WebDriver instance
        driver = browser
        wait= WebDriverWait(driver,10)
        print(" Tesing all links on all pages ")

        # --- Main Testing Loop (Page Iteration) ---
        # Outer loop runs for the 3 pages in the index_page list (Pcount = 0, 1, 2)
        for index_page in index_pages:
            try:
                # Load the current page URL from the list
                driver.get(index_page)
                print(f"testing on page {index_page}")

                # --- Link Testing Loop ---
                # Inner loop iterates through the first three navigation links on the current page
                nav_links = driver.find_elements(By.XPATH, '//nav//a')
                for i in range(len(nav_links)):
                    xpathL = f'(//nav//a)[{i + 1}]'

                    try:
                        # Locate the navigation link element using a dynamic XPath.
                        # '//nav/ul/li[{count}]/a' targets the 1st, 2nd, and 3rd list items in the nav menu.

                        # Get the 'href' attribute value (the target URL) of the link

                        element = wait.until(EC.element_to_be_clickable((By.XPATH,xpathL)))
                        href_value = element.get_property('href')
                        # --- Same-Page Link Test ---
                        # Check if the link's target URL is the same as the current page URL
                        if href_value == index_page:
                            print(f"Executing same page link on page {index_page}")
                            if "#" in href_value:
                                print("  Note: Testing scroll behavior is recommended for anchor links.")

                            element.click()  # Click the same-page link

                            print(" \u2713 PASS: Same-page link clicked successfully (no navigation expected).")  # Log success without verification of scroll/hash change

                        # --- External Link Test ---
                        # If the link is pointing to a different page
                        else:

                            print(f"testing link {href_value} on page {index_page}")
                            print(href_value)

                            element.click()  # Click the link (navigates to a new page)
                            wait.until(EC.url_changes(index_page))

                            # 3. VERIFICATION: Wait for the main page title (e.g., "VIDEO GAME CONSOLE WARS")
                            # or a unique element on the new page to be present to confirm successful load.
                            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

                            print(" \u2713 PASS: Successfully navigated to new page and confirmed load.")

                            # 4. Navigate back to the original test page
                            driver.back()
                            # 5. VERIFICATION: Wait for the browser to return to the original URL
                            wait.until(EC.url_to_be(index_page))
                            print(f"Successfully returned to: {index_page}")


                              # Navigate back to the original test page
                    except TimeoutException as te:
                        print(
                            f"  \u2717 FAIL: Timeout for link  ({xpathL}) on page {index_page}. Error: {te}")
                        fails += 1
                    except NoSuchElementException as nsee:
                        print(
                            f"  \u2717 FAIL: Element missing for link {xpathL} on page {index_page}. Error: {nsee}")
                        fails += 1
                    except WebDriverException as wde:
                        print(f"  \u2717 FAIL: WebDriver error on link {xpathL}. Error: {wde}")
                        fails += 1


                    except Exception as e:
                        # Catch all other unexpected errors
                        print(
                            f"  \u2717 FAIL: An unexpected error occurred on link {xpathL} on page {index_page}. Error: {e}")
                        fails += 1


            except WebDriverException as e:
                print(f"\nFATAL ERROR: Could not load or interact with page {index_page}. Check if the path is correct and accessible.")
                print(f"Details: {e}")
                fails += 1



        if fails==0:
            print("All tests passed")
        else:
            print(f"{fails} tests failed")


def Main():
    try:
        chrome=webdriver.Chrome()
        test.run(chrome,index_pages)
    except WebDriverException as e:
        print(f"\nERROR: Failed to initialize chrome. Ensure the WebDriver is installed and in your system's PATH.")
        driver.quit()
    finally:
        if chrome:
            chrome.quit()
            print("Closed Edge.")

    print("chrome start")

    try:
        firefox = webdriver.Firefox()
        test.run(firefox,index_pages)
    except WebDriverException as e:
        print(f"\nERROR: Failed to initialize firefox. Ensure the WebDriver is installed and in your system's PATH.")
        firefox.quit()
    finally:
        if firefox:
            firefox.quit()
            print("Closed FireFox.")

    print("firefox start")

    try:
        edge = webdriver.Edge()
        test.run(edge,index_pages)
    except WebDriverException as e:
        print(f"\nERROR: Failed to initialize Edge. Ensure the WebDriver is installed and in your system's PATH.")
        edge.quit()
    finally:
        if edge:
            edge.quit()
            print("Closed edge.")

    print("edge start")


Main()