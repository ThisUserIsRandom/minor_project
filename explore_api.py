# import requests
# from bs4 import BeautifulSoup

import google.generativeai as genai
import markdown

def scrape_wikipedia_intro(key, topic):
    genai.configure(api_key=key)

    factS = ''
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        factS = model.generate_content(
            f""" generate an arictle on fun facts(atleat 20) and latest news on {topic} """
        )
        
        factS = factS.candidates[0].content.parts[0].text
    except Exception as e:
        factS = e

    html =  markdown.markdown(factS)

    return html.replace('\n','') #.replace('#','')[6:].replace('}[','},[').replace('\n','').replace('**','<h1>')

scrape_wikipedia_intro('AIzaSyBVZ4t-A7M_AlkgeBRlRznH6sr-GUjO4mo','dinosaurs')

# if __name__ == 'main':
#     pass

# AIzaSyBVZ4t-A7M_AlkgeBRlRznH6sr-GUjO4mo/dinosaurs
