#!/usr/bin/env python

from selenium import webdriver
from sys import argv

SELECTIONS = 5

BARCODE = ""
PIN = ""
with open('/Users/johnmussman/dev/librarycard/credentials.txt', 'r') as fp:
	BARCODE, PIN = [l.strip() for l in fp.readlines()]

query = 'first robot'
if len(argv) > 1:
	query = ' '.join(argv[1:])
else:
	print 'Usage: python librarycard.py <search query>'
	print "Defaulting to '" + query + "'."

search_url_start = "https://browse.nypl.org/iii/encore/search/C__S"
search_url_end = "__Ff%3Afacetcollections%3A96%3A96%3ACirculating%3A%3A__Ff%3Afacetmediatype%3Aa%3Aa%3ABOOKLw%3D%3DTEXT%3A%3A__Orightresult__U__X0?lang=eng&suite=def"
url = search_url_start + query + search_url_end

browser = webdriver.PhantomJS()

try:
	print ''
	browser.get(url)
	
	results = [browser.find_element_by_xpath(".//*[@id='recordDisplayLink2Component']").text]
	next_results_xpath = ".//*[@id='recordDisplayLink2Component_0']"
	for i in range(SELECTIONS - 1):
		try:
			next_results_xpath = next_results_xpath[:38] + str(i) + next_results_xpath[-2:]
			results.append(browser.find_element_by_xpath(next_results_xpath).text)
		except:
			pass

	print 'Found ' + str(len(results)) + ' results:'
	for index, result in enumerate(results):
		print index + 1, ' ', result
	print ''

	entry = raw_input("Choose a book number to put on hold, or not: ")
	print ''

	try:
		e_num = int(entry.strip())
		if e_num <= SELECTIONS and e_num > 0:
			if e_num == 1:
				browser.find_element_by_xpath(".//*[@id='genericLink']").click()
			else:
				browser.find_element_by_xpath(".//*[@id='genericLink_" + str(e_num - 1) + "']").click()
		
			barcode = browser.find_element_by_xpath(".//*[@id='code']")
			barcode.click()
			barcode.send_keys(BARCODE)

			pin = browser.find_element_by_xpath(".//*[@id='pin']")
			pin.click()
			pin.send_keys(PIN)

			browser.find_element_by_xpath(".//*[@id='fm1']/div[3]/input").click()
			browser.find_element_by_xpath(".//*[@id='itemRequestSubmitComponent']").click()

			print "Successfully put book on hold: ", results[e_num - 1]
		else:
			print 'Number not between 1 and 5. Did not put book on hold. Goodbye.'
	except:
		print 'Did not put book on hold. Goodbye.'
		pass

except:
	print "Nothing found for '" + query + "'."

print ''
print ''

browser.quit()