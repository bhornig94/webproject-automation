from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class test:
    def run (browser):
        # Initialize a counter for iterating through the links on a page
        count = 1
        fails= 0
        # Initialize a counter for iterating through the web pages
        Pcount = 0
        # List of local file paths (URLs) to be tested
        index_page = ["file:///C:/Users/brent/Desktop/webproject/webproject/index.htm",
                      "file:///C:/Users/brent/Desktop/webproject/webproject/ps4.htm",
                      "file:///C:/Users/brent/Desktop/webproject/webproject/xbox.htm"]
        # Initialize the Firefox WebDriver instance
        driver = browser
        wait= WebDriverWait(driver,10)
        print(" Tesing all links on all pages ")

        # --- Main Testing Loop (Page Iteration) ---
        # Outer loop runs for the 3 pages in the index_page list (Pcount = 0, 1, 2)
        while Pcount <= 2:
            # Load the current page URL from the list
            driver.get(index_page[Pcount])
            print(f"testing on page {index_page[Pcount]}")

            # --- Link Testing Loop ---
            # Inner loop iterates through the first three navigation links on the current page
            while count <= 3:

                try:
                    # Locate the navigation link element using a dynamic XPath.
                    # '//nav/ul/li[{count}]/a' targets the 1st, 2nd, and 3rd list items in the nav menu.
                    xpathL = f'//nav/ul/li[{count}]/a'
                    # Get the 'href' attribute value (the target URL) of the link

                    element = wait.until(EC.element_to_be_clickable((By.XPATH,xpathL)))
                    href_value = element.get_property('href')
                    # --- Same-Page Link Test ---
                    # Check if the link's target URL is the same as the current page URL
                    if href_value == index_page[Pcount]:
                        print(f"Executing same page link on page {index_page[Pcount]}")
                        if "#" in href_value:
                            print("  Note: Testing scroll behavior is recommended for anchor links.")

                        element.click()  # Click the same-page link

                        print("PASS: Same-page link clicked successfully (no navigation expected).")  # Log success without verification of scroll/hash change

                    # --- External Link Test ---
                    # If the link is pointing to a different page
                    else:

                        print(f"testing link {href_value} on page {index_page[Pcount]}")
                        print(href_value)

                        element.click()  # Click the link (navigates to a new page)
                        wait.until(EC.url_changes(index_page[Pcount]))

                        # 3. VERIFICATION: Wait for the main page title (e.g., "VIDEO GAME CONSOLE WARS")
                        # or a unique element on the new page to be present to confirm successful load.
                        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

                        print("   PASS: Successfully navigated to new page and confirmed load.")

                        # 4. Navigate back to the original test page
                        driver.back()
                        # 5. VERIFICATION: Wait for the browser to return to the original URL
                        wait.until(EC.url_to_be(index_page[Pcount]))
                        print(f"  Successfully returned to: {index_page[Pcount]}")


                          # Navigate back to the original test page

                except Exception as e:
                    # Catch any error during finding or interacting with the link
                    print(f"Error interacting with link #{count} on page {index_page[Pcount]}: {e}")
                    fails+=1

                # Increment the link counter to move to the next link
                count += 1

            # Increment the page counter to move to the next URL in the list
            Pcount += 1
            # Wait 2 seconds before loading the next page
            # Reset the link counter for the new page
            count = 1

        # Close the browser window and end the WebDriver session
        driver.quit()
        if fails==0:
            print("All tests passed")
        else:
            print(f"{fails} tests failed")
def Main():
    chrome=webdriver.Chrome()


    test.run(chrome)
    print("chrome start")
    firefox = webdriver.Firefox()
    print("firefox start")
    test.run(firefox)
    print("edge start")
    edge = webdriver.Edge()
    test.run(edge)
Main()