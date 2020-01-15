# from selenium import webdriver

# browser = webdriver.Firefox()

# Fulano has heard of an interesting new To-Do list online application. He decided to check his homepage.
# browser.get('http://localhost:8000/')

# He realizes that the page title and header mention to-do lists.
# assert 'To-Do' in browser.title

# What I call functional tests, some people prefer to call acceptance tests or end-to-end tests. The bottom line is that these types of tests look at how the whole application works from the outside. Another term used is black box test, because the test knows nothing about the inside of the sustem under test.

# Acceptance tests must contain a human-readable story, that we can understand. We leave this explicit using comments that accompany the test code. When we create a new acceptance test, we can write that comments first to capture the main points of the User Story. Because they are human readable, we can even share them with non-programmers as a way to discuss the requirements and features of their application.

# TDD and agile software development methodologies often go hand in hand, and one of the topics often discussed is the minimum viable app; what is the simplest artifact we can build that is usable? Let's start by building this so we can test the water depth as quickly as possible.

# A minimum workable task list really only needs to allow the user to enter some task items and to remember them at the next access.

# This is what we call the expected failure, which is actually good news - not as good as a passing test, but at least the failure is for the right reason; we can have some confidence that we wrote the test correctly.

# There are some annoying little things that we will probably have to deal with. Firstly, the message "AssertionError" doesn't help much - it would be interesting if the test tells us what was actually found in the browser title. Also, the test left a pending Firefox window on the desktop, so it would be nice if it was automatically closed to us.

# One option would be to use the second parameter of the assert reserved word - something like:
# assert 'To-Do' in browser.title, "Browser title was " + browser.title


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Fulano has heard of an interesting new To-Do list online application.
        # He decided to check his homepage.
        self.browser.get('http://localhost:8000/')

        # He realizes that the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is encouraged to insert a task item immediately.
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Buy peacock feathers" into
        # a text box (Fulano's hobby is making fly fishing lures)
        input_box.send_keys('Buy peacock feathers')

        # When she enters, the page refreshes,
        # and now the page lists "1: Buy peacock feathers" as an item in a to-do list.
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

        # There is still a text box encouraging him to add another item.
        # He inserts "Use peacock feathers to make a fly"
        # (Use peacock feathers to fly - Fulano is very methodical)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page refreshes again and now shows both items in your list.
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.assertIn('2: Use peacock feathers to make a fly',
            [row.text for row in rows]
        )

        # So-and-so wonders if the site will remember your list.
        # Then he notices that the site generated a unique URL 
        # for her - there's a lilttle explanatoory text for that.
        self.fail('Finish the test!')

        # He accesses this URL - his to-do list is still there.

if __name__ == '__main__':
    unittest.main(warnings='ignore')


