import json

import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime
import requests


def create_post(title, text):
    article_url = ''

    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'title': title,
        'content': text,
        'status': 'publish',
    }
    if title != '' and text != '':
        r = requests.post('http://localhost:8000/wp-json/wp/v2/posts', headers=headers, json=json_data,
                          auth=('admin', 'admin'))
        if r.status_code == 201:
            article_url = r.json()['guid']['rendered']
    return article_url


def generate_article(stock_date):
    # Convert the string to a datetime object
    date_object = datetime.strptime(stock_date, "%Y-%m-%d")
    # Format the date
    formatted_date = date_object.strftime("%d %B %Y")
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    prompt = f'Write me an article on stock market performance for the date {formatted_date}, including key indices such as the S&P 500, Dow Jones Industrial Average, and NASDAQ Composite. Highlight notable gainers and losers, identifying the sectors driving market movement. Discuss any significant economic events, corporate announcements, or geopolitical factors influencing market trends. Include information on trading volume, volatility, and any technical patterns observed. Additionally, comment on the overall market sentiment, investor behavior, and potential implications for the upcoming trading sessions. Lastly, offer insights into relevant commodities, currencies, and interest rates that may have impacted the broader financial landscape. Add relevant headings where needed. Also suggest relevant Blog post title in H1 tag. At the end return data in JSON format with two fields: Title and Description where the "Title" contains the blog title and "Desrcription" contains the entire article. Do not return any other text besides JSON'
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(contents=prompt)
    response_text = response.text.replace("```json", '').replace("```", "")
    json_data = json.loads(response_text)
    return json_data


if __name__ == '__main__':
    url = ''
    # Assuming you have a date string
    date_string = "2023-12-22"
    article = generate_article(date_string)
    if article:
        print('Generating the article with title: {}'.format(article['Title']))
        url = create_post(article['Title'], article['Description'])
        print('Article generated success. Visit at; {}'.format(url))
