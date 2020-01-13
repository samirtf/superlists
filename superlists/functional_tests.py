from selenium import webdriver

browser = webdriver.Firefox()

# Fulano has heard of an interesting new To-Do list online application. He decided to check his homepage.
browser.get('http://localhost:8000/')

# He realizes that the page title and header mention to-do lists.
assert 'To-Do' in browser.title

# What I call functional tests, some people prefer to call acceptance tests or end-to-end tests. The bottom line is that these types of tests look at how the whole application works from the outside. Another term used is black box test, because the test knows nothing about the inside of the sustem under test.

# Acceptance tests must contain a human-readable story, that we can understand. We leave this explicit using comments that accompany the test code. When we create a new acceptance test, we can write that comments first to capture the main points of the User Story. Because they are human readable, we can even share them with non-programmers as a way to discuss the requirements and features of their application.

# TDD and agile software development methodologies often go hand in hand, and one of the topics often discussed is the minimum viable app; what is the simplest artifact we can build that is usable? Let's start by building this so we can test the water depth as quickly as possible.

# A minimum workable task list really only needs to allow the user to enter some task items and to remember them at the next access.

# This is what we call the expected failure, which is actually good news - not as good as a passing test, but at least the failure is for the right reason; we can have some confidence that we wrote the test correctly.

# There are some annoying little things that we will probably have to deal with. Firstly, the message "AssertionError" doesn't help much - it would be interesting if the test tells us what was actually found in the browser title. Also, the test left a pending Firefox window on the desktop, so it would be nice if it was automatically closed to us.

# One option would be to use the second parameter of the assert reserved word - something like:
# assert 'To-Do' in browser.title, "Browser title was " + browser.title

