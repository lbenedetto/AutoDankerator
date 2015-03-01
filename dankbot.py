import praw
import os
import collections

global subreddit
subreddit = None

# Login stuff
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


def is_summon_chain(post, r):
    if not post.is_root:
        parent_comment_id = post.parent_id
        parent_comment = r.get_info(thing_id=parent_comment_id)
        if parent_comment.author != None and str(
                parent_comment.author.name) == 'AutoDankerator':
            return True
        else:
            return False
    else:
        return False


def is_already_done(comment):
    done = False
    numofr = 0
    try:
        repliesarray = comment.replies
        numofr = len(list(repliesarray))
    except:
        pass
    if numofr != 0:
        for reply in comment.replies:
            if reply.author != None and reply.author.name == 'AutoDankerator':
                done = True
                continue
    if done:
        return True
    else:
        return False



def usernameMentions(r):
    pass


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