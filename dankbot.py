import praw
import os


def prawLogin():
    print("Logging in")
    r = praw.Reddit(''''Dank Bot v 1.0
By: /u/Styyxx and /u/larperdoodle
Github: https://github.com/larperdoodle/AutoDankerator''')
    settings = checkSettings('settings.txt')
    print(settings)
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
            # TODO Add things for Dankerator to say
            # It should be able to tell about itself, as well
            # as explain other memes.
            # Pull from KnowYourMeme?
            checkCommentForWordAndReply("AutoDankerator", comment, "You called?")


def checkCommentForWordAndReply(word, comment, reply):
    if word in comment.body and not alreadyDone(comment):
        print("Replying to comment")
        comment.reply(reply)


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