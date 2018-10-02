import praw
import sys
import sqlite3
import os
import datetime
import string
import time

settings = {}


def main():
    now = datetime.datetime.now()
    today = (str(now.month) + "-" + str(now.day) + "-" + str(now.year))
    try:
        reddit = praw.Reddit(client_id=settings['client_id'],
                             client_secret=settings['client_secret'],
                             password=settings['client_password'],
                             user_agent=settings['user_agent'],
                             username=settings['client_username'])
    except KeyError:
        print("Error: Unable to read all reddit API credentials from init.ini")
        sys.exit()

    for sub in sys.argv[1:]:
        cursor, conn = create_database(today, sub)
        fill_table(cursor, conn, reddit, today, sub)
        conn.close()


# creates a new daily row if necessary,
# adds each comment obtained from get_comments()
# to the database
# INPUT: db cursor, db conn, praw reddit, date (mm-dd-yyyy)
# RETURN: None
def fill_table(cursor, conn, reddit, today, sub):
    count = 0
    titles, comments = get_titles_and_comments(reddit, sub)
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


# creates a directory named <subreddit> and creates
# a database with a table named comments within it
# INPUT: date (mm-dd-yyyy)
# RETURN: db cursor, db connection
def create_database(today, sub):
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
    return cursor, conn


# returns a list of lists containing all comments found on all posts from the day, as well as a list of titles
# RETURN: list of strings (punctuation stripped)
def get_titles_and_comments(reddit, sub):
    count, interval = 0, -1
    comments = []
    # maps comment -> title
    titles = {}
    subreddit = reddit.subreddit(sub)
    top = subreddit.top('day')
    for post in top:
        post.comments.replace_more()
        clean_title = post.title.translate(str.maketrans('', '', string.punctuation))
        for comment in post.comments.list():
            clean_comment = comment.body.translate(str.maketrans('', '', string.punctuation))
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
    for comment in comments:
        print(comment)
    return titles, comments


# read the contents of an ini file and write them to a dictionary
# RETURN: None
def read_init():
    try:
        with open("init.ini", "r") as f:
            lines = [line.strip('\n').split("=") for line in f]
            for line in lines:
                try:
                    settings[line[0]] = line[1]
                except IndexError:
                    print("Error: Invalid arguments in init.ini")
                    sys.exit()
    except FileNotFoundError:
        print("Error: init.ini uninitialized. Please add your reddit API credentials.")
        write_ini()
        sys.exit()


# write init.ini to a default state
# RETURN: None
def write_ini():
    try:
        with open("init.ini", "w+") as f:
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


if __name__ == "__main__":
    t0 = time.time()
    read_init()

    # ensure proper command line usage
    try:
        arg1 = sys.argv[1]
    except IndexError:
        print("Usage: subcomments.py <subreddit1, subreddit2, ...>")
        sys.exit()
    main()
    t1 = time.time()
    runtime = t1 - t0
    print("Runtime: %.2f seconds" % runtime)
