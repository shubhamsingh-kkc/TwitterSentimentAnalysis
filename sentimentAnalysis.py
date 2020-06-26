from PyQt5.QtWidgets import *
import sys
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class windowDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 600, 800)
        self.createUi()
        self.show()
        apiKey = 'XXXXXXXXXXXXXXXXXXX'
        apiSecretKey = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        accessToken = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        accessTokenSecret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

        try:
            self.auth = OAuthHandler(apiKey, apiSecretKey)
            self.auth.set_access_token(accessToken, accessTokenSecret)
            self.api = tweepy.API(self.auth)
        except :
            self.msgBox = QMessageBox()
            self.msgBox.setText("Error : Authentication failed!!")
            self.msgBox.show()

    def createUi(self):
        self.createWidgets()
        self.setWindowTitle("Twitter Sentiment Analysis")
        vbox = QVBoxLayout()

        vbox.addWidget(self.grpbox1)
        vbox.addWidget(self.grpbox2)
        vbox.addWidget(self.grpbox3)
        vbox.addWidget(self.grpbox4)

        self.setLayout(vbox)

    def createWidgets(self):
        self.grpbox1 = QGroupBox()
        self.grpbox2 = QGroupBox()
        self.grpbox3 = QGroupBox()
        self.grpbox4 = QGroupBox()

        label1 = QLabel("Querry : ")
        label2 = QLabel("Count : ")
        self.querry = QLineEdit()
        self.count = QLineEdit()
        btn1 = QPushButton("Get Sentiments!")
        btn2 = QPushButton("Clear!")
        self.sentiments = QPlainTextEdit()
        self.sentiments.setReadOnly(True)

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()

        hbox1.addWidget(label1)
        hbox1.addWidget(self.querry)
        hbox2.addWidget(label2)
        hbox2.addWidget(self.count)
        hbox3.addWidget(btn1)
        hbox3.addWidget(btn2)
        hbox4.addWidget(self.sentiments)

        self.grpbox1.setLayout(hbox1)
        self.grpbox2.setLayout(hbox2)
        self.grpbox3.setLayout(hbox3)
        self.grpbox4.setLayout(hbox4)

        btn2.clicked.connect(self.clearText)
        btn1.clicked.connect(self.getSentiments)

    def clearText(self):
        self.querry.setText("")
        self.count.setText("")
        self.sentiments.setPlainText("")
        self.finalString = ""

    def getSentiments(self):
        self.main()
        self.sentiments.appendPlainText(self.finalString)

    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def getTweetSentiment(self, tweet):
        analysis = TextBlob(self.cleanTweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def getTweets(self, query, count=20):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count)

            for tweet in fetched_tweets:
                parsed_tweets = {}
                parsed_tweets['text'] = tweet.text
                parsed_tweets['sentiment'] = self.getTweetSentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweets not in tweets:
                        tweets.append(parsed_tweets)
                else:
                    tweets.append(parsed_tweets)
            return tweets
        except tweepy.TweepError as e:
            print("Error : " + str(e))

    def main(self):
        tweets = window.getTweets(query= self.querry.text(), count=int(self.count.text()))
        self.finalString = ""
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        self.finalString = self.finalString + ("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets))) + "\n"

        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        self.finalString = self.finalString + ("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets))) + "\n"

        self.finalString = self.finalString + ("Neutral tweets percentage: {} % \ ".format(
            100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets))) + "\n"

        self.finalString = self.finalString + ("\n\nPositive tweets:\n")
        i = 1
        for tweet in ptweets[:5]:
            self.finalString = self.finalString + str(i) + ". " + str((tweet['text']))
            self.finalString = self.finalString + "\n"
            i = i + 1

        self.finalString = self.finalString + ("\n\nNegative tweets:\n")
        j = 1
        for tweet in ntweets[:5]:
            self.finalString = self.finalString + str(j) + ". " + str((tweet['text']))
            self.finalString = self.finalString + "\n"
            j = j + 1


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = windowDialog()
    sys.exit(app.exec_())
