from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

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
		self.browser.get('http://localhost:8000')

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

		# He types "buy guitar strings" into a text box.
		input_text_box.send_keys("Buy Guitar Strings")

		# He hits enter. The page updates and now the page lists:
		# "1. Buy guitar strings" as an item on the todo list.
		input_text_box.send_keys(Keys.ENTER)

		self.check_for_row_in_list_table('1: Buy Guitar Strings')

		# The page shows a text box to enter another item.
		# He adds the item "change strings on the guitar"
		self.check_for_row_in_list_table('1: Buy Guitar Strings')
		self.check_for_row_in_list_table('2: change strings on the guitar')

		self.fail("Finish the test!")

		# The page updates again and shows both items in the todo list.

		# He wonders if the page will save his todo list when he closes the site.
		# Then he sees the text explaining that there is a unqiue URL that
		# he can use to access the todo list.

		# He visits the URL and sees the todo list is still there.

		# He is satisfied and closes the browser for now.

if __name__ == '__main__':
	unittest.main(warnings = 'ignore')
