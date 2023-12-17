from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

test = list()
test_result= list()
ran = 0

d = webdriver.Chrome()
d.maximize_window()
d.get("http://127.0.0.1:5000")
d.save_screenshot(f"Test/TestSS/homepage.png")

d.find_element(By.LINK_TEXT, "R E N T").click()
time.sleep(1)

try:
    ran+=1
    test.append("test_email_validation_owner_login")
    #email validation for owner login
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("aakashmahindreker")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()
    time.sleep(3)
    expected_title = "Waterside Login"
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.refresh()
    ran+=1
    test.append("test_non-registered_owner_login")
    #unregistered user login for owner
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("axm7304")
    d.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()
    time.sleep(3)
    expected_title = "Waterside Register"
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.refresh()
    ran+=1
    test.append("test_register_unmatched_passwords_owner")
    #register for owner
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your first name']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your last name']").send_keys("Mahindreker")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Confirm your password']").send_keys("Aaakkash")
    d.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()
    time.sleep(3)
    expected_title = "Waterside Register"
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.refresh()
    ran+=1
    test.append("test_register_matched_passwords_owner")
    #register for owner
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your first name']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your last name']").send_keys("Mahindreker")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Confirm your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()
    time.sleep(3)
    expected_title = "Waterside Login"
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.refresh()
    ran+=1
    test.append("test_registered_owner_login")
    #registered user login for owner
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()
    time.sleep(3)
    expected_title = "Aakash's Dashboard"
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.refresh()
    ran+=1
    test.append("test_owner_add_boat")
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, 'a[href="/owner/boats/create"]').click()
    time.sleep(2)
    expected_title = 'Add Boat Details'
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.back()
    time.sleep(2)
    ran+=1
    test.append("test_owner_edit_details")
    d.find_element(By.CSS_SELECTOR, 'button[class="dropbtn"]').click()
    time.sleep(1)
    d.find_element(By.LINK_TEXT, 'Account Details').click()
    time.sleep(2)
    expected_title = 'Edit Account Details'
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.back()
    ran+=1
    test.append("test_owner_logout")
    d.find_element(By.CSS_SELECTOR, 'button[class="dropbtn"]').click()
    time.sleep(1)
    d.find_element(By.LINK_TEXT, 'Logout').click()
    time.sleep(2)
    expected_title = 'Waterside: Boat Rental Service'
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.find_element(By.LINK_TEXT, "R E N T").click()
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)
    d.refresh()
    ran+=1
    test.append("test_owner_account_delete")
    d.find_element(By.CSS_SELECTOR, 'button[class="dropbtn"]').click()
    time.sleep(1)
    d.find_element(By.LINK_TEXT, 'Delete Account').click()
    time.sleep(2)
    d.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[name='email1']").send_keys("axm7304@mavs.uta.edu")
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(2)
    expected_title = 'Waterside: Boat Rental Service'
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")


d.get("http://127.0.0.1:5000")
time.sleep(1)
d.find_element(By.LINK_TEXT, "H I R E").click()
time.sleep(1)

try:
    ran+=1
    test.append("test_email_validation_customer_login")
    #email validation for customer login
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("aakashmahindreker")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()
    time.sleep(3)
    expected_title = "Waterside Login"
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.refresh()
    ran+=1
    test.append("test_non-registered_customer_login")
    #unregistered user login for customer
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()
    time.sleep(3)
    expected_title = "Waterside Register"
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    ran+=1
    test.append("test_register_unmatched_passwords_customer")
    #register for owner
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your first name']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your last name']").send_keys("Mahindreker")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Confirm your password']").send_keys("Aaakkash")
    d.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()
    time.sleep(3)
    expected_title = "Waterside Register"
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.refresh()
    ran+=1
    test.append("test_register_matched_passwords_customer")
    #register for owner
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your first name']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your last name']").send_keys("Mahindreker")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Confirm your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()
    time.sleep(3)
    expected_title = "Waterside Login"
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.refresh()
    ran+=1
    test.append("test_registered_customer_login")
    #unregistered user login for customer
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()
    time.sleep(3)
    expected_title = "Aakash's Dashboard"
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
except:
    test_result.append("Failed")

try:
    d.refresh()
    ran+=1
    test.append("test_customer_book_boat_non-available")
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, 'a[href="/customer/boats/payment/6564262fe021ec61981af15c"]').click()
    time.sleep(2)
    expected_title = "Aakash's Dashboard"
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.refresh()
    ran+=1
    test.append("test_customer_book_boat_available")
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, 'a[href="/customer/boats/payment/65642698e021ec61981af15d"]').click()
    expected_title = "Payment"
    actual_title = d.title
    assert actual_title is not expected_title
    time.sleep(2)
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.back()
    ran+=1
    test.append("test_customer_logout")
    d.find_element(By.CSS_SELECTOR, 'button[class="dropbtn"]').click()
    time.sleep(1)
    d.find_element(By.LINK_TEXT, 'Logout').click()
    time.sleep(2)
    expected_title = 'Waterside: Boat Rental Service'
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

try:
    d.find_element(By.LINK_TEXT, "H I R E").click()
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[placeholder='Enter your password']").send_keys("Aakash")
    d.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)
    d.refresh()
    ran+=1
    test.append("test_customer_account_delete")
    d.find_element(By.CSS_SELECTOR, 'button[class="dropbtn"]').click()
    time.sleep(1)
    d.find_element(By.LINK_TEXT, 'Delete Account').click()
    time.sleep(2)
    d.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys("axm7304@mavs.uta.edu")
    d.find_element(By.CSS_SELECTOR, "input[name='email1']").send_keys("axm7304@mavs.uta.edu")
    time.sleep(1)
    d.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(2)
    expected_title = 'Waterside: Boat Rental Service'
    actual_title = d.title
    assert actual_title is not expected_title
    test_result.append("Passed")
    d.save_screenshot(f"Test/TestSS/{test[ran-1]}.png")
except:
    test_result.append("Failed")

print(f"{'Test Cases':<50}{'Test Results': <15}")
for i in range(len(test)):
    print(f"{test[i]:<50}{test_result[i]:<10}")

print(f"\nRan Tests: {ran}\nPassed: {test_result.count('Passed')}, Failed: {test_result.count('Failed')}")