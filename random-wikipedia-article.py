from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
import time
import pdfkit

class RandomWikiArticle:
	def __init__(self):
		self.title = ""
		self.url = ""
		self.driver = None

		#setup Chrome drive options to call it as headless
		self.options = webdriver.ChromeOptions()
		self.options.add_argument('--headless')

		#calls and displays initial random article
		self.getNewArticle()

	#call headless browser to open
	def launchChromeHeadless(self):
		#uses ChromeDriveManager so it never fails due to version issues
		self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

	#launch visible instance of Chrome
	def launchChrome(self):
		self.driver = webdriver.Chrome(ChromeDriverManager().install())

	#points browser to Wikipedia home page
	def goToWikipedia(self):
		self.driver.get("https://en.wikipedia.org/wiki/Main_Page")
	
	#calls a new random article
	def getNewArticle(self):
		#only launches new headless Chrome if there is not one currently open
		if self.driver == None:
			self.launchChromeHeadless()
			self.goToWikipedia()
		
		#finds the Random Article button on the page and clicks it
		random_button = self.driver.find_element_by_id("n-randompage")
		random_button.click()

		#save URL to launch if user wants to read more
		self.url = self.driver.current_url
		
		#captures the title of the article and displays
		ID = "firstHeading"
		self.title = self.driver.find_element_by_id(ID)

	#launches visible window to the article on Wikipedia
	def readArticle(self):
		self.driver.quit()
		self.launchChrome()
		self.driver.get(self.url)

	#saves the current article as a PDF file to the directory 
	#where the python script is running from
	def savePDF(self):
		pdfkit.from_url(self.url, self.title.text+'.pdf')
		print("*********************")
		print("Successfully saved as "+self.title.text+".pdf")

#variable to track user input
user_input = ""

#initialize first browser with random article
article = RandomWikiArticle()

while user_input != 'E':
	#get user input on the currently displayed article title
	print("*********************")
	user_input = input("Would you like to read about " + article.title.text + ", or save as a PDF? (Y or N, S to save, or E to quit):")
	print("*********************")

	#handle different user inputs
	if user_input == 'Y':
		article.readArticle()
	elif user_input == 'N':
		article.getNewArticle()
	elif user_input == 'S':
		article.savePDF()
		user_input = "Y"
	elif user_input == 'E':
		if article.driver != None:
			article.driver.quit()
		continue
	else:
		print("Invalid response")
		continue

	#get user input on whether they want to see more articles
	while user_input == 'Y':
		print("*********************")
		user_input = input("Would you like to see another title? (Y or N):")
		print("*********************")
		
		if user_input == 'Y':
			article.driver.quit()
			article.driver = None
			article.getNewArticle()
			user_input = "N"
			continue
		elif user_input == 'N' or user_input == 'E':
			user_input = "E"
			article.driver.quit()
			continue
		else:
			print("Invalid response")
			user_input = "Y"