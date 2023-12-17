import json
import newspaper
import time

# Load the articles from the output.json file
with open('international_articles_translated.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Iterate over each article and scrape its content
for i, article in enumerate(articles):
    url = article['summary']
    try:
        # Instantiate a newspaper Article object with the URL
        article_obj = newspaper.Article(url)

        # Download and parse the article content
        article_obj.download()
        article_obj.parse()

        # Remove unwanted text from the article content
        unwanted_text = "You can only read Le Monde on one device at a time (computer, phone or tablet). It is only possible to read the World with an account on another device. It is a question of whether you can use another software to read a book or book. If you have another account, it is not necessary to use the same device to read the book. You must use the statement on a computer or tablet to read it. Le Monde was published in December 2012. It was an opportunity to publish a new written version of this edition and increase its ability to read this version with the help of another person, or you will not now be born another phone or desktop device on your computer, or on another reading system from your account at that time, from October 1st."
        if unwanted_text in article_obj.text:
            index = article_obj.text.index(unwanted_text)
            article_text = article_obj.text[:index]

        # If the unwanted text is not found, use the original article text
        else:
            article_text = article_obj.text

        # Add the cleaned text to the article dictionary
        article['content'] = article_text

        # Print the index of the processed article
        print(f"Processed article {i+1}/{len(articles)}")
        time.sleep(0.3)

    except Exception as e:
        # If there was an error scraping the article, add an error message to the dictionary
        article['content'] = f"Error scraping article content: {str(e)}"

# Save the updated articles to a new JSON file
with open('international_articlesCLEANED.json', 'w' , encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)
