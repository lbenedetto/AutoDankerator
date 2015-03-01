import praw
import os


global subreddit
subreddit = None


def prawLogin():
    print("Logging in")
    r = praw.Reddit('Dank Bot 1.0 by /u/Styyxx')
    r.login('AutoDankerator', 'dayynklmao')
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


def usernameMentions(r):
    for submission in subreddit.get_new(limit=25):
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        already_done = set()
        print("Iterating through comments")
        for comment in flat_comments:
            if "AutoDankerator" in comment.body and comment.id not in already_done:
                commentReplies = r.get_submission(comment.permalink).comments[0]
                for commentReply in commentReplies:
                    if commentReply.author == "AutoDankerator":
                        pass
                print("Replying to comment")
                comment.reply('You called?')
                already_done.add(comment.id)


def checkSettings():
    try:
        if not os.path.exists('settings.txt'):
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
    check = checkSettings()
    if check is True:
        usernameMentions(r)

main()