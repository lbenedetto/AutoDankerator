import praw
import os
from urllib.request import urlopen
import re
import string


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
    if done:
        return True
    else:
        return False


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
                    dankSearch = comment.split("what is")
                    dankSearch = clean(dankSearch[1])
                    dankURL = "http://knowyourmeme.com/memes/" + dankSearch
                    if URLisValid(dankURL):
                        comment.reply(dankURL, "\n", "I am a bot, this action was performed automatically.")
            # Things that should happen all the time always
            checkForWordAndReply('ayy lmao', comment, 'ayy lmao')


def clean(s):
    s = s.strip()
    s = re.sub('[%s]' % re.escape(string.punctuation), '', s)
    s = s.replace(" ", "-")
    return s


def URLisValid(url):
    try:
        urlopen(url)
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