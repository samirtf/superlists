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


from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                print(repr(rows))
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Fulano has heard of an interesting new To-Do list online application.
        # He decided to check his homepage.
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box encouraging him to add another item.
        # He inserts "Use peacock feathers to make a fly"
        # (Use peacock feathers to fly - Fulano is very methodical)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        # The page refreshes again and now shows both items in your list.
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # So-and-so wonders if the site will remember your list.
        # Then he notices that the site generated a unique URL 
        # for her - there's a lilttle explanatoory text for that.
        self.fail('Finish the test!')

        # He accesses this URL - his to-do list is still there.


    def test_can_start_a_list_for_user(self):
        # He heard about an interesting new online task list application. 
        # She decides.
        
        # The page is refreshed again and now shows the two items in your list.
        self.wait_for_row_in_a_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_a_list_table('1: Buy peacock feathers')

        # Satisfied, he goes back to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # He starts a new task list.
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # He realizes that her list has a unique URL.
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, arrives on the site.

        # We use a new browser session to ensure that no information from Edith is coming from cookies.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis accesses the home page. There is no sign of Edith's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by inserting a new item. He's less interesting than Edith.
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, 'lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no sign of Edith's list.
        page_text = self.browser.fund_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep.
        
