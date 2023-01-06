import os
import telebot
import flask
import requests
import conf
from bs4 import BeautifulSoup

bot = telebot.TeleBot(conf.TOKEN, parse_mode=None)
doc = requests.get('https://www.cimec.unitn.it/en', headers=conf.HEADERS)
soup = BeautifulSoup(doc.text, 'html.parser')
app = flask.Flask(__name__)


def handle_posts(path):
    posts_list = []
    posts = path.find_all(attrs="view-content")[0].find_all("a")
    for post in posts:
        posts_list.append(post.text.strip() + f"\n<i>Read more:\t <a href='{post['href']}'>link</a></i>" + "\n\n")
    return posts_list


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    description = "Bot description. To get the latest CIMeC news type /news. To get events type /events."
    bot.send_message(message.chat.id, description)


@bot.message_handler(commands=['news'])
def news_message(message):
    news_html = soup.find(text="News").parent.next_sibling.next_sibling
    news_list = handle_posts(news_html)
    # news = news_html.find_all(attrs="view-content")[0].find_all("a")
    # for new in news:
    #     news_list.append(new.text.strip() + f"\n<i>Read more:\t <a href='{new['href']}'>link</a></i>" + "\n\n")
    bot.send_message(message.chat.id, "".join(news_list), parse_mode="HTML")


@bot.message_handler(commands=['events'])
def events_message(message):
    event_html = soup.find("h2", text="Events").parent
    events_list = handle_posts(event_html)
    # events = event_html.find_all(attrs="view-content")[0].find_all("a")
    # for event in events:
    #     events_list.append(event.text.strip() + f"\n<i>Read more:\t <a href='{event['href']}'>link</a></i>" + "\n\n")
    bot.send_message(message.chat.id, "".join(events_list), parse_mode="HTML")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)


bot.infinity_polling()


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)