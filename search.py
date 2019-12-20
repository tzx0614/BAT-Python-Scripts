#! python3
# search.py - Opens several Google search results.

from requests_html import HTMLSession
import webbrowser
import logging
import sys

print("Searching the Internet...")

user_input = "+".join(sys.argv[1:])

response = HTMLSession().get(f"https://www.google.com/search?q={user_input}").html

div = response.find("div.r")
div_a_list = [d.find("a") for d in div]
links = [a.attrs["href"] for a_list in div_a_list for a in a_list]

min_searches = min(5, len(links))

opened_links = int()
iteration = int()

print(links)

while opened_links < min_searches:
    link = links[iteration]
    try:
        if link.startswith("https://"):
            webbrowser.open(link)
            opened_links += 1
        elif "https://" in link:
            index = link.index("https://")
            webbrowser.open(link[index:])
            opened_links += 1

    except Exception as e:
        logging.warning(f"Error: {e}")
    finally:
        iteration += 1
