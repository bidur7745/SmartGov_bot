import asyncio
from playwright.async_api import async_playwright
import os

async def test_fill():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://applydlnew.dotm.gov.np/login/", timeout=2000000)

        await page.wait_for_selector('#mobile', timeout=10000)
        await page.fill('#mobile', '9702935684')
        print("Filled mobile number.")

        captcha_input = input("Please enter the CAPTCHA shown on screen: ")
        await page.fill('input[name="captcha"]', captcha_input)
        print("Filled CAPTCHA.")

        # Wait a bit for any validations or events
        await page.wait_for_timeout(1000)

        # Click the submit button to go to next page 2
        await page.click('button[type="submit"]')
        print("Clicked on submit button.")

        # page 2 thing
        Mpin_input = input("Please enter the Mpin shown on screen: ")
        await page.fill('input[name="mpin"]', Mpin_input)
        print("Successfully added mpin")
        await page.wait_for_selector('#mpin', timeout=10000)

        # Option 1: Submit by pressing Enter
        await page.locator('#mpin').press('Enter')
        print("Page 2 loaded.")

        # page 3 things
        await page.click('button[type="submit"]')
        print("Clicked on next button of page 3")

        # page 4 thing select your citizenship country
        await page.click('button[type="submit"]')

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

        # page 5 thing filling the actual form
        await page.wait_for_selector('#firstname', timeout=30000000)
        await page.fill('#firstname', user_data['firstname'])
        await page.fill('#middlename', user_data['middlename'])
        await page.fill('#lastname', user_data['lastname'])

        # Set date of birth (DOB) for 2058-08-10 (Mangsir 10, 2058)
        await page.click('#dob')
        await page.wait_for_timeout(1000)  # Wait for calendar to open
        await page.locator('select#year').select_option("2058")  # Select year
        await page.locator('select#month').select_option("8")  # Select Mangsir
        await page.wait_for_timeout(300)  # Wait for calendar grid to update
        await page.click('td[data-value="2058-08-10"]')  # Click day 10
        print("Selected DOB: 2058-08-10")

        # Citizenship number
        await page.fill('#citizenshipno', user_data['citizenshipno'])

        # Use select_option instead of fill for <select>
        await page.wait_for_selector('#issuedistrict', timeout=15000, state='visible')
        await page.select_option('#issuedistrict', label='Morang')

        # issuedate calendar widget
        await page.click('#issuedate1')
        await page.wait_for_selector('select#year', timeout=5000)  # Wait for year dropdown
        await page.locator('select#year').select_option("2075")  # Select year 2075
        await page.locator('select#month').select_option("6")  # Select Ashwin (value="6")
        await page.wait_for_timeout(300)  # Wait for calendar grid to update
        await page.click('td[data-value="2075-06-12"]')  # Click day 12
        print("Selected Issue Date: 2075-06-12")

        # email container
        await page.fill('#email', user_data['email'])

        # Submit button
        await page.click('button[type="submit"]')
        print("Clicked on Next button to go to the next page")

        # page 6 things
        user_data2 = {
            "firstname_ll": "आशिष ",
            "middlename_ll": " ",
            "lastname_ll": "लिम्बु",
            "occupation": "Student",
            "education": "Undergraduate",
            "identitymark": "normal",
            "wardnumber": "9",
            "tolename": "Ratwamani",
            "citizenship_front_image": os.path.abspath("./front_img.jpg"),
            "citizenship_back_image": os.path.abspath("./back_img.jpg"),
        }

        # Applicant Details
        await page.wait_for_selector('#firstname_ll', timeout=30000000)
        await page.fill('#firstname_ll', user_data2['firstname_ll'])
        await page.fill('#middlename_ll', user_data2['middlename_ll'])
        await page.fill('#lastname_ll', user_data2['lastname_ll'])

        # Gender
        await page.wait_for_selector('#gender_id', timeout=15000, state='visible')
        await page.select_option('#gender_id', label='Male')

        # blood group
        await page.wait_for_selector('#bloodgroup_id', timeout=15000, state='visible')
        await page.select_option('#bloodgroup_id', label='B+')

        # Identity Mark
        await page.fill('#identitymark', user_data2['identitymark'])

        # Profession
        occupation_exists = await page.locator('select[name="occupation"]').count()
        print(f"Occupation select elements found: {occupation_exists}")
        if occupation_exists:
            occupation_html = await page.locator('select[name="occupation"]').evaluate('el => el.outerHTML')
            print(f"Occupation HTML: {occupation_html[:200]}...")
            occupation_parent = await page.locator('select[name="occupation"]').evaluate('el => el.parentElement.outerHTML')
            print(f"Occupation parent HTML: {occupation_parent[:200]}...")

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
        await page.wait_for_selector('#education', timeout=15000, state='visible')
        await page.select_option('#education', label=user_data2['education'])

        # Guardian
        # Relationship
        await page.wait_for_selector('#witness_relationship', timeout=15000, state='visible')
        await page.select_option('#witness_relationship', label='Father')

        # Father name
        await page.wait_for_selector('#witness_firstname', timeout=10000)
        await page.fill('#witness_firstname', 'Jeet')
        print("Filled mobile number.")

        # father middle name
        await page.wait_for_selector('#witness_middlename', timeout=10000)
        await page.fill('#witness_middlename', 'Bahadur')
        print("Filled father middle name.")

        # father last name
        await page.wait_for_selector('#witness_lastname', timeout=10000)
        await page.fill('#witness_lastname', 'Limbu')
        print("Filled father last name.")

        # province selection
        print("Attempting to select province...")
        province_exists = await page.locator('#perm_zone').count()
        print(f"Province select elements found: {province_exists}")
        if province_exists:
            province_html = await page.locator('#perm_zone').evaluate('el => el.outerHTML')
            print(f"Province HTML: {province_html[:200]}...")
            province_parent = await page.locator('#perm_zone').evaluate('el => el.parentElement.outerHTML')
            print(f"Province parent HTML: {province_parent[:200]}...")
            try:
                await page.wait_for_selector('#perm_zone', timeout=15000, state='visible')
                province_options = await page.locator('#perm_zone option').all_inner_texts()
                print(f"Available provinces: {province_options}")
                province_disabled = await page.locator('#perm_zone').evaluate('el => el.disabled')
                print(f"Is province dropdown disabled? {province_disabled}")
                if await page.locator('#perm_zone').is_visible():
                    try:
                        await page.select_option('#perm_zone', value="10001")  # Use value for Koshi Province
                        print("Selected province: Koshi Province")
                    except Exception as e:
                        print(f"Failed to select province with select_option: {str(e)}")
                        print("Trying fallback methods...")
                        # Fallback 1: Click dropdown and select option
                        try:
                            await page.click('#perm_zone')
                            await page.locator('#perm_zone option[value="10001"]').click()
                            print("Selected province: Koshi Province (fallback 1)")
                        except:
                            print("Fallback 1 failed.")
                        # Fallback 2: JavaScript evaluation
                        try:
                            await page.evaluate('document.querySelector("#perm_zone").value = "10001"')
                            await page.evaluate('document.querySelector("#perm_zone").dispatchEvent(new Event("change"))')
                            print("Selected province: Koshi Province (fallback 2 - JavaScript)")
                        except:
                            print("Fallback 2 failed.")
                        # Fallback 3: Keyboard input
                        try:
                            await page.locator('#perm_zone').click()
                            await page.keyboard.type('Koshi Province')
                            await page.keyboard.press('Enter')
                            print("Selected province: Koshi Province (fallback 3 - keyboard)")
                        except:
                            print("All fallback methods failed for province.")
                else:
                    print("Province dropdown is not visible.")
            except Exception as e:
                print(f"Failed to find province selector: {str(e)}")
                await page.screenshot(path="province_error_screenshot.png")
                print("Screenshot saved as province_error_screenshot.png")

        # district selection
        print("Attempting to select district...")
        district_exists = await page.locator('#perm_district').count()
        print(f"District select elements found: {district_exists}")
        if district_exists:
            district_html = await page.locator('#perm_district').evaluate('el => el.outerHTML')
            print(f"District HTML: {district_html[:200]}...")
            district_parent = await page.locator('#perm_district').evaluate('el => el.parentElement.outerHTML')
            print(f"District parent HTML: {district_parent[:200]}...")
            try:
                await page.wait_for_selector('#perm_district', timeout=15000, state='visible')
                district_options = await page.locator('#perm_district option').all_inner_texts()
                print(f"Available districts: {district_options}")
                district_disabled = await page.locator('#perm_district').evaluate('el => el.disabled')
                print(f"Is district dropdown disabled? {district_disabled}")
                if await page.locator('#perm_district').is_visible():
                    try:
                        await page.select_option('#perm_district', value="10009")  # Morang
                        print("Selected district: Morang")
                    except Exception as e:
                        print(f"Failed to select district with select_option: {str(e)}")
                        print("Trying fallback methods...")
                        # Fallback 1: Click dropdown and select option
                        try:
                            await page.click('#perm_district')
                            await page.locator('#perm_district option[value="10009"]').click()
                            print("Selected district: Morang (fallback 1)")
                        except:
                            print("Fallback 1 failed.")
                        # Fallback 2: JavaScript evaluation
                        try:
                            await page.evaluate('document.querySelector("#perm_district").value = "10009"')
                            await page.evaluate('document.querySelector("#perm_district").dispatchEvent(new Event("change"))')
                            print("Selected district: Morang (fallback 2 - JavaScript)")
                        except:
                            print("Fallback 2 failed.")
                        # Fallback 3: Keyboard input
                        try:
                            await page.locator('#perm_district').click()
                            await page.keyboard.type('Morang')
                            await page.keyboard.press('Enter')
                            print("Selected district: Morang (fallback 3 - keyboard)")
                        except:
                            print("All fallback methods failed for district.")
                else:
                    print("District dropdown is not visible.")
            except Exception as e:
                print(f"Failed to find district selector: {str(e)}")
                await page.screenshot(path="district_error_screenshot.png")
                print("Screenshot saved as district_error_screenshot.png")

        # Rular urban municipality
        print("Attempting to select municipality...")
        district_exists = await page.locator('#perm_villagemetrocity').count()
        if district_exists:
            district_html = await page.locator('#perm_villagemetrocity').evaluate('el => el.outerHTML')
            print(f"Municipality HTML: {district_html[:200]}...")
            district_parent = await page.locator('#perm_villagemetrocity').evaluate('el => el.parentElement.outerHTML')
            print(f"Municipality parent HTML: {district_parent[:200]}...")
            try:
                await page.wait_for_selector('#perm_villagemetrocity', timeout=15000, state='visible')
                district_options = await page.locator('#perm_villagemetrocity option').all_inner_texts()
                print(f"Available municipalities: {district_options}")
                district_disabled = await page.locator('#perm_villagemetrocity').evaluate('el => el.disabled')
                print(f"Is municipality dropdown disabled? {district_disabled}")
                if await page.locator('#perm_district').is_visible():
                    try:
                        await page.select_option('#perm_villagemetrocity', value="10087")  # Morang
                        print("Selected municipality: Morang")
                    except Exception as e:
                        print(f"Failed to select municipality with select_option: {str(e)}")
                        print("Trying fallback methods...")
                        # Fallback 1: Click dropdown and select option
                        try:
                            await page.click('#perm_villagemetrocity')
                            await page.locator('#perm_villagemetrocity option[value="10087"]').click()
                            print("Selected municipality: Ratwamai (fallback 1)")
                        except:
                            print("Fallback 1 failed.")
                        # Fallback 2: JavaScript evaluation
                        try:
                            await page.evaluate('document.querySelector("#perm_villagemetrocity").value = "10009"')
                            await page.evaluate('document.querySelector("#perm_villagemetrocity").dispatchEvent(new Event("change"))')
                            print("Selected municipality: Ratwamai (fallback 2 - JavaScript)")
                        except:
                            print("Fallback 2 failed.")
                        # Fallback 3: Keyboard input
                        try:
                            await page.locator('#perm_villagemetrocity').click()
                            await page.keyboard.type('Ratwamai')
                            await page.keyboard.press('Enter')
                            print("Selected municipality: Morang (fallback 3 - keyboard)")
                        except:
                            print("All fallback methods failed for municipality.")
                else:
                    print("Municipality dropdown is not visible.")
            except Exception as e:
                print(f"Failed to find municipality selector: {str(e)}")
                await page.screenshot(path="municipality_error_screenshot.png")
                print("Screenshot saved as municipality_error_screenshot.png")

        # Ward Number
        print("Attempting to fill ward number...")
        wardnumber_exists = await page.locator('#perm_wardnumber').count()
        print(f"Ward number input elements found: {wardnumber_exists}")
        if wardnumber_exists:
            wardnumber_html = await page.locator('#perm_wardnumber').evaluate('el => el.outerHTML')
            print(f"Ward number HTML: {wardnumber_html[:200]}...")
            wardnumber_parent = await page.locator('#perm_wardnumber').evaluate('el => el.parentElement.outerHTML')
            print(f"Ward number parent HTML: {wardnumber_parent[:200]}...")
            try:
                await page.wait_for_selector('#perm_wardnumber', timeout=15000, state='visible')
                wardnumber_disabled = await page.locator('#perm_wardnumber').evaluate('el => el.disabled')
                print(f"Is ward number input disabled? {wardnumber_disabled}")
                if await page.locator('#perm_wardnumber').is_visible():
                    try:
                        await page.fill('#perm_wardnumber', user_data2['wardnumber'])
                        print(f"Filled ward number: {user_data2['wardnumber']}")
                    except Exception as e:
                        print(f"Failed to fill ward number with fill: {str(e)}")
                        print("Trying fallback method...")
                        # Fallback: JavaScript evaluation
                        try:
                            await page.evaluate(f'document.querySelector("#perm_wardnumber").value = "{user_data2["wardnumber"]}"')
                            await page.evaluate('document.querySelector("#perm_wardnumber").dispatchEvent(new Event("input"))')
                            print(f"Filled ward number: {user_data2['wardnumber']} (fallback - JavaScript)")
                        except:
                            print("Fallback failed.")
                else:
                    print("Ward number input is not visible.")
            except Exception as e:
                print(f"Failed to find ward number selector: {str(e)}")
                await page.screenshot(path="wardnumber_error_screenshot.png")
                print("Screenshot saved as wardnumber_error_screenshot.png")

        # Tole name
        await page.wait_for_selector('#perm_tole', timeout=30000000)
        await page.fill('#perm_tole', user_data2['tolename'])

        # Same as Permanent Checkbox
        print("Attempting to tick same as permanent checkbox...")
        checkbox_exists = await page.locator('#sameaspermanent').count()
        print(f"Same as permanent checkbox elements found: {checkbox_exists}")
        if checkbox_exists:
            checkbox_html = await page.locator('#sameaspermanent').evaluate('el => el.outerHTML')
            print(f"Checkbox HTML: {checkbox_html[:200]}...")
            checkbox_parent = await page.locator('#sameaspermanent').evaluate('el => el.parentElement.outerHTML')
            print(f"Checkbox parent HTML: {checkbox_parent[:200]}...")
            try:
                await page.wait_for_selector('#sameaspermanent', timeout=15000, state='visible')
                checkbox_disabled = await page.locator('#sameaspermanent').evaluate('el => el.disabled')
                checkbox_checked = await page.locator('#sameaspermanent').evaluate('el => el.checked')
                print(f"Is checkbox disabled? {checkbox_disabled}")
                print(f"Is checkbox already checked? {checkbox_checked}")
                if await page.locator('#sameaspermanent').is_visible() and not checkbox_checked:
                    try:
                        await page.check('#sameaspermanent')
                        print("Ticked same as permanent checkbox")
                    except Exception as e:
                        print(f"Failed to tick checkbox with check: {str(e)}")
                        print("Trying fallback method...")
                        # Fallback: JavaScript evaluation
                        try:
                            await page.evaluate('document.querySelector("#sameaspermanent").checked = true')
                            await page.evaluate('document.querySelector("#sameaspermanent").dispatchEvent(new Event("change"))')
                            print("Ticked same as permanent checkbox (fallback - JavaScript)")
                        except:
                            print("Fallback failed.")
                elif checkbox_checked:
                    print("Checkbox is already ticked; no action needed.")
                else:
                    print("Checkbox is not visible.")
            except Exception as e:
                print(f"Failed to find checkbox selector: {str(e)}")
                await page.screenshot(path="sameaspermanent_error_screenshot.png")
                print("Screenshot saved as sameaspermanent_error_screenshot.png")

        # front side photo
        print("Attempting to upload citizenship front image...")
        upload_exists = await page.locator('#upload1').count()
        print(f"Upload input elements found: {upload_exists}")
        if upload_exists:
            upload_html = await page.locator('#upload1').evaluate('el => el.outerHTML')
            print(f"Upload HTML: {upload_html[:200]}...")
            upload_parent = await page.locator('#upload1').evaluate('el => el.parentElement.outerHTML')
            print(f"Upload parent HTML: {upload_parent[:200]}...")
            try:
                await page.wait_for_selector('#upload1', timeout=15000, state='visible')
                upload_disabled = await page.locator('#upload1').evaluate('el => el.disabled')
                print(f"Is upload input disabled? {upload_disabled}")
                if await page.locator('#upload1').is_visible():
                    # Verify file exists
                    if os.path.exists(user_data2['citizenship_front_image']):
                        try:
                            await page.set_input_files('#upload1', user_data2['citizenship_front_image'])
                            print(f"Uploaded citizenship front image: {user_data2['citizenship_front_image']}")
                            # Trigger change event to ensure readURL1() runs
                            await page.evaluate('document.querySelector("#upload1").dispatchEvent(new Event("change"))')
                        except Exception as e:
                            print(f"Failed to upload file with set_input_files: {str(e)}")
                            print("Trying fallback method...")
                            # Fallback: JavaScript to set files (less reliable, but attempts to trigger event)
                            try:
                                await page.evaluate(f'''
                                    const input = document.querySelector("#upload1");
                                    const file = new File([""], "{os.path.basename(user_data2['citizenship_front_image'])}", {{type: "image/jpeg"}});
                                    const dataTransfer = new DataTransfer();
                                    dataTransfer.items.add(file);
                                    input.files = dataTransfer.files;
                                    input.dispatchEvent(new Event("change"));
                                ''')
                                print(f"Uploaded citizenship front image: {user_data2['front_img']} (fallback - JavaScript)")
                            except:
                                print("Fallback failed.")
                    else:
                        print(f"File not found: {user_data2['front_img']}")
                else:
                    print("Upload input is not visible.")
            except Exception as e:
                print(f"Failed to find upload selector: {str(e)}")
                await page.screenshot(path="upload1_error_screenshot.png")
                print("Screenshot saved as upload1_error_screenshot.png")

        # Citizenship back Image Upload
        print("Attempting to upload citizenship back image...")
        upload_exists = await page.locator('#upload2').count()
        print(f"Upload input elements found: {upload_exists}")
        if upload_exists:
            upload_html = await page.locator('#upload2').evaluate('el => el.outerHTML')
            print(f"Upload HTML: {upload_html[:200]}...")
            upload_parent = await page.locator('#upload2').evaluate('el => el.parentElement.outerHTML')
            print(f"Upload parent HTML: {upload_parent[:200]}...")
            try:
                await page.wait_for_selector('#upload2', timeout=15000, state='visible')
                upload_disabled = await page.locator('#upload2').evaluate('el => el.disabled')
                print(f"Is upload input disabled? {upload_disabled}")
                if await page.locator('#upload2').is_visible():
                    # Verify file exists
                    if os.path.exists(user_data2['citizenship_back_image']):
                        try:
                            await page.set_input_files('#upload2', user_data2['citizenship_back_image'])
                            print(f"Uploaded citizenship back image: {user_data2['citizenship_back_image']}")
                            # Trigger change event to ensure readURL1() runs
                            await page.evaluate('document.querySelector("#upload2").dispatchEvent(new Event("change"))')
                        except Exception as e:
                            print(f"Failed to upload file with set_input_files: {str(e)}")
                            print("Trying fallback method...")
                            # Fallback: JavaScript to set files (less reliable, but attempts to trigger event)
                            try:
                                await page.evaluate(f'''
                                    const input = document.querySelector("#upload2");
                                    const file = new File([""], "{os.path.basename(user_data2['back_img'])}", {{type: "image/jpeg"}});
                                    const dataTransfer = new DataTransfer();
                                    dataTransfer.items.add(file);
                                    input.files = dataTransfer.files;
                                    input.dispatchEvent(new Event("change"));
                                ''')
                                print(f"Uploaded citizenship back image: {user_data2['back_img']} (fallback - JavaScript)")
                            except:
                                print("Fallback failed.")
                    else:
                        print(f"File not found: {user_data2['back_img']}")
                else:
                    print("Upload input is not visible.")
            except Exception as e:
                print(f"Failed to find upload selector: {str(e)}")
                await page.screenshot(path="upload2_error_screenshot.png")
                print("Screenshot saved as upload2_error_screenshot.png")

        # next button trigger point
        await page.click('button[type="submit"]')
        print("Clicked on Next button to go to the next page")

        # Wait to observe results
        await page.wait_for_timeout(1000000)

        await browser.close()

# Run the async function
# asyncio.run(test_fill())