import time
from ssutil import *


def main():
    settings = read_ini('init.ini')
    reddit = get_reddit(settings)
    for sub in sys.argv[1:]:
        conn = create_database(sub, settings)
        titles, comments = get_titles_and_comments(reddit, sub, settings)
        fill_table(conn, sub, titles, comments)
        conn.close()


if __name__ == "__main__":
    t0 = time.time()
    ensure_proper_usage(sys.argv)
    main()
    t1 = time.time()
    runtime = t1 - t0
    print("Runtime: %.2f seconds" % runtime)
