import string
import sys
import datetime
import praw
import sqlite3
import os
from prawcore import OAuthException


# cleans a string by removing punctuation and trailing whitespace
# RETURN: cleaned string

def clean(s):
    return s.translate(str.maketrans('', '', string.punctuation)).rstrip().lower()


# make a string suitable for SQLite db
# RETURN: barely cleaned string
def soft_clean(s):
    return s.replace("'", "`")


# returns a PRAW reddit
# INPUT: settings file (used to establish reddit connection)
# RETURN: reddit (PRAW)
def get_reddit(settings):
    try:
        reddit = praw.Reddit(client_id=settings['client_id'],
                             client_secret=settings['client_secret'],
                             password=settings['client_password'],
                             user_agent=settings['user_agent'],
                             username=settings['client_username'])
        try:
            reddit.user.me()
        except OAuthException:
            print("Error: Invalid redddit API credentials")
            sys.exit()
        return reddit
    except KeyError:
        print("Error: Unable to read all reddit API credentials from init.ini")
        sys.exit()


# write init.ini to a default state
# INPUT: path to .ini
# RETURN: None
def write_ini(path):
    try:
        with open(path, "w+") as f:
            # important to leave empty string at the end so .join() works properly
            required_values = ["client_id",
                               "client_secret",
                               "client_password",
                               "user_agent",
                               "client_username",
                               "db_path",
                               ""]
            required_values = '=\n'.join(required_values)
            f.writelines(required_values)
    except IOError:
        print("Error: Unable to write init.ini")
        sys.exit()


# read the contents of an ini file and write them to a dictionary
# INPUT: path to .ini
# RETURN: dictionary (settings)
def read_ini(path):
    settings = {}
    try:
        with open(path, "r") as f:
            lines = [line.strip('\n').split("=") for line in f]
            for line in lines:
                try:
                    settings[line[0]] = line[1]
                except IndexError:
                    print("Error: Invalid arguments in .ini file")
                    sys.exit()
    except FileNotFoundError:
        print("Error: Requested .ini uninitialized.")
        write_ini(path)
        sys.exit()
    return settings


# find the current date
# RETURN: string (representing date in mm-dd-yyyy format)
def get_date():
    now = datetime.datetime.now()
    return str(now.month) + "-" + str(now.day) + "-" + str(now.year)


# creates a new daily row if necessary,
# adds each comment obtained from get_comments()
# to the database
# INPUT: db conn, praw reddit, date (mm-dd-yyyy)
# RETURN: None
def fill_table(conn, sub, titles, comments):
    count = 0
    cursor = conn.cursor()
    today = get_date()
    for comment in comments:
        try:
            cursor.execute(
                "INSERT INTO '{tn}' ('{col1}', '{col2}') VALUES ('{val1}', '{val2}');"
                    .format(tn=today, col1='Comments', col2='Titles', val1=comment, val2=titles[comment]))
            count += 1
        except sqlite3.IntegrityError:
            pass
        conn.commit()
    print("Total added to database: %d %s comments" % (count, sub))


# returns a list of lists containing all comments found on all posts from the day, as well as a list of titles
# RETURN: <list of titles, list of comments> (punctuation stripped)
def get_titles_and_comments(reddit, sub, settings):
    print('Browsing %s' % sub)
    count, interval = 0, -1
    comments = []
    # maps comment -> title
    titles = {}
    subreddit = reddit.subreddit(sub)
    top = subreddit.top('day')
    for post in top:
        post.comments.replace_more()
        clean_title = clean(post.title)
        for comment in post.comments.list():
            clean_comment = soft_clean(comment.body)
            titles[clean_comment] = clean_title
            comments.append(clean_comment)
            count += 1
            if settings['comment_progress_updates'].lower() == "true":
                if interval == -1:
                    try:
                        interval = int(settings['comment_progress_interval'])
                    except ValueError:
                        print("Error: Expecting an integer for 'comment_progress_interval'")
                if count % interval == 0:
                    print("%d comments recorded" % count)
    print("Total recorded: {count} {sub} comments".format(count=count, sub=sub))
    return titles, comments


# creates a directory named <subreddit> and creates
# a database with a table named comments within it
# INPUT: subreddit, settings
# RETURN: db connection
def create_database(sub, settings):
    today = get_date()
    # fetch path from .ini else resort to default
    try:
        db_path = settings["db_path"].format(sub=sub)
    except KeyError:
        db_path = "db/" + sub + "/comments.sqlite"

    # create the directory specified by db_path if required
    if not os.path.isdir(db_path.format(sub=sub)):
        os.makedirs(db_path.format(sub=sub))

    conn = sqlite3.connect(db_path.format(sub=sub) + "/comments.sqlite")

    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS '{tn}' ('{col1}' varchar(8000) unique, '{col2}' varchar(8000));"
            .format(tn=today, sub=sub, col1='Comments', col2="Titles"))
    return conn


# ensure at least one argument is passed in
# RETURN: None
def ensure_proper_usage(args):
    try:
        args[1]
    except IndexError:
        print("Usage: subcomments.py <subreddit1, subreddit2, ...>")
        sys.exit()
