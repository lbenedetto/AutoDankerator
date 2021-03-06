import praw
import os
import urllib
import re
import string
from bs4 import BeautifulSoup


def prawLogin():
    print("Logging in")
    r = praw.Reddit('''Dank Bot v 1.46
By: /u/Styyxx and /u/larperdoodle
GitHub: https://github.com/larperdoodle/AutoDankerator''')
    settings = checkSettings('settings.txt')
    r.login('AutoDankerator', settings[2])
    return r


# This function parses through the provided HTML and returns a clean string of the About data
def getAboutText(url):
    if URLisValid(url):
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page)
        data = soup.find('h2', {'id': 'about'}).next_element.next_element.next_element
        return str(data)
    else:
        return "le tips fedora"  # This is what you get, Lars


# This changes <strong> to reddits format for bold
def convertFormatting(t):
    str(t)
    t = re.sub('<p>', '', t)
    t = re.sub('</p>', '', t)
    t = re.sub('<strong>', '**', t)
    t = re.sub('</strong>', '**', t)
    t = re.sub('<i>', '*', t)
    t = re.sub('</i>', '*', t)
    t = re.sub(r'<a href=".+">', '', t)
    t = re.sub("</a>", "", t)
    return t


# Checks if the bot has already replied to a comment
def alreadyDone(comment):
    done = False
    numofR = 0
    try:
        repliesArray = comment.replies
        numofR = len(list(repliesArray))
    except:
        pass
    if numofR != 0:
        for reply in comment.replies:
            if reply.author is not None and reply.author.name == 'AutoDankerator':
                done = True
                continue
    if comment.author.name == 'AutoDankerator':
        done = True
    if done:
        return True
    else:
        return False

# Creates a reply
def knowYourMeme(meme):
    dankSearch = clean(meme)
    dankURL = "http://knowyourmeme.com/memes/" + dankSearch
    info = convertFormatting(getAboutText(dankURL))
    if URLisValid(dankURL):
        reply = ''
        List = [">", info, "  \n  \n  ", "[", meme.strip(), "](", dankURL, ")  ",
                "  \nI am a bot, this action was performed automatically."]
        for item in List:
            reply += item
    else:
        reply = 'I do not know what "'
        reply += meme.strip()
        reply += '" is.'
    return reply


# Checks the submissions for comments that ask for me
def usernameMentions():
    for submission in subreddit.get_new(limit=25):
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        print("Searching comments in", submission)
        for comment in flat_comments:
            # Things that should happen if AutoDankerator is also in the comment
            if checkForWord("AutoDankerator", comment):
                if checkForWord("what is", comment):
                    dankSearch = comment.body.split("what is")
                    meme = dankSearch[1]
                    if meme.strip() == 'love':
                        reply = "[baby don't hurt me](https://www.youtube.com/watch?v=xhrBDcQq2DM)"
                    else:
                        reply = knowYourMeme(meme)
                    print("Replying to comment", comment)
                    comment.reply(reply).distinguish()
            # Things that should happen all the time always
            checkForWordAndReply('ayy lmao', comment, 'ayy lmao')
            checkForWordAndReply('well memed', comment, '[](/tip)')


# Removes punctuation from text
def clean(s):
    s = s.strip()
    s = re.sub('[%s]' % re.escape(string.punctuation), '', s)
    s = s.replace(" ", "-")
    return s


# Is URL valid and not a 404?
def URLisValid(url):
    try:
        urllib.request.urlopen(url)
        return True
    except:
        return False


def checkForWordAndReply(word, comment, reply):
    if checkForWord(word, comment):
        print("Replying to comment", comment)
        comment.reply(reply).distinguish()
    return True


def checkForWord(word, comment):
    if word.lower() in comment.body.lower() and alreadyDone(comment) == False:
        return True
    return False


def checkSettings(filename):
    settings = []
    try:
        if not os.path.exists(filename):
            raise IOError
        with open(filename) as file:
            for line in file:
                line = str(line.strip())
                settings.append(line)
        try:
            file.close()
        except:
            pass
    except IOError:
        pass
    except:
        pass
    return settings


# Main function
def main():
    r = prawLogin()
    settings = checkSettings('settings.txt')
    global subreddit
    subreddit = r.get_subreddit("dankmemes")
    if settings[1] == 'yes':
        usernameMentions()


main()
