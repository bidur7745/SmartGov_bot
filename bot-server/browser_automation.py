import asyncio
from playwright.async_api import async_playwright

async def test_fill():
    playwright = await async_playwright().start()  # Start Playwright manually
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()

    try:
        await page.goto("https://applydlnew.dotm.gov.np/login/", timeout=2000000)

        await page.wait_for_selector('#mobile', timeout=10000)
        await page.fill('#mobile', '9702935684')
        print("Filled mobile number.")

        captcha_input = input("Please enter the CAPTCHA shown on screen: ")
        await page.fill('input[name="captcha"]', captcha_input)
        print("Filled CAPTCHA.")

        await page.wait_for_timeout(1000)

        await page.click('button[type="submit"]')
        print("Clicked on submit button.")

        # Page 2: MPIN
        Mpin_input = input("Please enter the MPIN shown on screen: ")
        await page.fill('input[name="mpin"]', Mpin_input)
        print("Successfully added MPIN")
        await page.wait_for_selector('#mpin', timeout=10000)

        await page.locator('#mpin').press('Enter')
        print("Page 2 submitted.")

        # Page 3: Click next
        await page.click('button[type="submit"]')
        print("Clicked on next button of page 3")

        # Page 4: Select citizenship country
        await page.click('button[type="submit"]')
        print("Clicked on next button of page 4")

        # Page 5: Fill the actual form
        user_data = {
            "firstname": "Ashish",
            "middlename": "",
            "lastname": "Limbu",
            "dateofbirth": "2058-08-10",
            "citizenshipno": "05-06-76-01521",
            "issueddistrict": "Morang",
            "issuedate": "2075-06-12",
            "email": "aaseslimbu2@gmail.com"
        }

        await page.wait_for_selector('#firstname', timeout=30000)
        await page.fill('#firstname', user_data['firstname'])
        await page.fill('#middlename', user_data['middlename'])
        await page.fill('#lastname', user_data['lastname'])

        # Set date of birth (DOB) for 2058-08-10 (Mangsir 10, 2058)
        await page.click('#dob')
        await page.wait_for_timeout(1000)
        await page.locator('select#year').select_option("2058")
        await page.locator('select#month').select_option("8")
        await page.wait_for_timeout(300)
        await page.click('td[data-value="2058-08-10"]')
        print("Selected DOB: 2058-08-10")

        await page.fill('#citizenshipno', user_data['citizenshipno'])

        await page.wait_for_selector('#issuedistrict', timeout=15000, state='visible')
        await page.select_option('#issuedistrict', label='Morang')
        print("Selected issued district: Morang")

        # Set issuedate for 2075-06-12 (Ashwin 12, 2075)
        await page.click('#issuedate1')
        await page.wait_for_selector('select#year', timeout=5000)
        await page.locator('select#year').select_option("2075")
        await page.locator('select#month').select_option("6")
        await page.wait_for_timeout(300)
        await page.click('td[data-value="2075-06-12"]')
        print("Selected Issue Date: 2075-06-12")

        await page.fill('#email', user_data['email'])
        print("Filled email")

        # Click the "Next" button to go to page 6
        await page.click('button[type="submit"]')
        print("Clicked on Next button to go to page 6")

        # Page 6: Applicant Details
        user_data2 = {
            "firstname_ll": "आशिष ",
            "middlename_ll": " ",
            "lastname_ll": "लिम्बु",
            "occupation": "Student",
            "education": "Undergraduate",
            "identitymark": "normal"
        }

        await page.wait_for_selector('#firstname_ll', timeout=30000)
        await page.fill('#firstname_ll', user_data2['firstname_ll'])
        await page.fill('#middlename_ll', user_data2['middlename_ll'])
        await page.fill('#lastname_ll', user_data2['lastname_ll'])
        print("Filled local language name fields")

        # Gender
        await page.wait_for_selector('#gender_id', timeout=15000, state='visible')
        await page.select_option('#gender_id', label='Male')
        print("Selected gender: Male")

        # Blood group
        await page.wait_for_selector('#bloodgroup_id', timeout=15000, state='visible')
        await page.select_option('#bloodgroup_id', label='B+')
        print("Selected blood group: B+")

        # Identity Mark
        await page.fill('#identitymark', user_data2['identitymark'])
        print("Filled identity mark")

        # Debug: Check for occupation element
        occupation_exists = await page.locator('select[name="occupation"]').count()
        print(f"Occupation select elements found: {occupation_exists}")
        if occupation_exists:
            occupation_html = await page.locator('select[name="occupation"]').evaluate('el => el.outerHTML')
            print(f"Occupation HTML: {occupation_html[:200]}...")
            occupation_parent = await page.locator('select[name="occupation"]').evaluate('el => el.parentElement.outerHTML')
            print(f"Occupation parent HTML: {occupation_parent[:200]}...")

        # Profession
        print("Attempting to select occupation...")
        try:
            await page.wait_for_selector('select[name="occupation"]', timeout=60000, state='visible')
            occupation_options = await page.locator('select[name="occupation"] option').all_inner_texts()
            print(f"Available occupations: {occupation_options}")
            occupation_disabled = await page.locator('select[name="occupation"]').evaluate('el => el.disabled')
            print(f"Is occupation dropdown disabled? {occupation_disabled}")
            if await page.locator('select[name="occupation"]').is_visible():
                try:
                    await page.select_option('select[name="occupation"]', value=user_data2['occupation'])
                    print("Selected occupation: Student")
                except Exception as e:
                    print(f"Failed to select occupation with select_option: {str(e)}")
                    print("Trying fallback methods...")
                    # Fallback 1: Click dropdown and select option
                    try:
                        await page.click('select[name="occupation"]')
                        await page.locator(f'select[name="occupation"] option[value="{user_data2["occupation"]}"]').click()
                        print("Selected occupation: Student (fallback 1)")
                    except:
                        print("Fallback 1 failed.")
                        # Fallback 2: JavaScript evaluation
                        try:
                            await page.evaluate(f'document.querySelector("select[name=\\"occupation\\"]").value = "{user_data2["occupation"]}"')
                            await page.evaluate('document.querySelector("select[name=\\"occupation\\"]").dispatchEvent(new Event("change"))')
                            print("Selected occupation: Student (fallback 2 - JavaScript)")
                        except:
                            print("Fallback 2 failed.")
                            # Fallback 3: Keyboard input
                            try:
                                await page.locator('select[name="occupation"]').click()
                                await page.keyboard.type('Student')
                                await page.keyboard.press('Enter')
                                print("Selected occupation: Student (fallback 3 - keyboard)")
                            except:
                                print("All fallback methods failed for occupation.")
            else:
                print("Occupation dropdown is not visible.")
        except Exception as e:
            print(f"Failed to find occupation selector: {str(e)}")
            await page.screenshot(path="occupation_error_screenshot.png")
            print("Screenshot saved as occupation_error_screenshot.png")

        # Education
        print("Attempting to select education...")
        await page.wait_for_selector('#education', timeout=15000, state='visible')
        await page.select_option('#education', value=user_data2['education'])
        print("Selected education: Undergraduate")

        # Guardian
        # Relationship
        await page.wait_for_selector('#witness_relationship', timeout=15000, state='visible')
        await page.select_option('#witness_relationship', label='Father')
        print("Selected relationship: Father")

        # Father name
        await page.wait_for_selector('#witness_firstname', timeout=10000)
        await page.fill('#witness_firstname', 'Jeet')
        print("Filled father first name.")

        # Father middle name
        await page.wait_for_selector('#witness_middlename', timeout=10000)
        await page.fill('#witness_middlename', 'Bahadur')
        print("Filled father middle name.")

        # Father last name
        await page.wait_for_selector('#witness_lastname', timeout=10000)
        await page.fill('#witness_lastname', 'Limbu')
        print("Filled father last name.")

        # Keep browser open for inspection
        print("Script completed. Browser will stay open for 10 minutes or until you press Ctrl+C.")
        try:
            await page.wait_for_timeout(600000)  # Wait 10 minutes
        except KeyboardInterrupt:
            print("Script interrupted by user. Closing browser.")
            await browser.close()
            await playwright.stop()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await page.screenshot(path="error_screenshot.png")
        print("Error occurred. Browser will stay open for inspection. Press Ctrl+C to close.")
        try:
            await page.wait_for_timeout(600000)  # Wait 10 minutes
        except KeyboardInterrupt:
            print("Script interrupted by user. Closing browser.")
            await browser.close()
            await playwright.stop()

# if _name_ == "_main_":
#     asyncio.run(test_fill())