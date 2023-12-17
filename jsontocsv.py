import csv
import json

# Open the JSON file and load the data
with open('international_articlesCLEANED.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Open the CSV file for writing and write the header row
with open('international_articlesCLEANED.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['Title', 'Link', 'Category', 'Author', 'Date', 'Summary', 'content'])

    # Loop through each item in the data and write a row to the CSV file
    for item in data:
        title = item.get('title', '')
        link = item.get('link', '')
        category = item.get('category', '')
        author = item.get('author', '')
        date = item.get('date', '')
        summary = item.get('summary', '')
        content = item.get('content', '')
        writer.writerow([title, link, category, author, date, summary, content])
