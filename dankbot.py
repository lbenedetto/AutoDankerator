import praw
import os
import collections

global subreddit
subreddit = None

# Login stuff
def prawLogin():
    print("Logging in")
    r = praw.Reddit('Dank Bot 1.0 by /u/Styyxx')
    password = checkSettings('password.txt')
    r.login('AutoDankerator', password)
    return r


def setFlairs(r):
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
            if reply.author != None and reply.author.name == 'AutoDankerator':
                done = True
                continue
    if done:
        return True
    else:
        return False


def usernameMentions(r):
    for submission in subreddit.get_new(limit=25):
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        already_done = set()
        print("Iterating through comments")
        for comment in flat_comments:
            if "AutoDankerator" in comment.body and comment.id not in already_done:
                if not alreadyDone(comment):
                    print("Replying to comment")
                    comment.reply('You called?')
                    already_done.add(comment.id)


def checkSettings(filename):
    try:
        if not os.path.exists(filename):
            print("Cannot read from the file if it does not exist")
            raise IOError
        with open('numbers.txt') as file:
            for line in file:
                if line == "True":
                    return True
        try:
            file.close()
        except:
            print("Could not close file")
    except IOError:
        print("I/O error")
    except ValueError:
        print("Data set contained a value which could not be converted to a float")
    except:
        print("Unexpected error")


def main():
    r = prawLogin()
    subreddit = r.get_subreddit("dankmemes")
    setFlairs(r)
    check = checkSettings('settings.txt')
    if check is True:
        usernameMentions(r)


main()