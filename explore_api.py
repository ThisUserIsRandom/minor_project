# import requests
# from bs4 import BeautifulSoup
import google.generativeai as genai

def scrape_wikipedia_intro(key,topic):
    genai.configure(api_key=key)

    factS = ""
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        factS = model.generate_content(f""" create a iframe of google news related to 
                                       {topic} 
                                       """)
    except Exception as e:
        factS = e

    return factS.candidates[0].content.parts[0].text.replace('\n','')


print(scrape_wikipedia_intro(key='AIzaSyBVZ4t-A7M_AlkgeBRlRznH6sr-GUjO4mo',topic='dinosaurs'))

# AIzaSyBVZ4t-A7M_AlkgeBRlRznH6sr-GUjO4mo/dinosaurs