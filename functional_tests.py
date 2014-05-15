from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test(self):
		# Jonas has heard about a new todo list website.
		# He goes to check out the site.
		self.browser.get('http://localhost:8000')

		# He notices the page title and header say todo list.
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!')

		# He is invited to start a new todo list.

		# He types "buy guitar strings" into a text box.

		# He hits enter. The page updates and now the page lists:
		# "1. Buy guitar strings" as an item on the todo list.

		# The page shows a text box to enter another item.
		# He adds the item "change strings on the guitar"

		# The page updates again and shows both items in the todo list.

		# He wonders if the page will save his todo list when he closes the site.
		# Then he sees the text explaining that there is a unqiue URL that
		# he can use to access the todo list.

		# He visits the URL and sees the todo list is still there.

		# He is satisfied and closes the browser for now.

if __name__ == '__main__':
	unittest.main(warnings = 'ignore')
