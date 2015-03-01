# TODO: Move everything regarding flairs to here.
import os
import praw


def prawLogin():
    r = praw.Reddit(''''Dank Bot v 1.0
By: /u/Styyxx and /u/larperdoodle
Github: https://github.com/larperdoodle/AutoDankerator''')
    settings = checkSettings('settings.txt')
    r.login('AutoDankerator', settings[2])
    return r


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


def setFlairs():
    rank = 0

    for submission in subreddit.get_top_from_all(limit=50):
        rank += 1
        if rank <= 25:
            submission.set_flair("#" + str(rank))
        else:
            submission.set_flair(None)

def main():
    r = prawLogin()
    settings = checkSettings('settings.txt')
    global subreddit
    subreddit = r.get_subreddit("dankmemes")
    setFlairs()

main()