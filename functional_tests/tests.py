from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Jonas has heard about a new todo list website.
		# He goes to check out the site.
		self.browser.get(self.live_server_url)

		# He notices the page title and header say todo list.
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# He is invited to start a new todo list.
		input_text_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
				input_text_box.get_attribute('placeholder'),
				'Enter a to-do item'
		)

		# He types "buy guitar strings" into a text box and hits enter.
		input_text_box.send_keys("Buy Guitar Strings")
		input_text_box.send_keys(Keys.ENTER)
		jonas_list_url = self.browser.current_url
		self.assertRegex(jonas_list_url, '/lists/.+')

		# The page updates and now the page lists:
		# "1. Buy guitar strings" as an item on the todo list.
		self.check_for_row_in_list_table('1: Buy Guitar Strings')

		# The page shows a text box to enter another item.
		# He adds the item "change strings on the guitar"
		input_text_box = self.browser.find_element_by_id('id_new_item')
		input_text_box.send_keys("change strings on the guitar")
		input_text_box.send_keys(Keys.ENTER)

		# The page updates again and shows both items in the todo list.
		self.check_for_row_in_list_table('1: Buy Guitar Strings')
		self.check_for_row_in_list_table('2: change strings on the guitar')

		# Now a new user, Francis, comes to the site.

		## use a new browser session to make sure that no info
		## from edith is present in cookies
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Francis visits the site and there is no sign of Jonas' list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy Guitar Strings', page_text)
		self.assertNotIn('change strings on the guitar', page_text)

		# Francis starts a new list by entering a new item.
		input_text_box = self.browser.find_element_by_id('id_new_item')
		input_text_box.send_keys('Buy Milk')
		input_text_box.send_keys(keys.ENTER)

		# Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, jonas_list_url)

		# again there is no trace of Jonas' list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy Guitar Strings', page_text)
		self.assertIn('Buy Milk', page_text)

		# satisfied, they both go back to sleep
