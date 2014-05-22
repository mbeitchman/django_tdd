from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'})

		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):
	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_all_items(self):
		Item.objects.create(text='foo foo')
		Item.objects.create(text='bar bar')

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response, 'foo foo')
		self.assertContains(response, 'bar bar')

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		expected_html = render_to_string('home.html')

		response = home_page(request)

		self.assertEqual(response.content.decode(), expected_html)

class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item_text = 'The first (ever) list item'
		second_item_text = 'The second item'

		first_item = Item()
		first_item.text = first_item_text
		first_item.save()

		second_item = Item()
		second_item.text = second_item_text
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]

		self.assertEqual(first_item_text, first_saved_item.text)
		self.assertEqual(second_item_text, second_saved_item.text)