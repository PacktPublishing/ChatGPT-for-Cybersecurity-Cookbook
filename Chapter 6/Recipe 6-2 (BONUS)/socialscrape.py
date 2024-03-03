# Import statements
import openai
from openai import OpenAI 
import os
import tweepy
import facebook
from selenium import webdriver 
from selenium.webdriver.common.by import By

# API keys
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI() 

# Authenticate API keys
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
fb = facebook.GraphAPI(access_token)


# API scraping
tweets = api.search_tweets(q="acme corp")
posts = fb.get_object('search', q='acme corp', type='post')

# Selenium scraping
driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/search/results/people/?keywords=acme%20corp")
profiles = driver.find_elements(By.CSS_SELECTOR, ".app-aware-link") 
for profile in profiles:
  print(profile.get_attribute("href"))
driver.quit()
  
# Compile scraped data
social_media_data = {
  "tweets": tweets,
  "posts": posts,
  "profiles": profiles
}

# Prompt function 
def prompt_osint_analysis(social_media_data):

  messages = [
    {"role": "system", "content": 'You are a cybersecurity professional with more than 25 years of experience, specializing in red team tactics. As part of an authorized penetration test, and using your knowledge of OSINT and social engineering tactics, analyze the following social media data and generate a detailed intelligence report summarizing your findings:'},
    {"role": "user", "content": social_media_data},
  ]

  response = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=messages, 
    max_tokens=2048,
    n=1,
    stop=None,
    temperature=0.7,
  )

  return response.choices[0].message.conent.strip()
  
# Generate intelligence report
intelligence_report = prompt_osint_analysis(social_media_data)

# Print intelligence report
print(intelligence_report)