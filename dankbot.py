import praw
import os
import urllib
import re
import string
from bs4 import BeautifulSoup


def prawLogin():
    print("Logging in")
    r = praw.Reddit(''''Dank Bot v 1.0
By: /u/Styyxx and /u/larperdoodle
Github: https://github.com/larperdoodle/AutoDankerator''')
    settings = checkSettings('settings.txt')
    print("Running with settings:", settings)
    r.login('AutoDankerator', settings[2])
    return r


def setFlairs():
    print("Getting comments")
    rank = 0

    for submission in subreddit.get_top_from_all(limit=50):
        rank += 1
        if rank <= 25:
            print("Adding flair for post #", rank)
            submission.set_flair("#" + str(rank))
        else:
            print("Removing flair from post #", rank)
            submission.set_flair(None)


def getAboutText(url):
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page)
    data = soup.find('h2', {'id': 'about'}).next_element.next_element.next_element
    return str(data)


def convertFormatting(t):
    str(t)
    t = re.sub('<p>', '', t)
    t = re.sub('</p>', '', t)
    t = re.sub('<strong>', '**', t)
    t = re.sub('</strong>', '**', t)
    t = re.sub(r'<a href=".+">', '', t)
    t = re.sub("</a>", "", t)
    return t


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
                if comment.author.name != "AutoDankerator":
                    done = True
                    continue
    if done:
        return True
    else:
        return False


def knowYourMeme(meme):
    dankSearch = clean(meme)
    dankURL = "http://knowyourmeme.com/memes/" + dankSearch
    info = convertFormatting(getAboutText(dankURL))
    if URLisValid(dankURL):
        reply = info
        reply += "  \n"
        reply += "["
        reply += meme.strip()
        reply += "]("
        reply += dankURL
        reply += ")  "
        reply += "  \nI am a bot, this action was performed automatically."
    else:
        reply = 'I do not know what "'
        reply += meme.strip()
        reply += '" is.'
    return reply


def usernameMentions():
    for submission in subreddit.get_new(limit=25):
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        print("Iterating through comments in", submission)
        for comment in flat_comments:
            # Things that should happen if AutoDankerator is also in the comment
            if checkForWord("AutoDankerator", comment):
                if checkForWord("what is", comment):
                    checkForWordAndReply('love', comment,
                                         "[baby don't hurt me](https://www.youtube.com/watch?v=xhrBDcQq2DM)")
                    print(comment)
                    dankSearch = comment.body.split("what is")
                    meme = dankSearch[1]
                    reply = knowYourMeme(meme)
                    comment.reply(reply)
            # Things that should happen all the time always


def clean(s):
    s = s.strip()
    s = re.sub('[%s]' % re.escape(string.punctuation), '', s)
    s = s.replace(" ", "-")
    return s


def URLisValid(url):
    try:
        urllib.request.urlopen(url)
        return True
    except:
        return False


def checkForWordAndReply(word, comment, reply):
    if checkForWord(word, comment):
        print("Replying to comment", comment)
        comment.reply(reply)


def checkForWord(word, comment):
    if word in comment.body and not alreadyDone(comment):
        return True
    return False


def checkSettings(filename):
    settings = []
    try:
        if not os.path.exists(filename):
            print("Cannot read from the file if it does not exist")
            raise IOError
        with open(filename) as file:
            for line in file:
                line = str(line.strip())
                settings.append(line)
        try:
            file.close()
        except:
            print("Could not close file")
    except IOError:
        print("I/O error")
    except:
        print("Unexpected error")
    return settings


def main():
    r = prawLogin()
    settings = checkSettings('settings.txt')
    global subreddit
    subreddit = r.get_subreddit("dankmemes")
    if settings[0] == 'yes':
        setFlairs()
    if settings[1] == 'yes':
        usernameMentions()


main()