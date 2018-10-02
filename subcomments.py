import time
from ssutil import *


def main():
    settings = get_settings()
    today = get_date()
    reddit = get_reddit(settings)
    for sub in sys.argv[1:]:
        conn = create_database(today, sub, settings)
        titles, comments = get_titles_and_comments(reddit, sub, settings)
        fill_table(conn, today, sub, titles, comments)
        conn.close()


if __name__ == "__main__":
    t0 = time.time()
    # ensure proper command line usage
    ensure_proper_usage(sys.argv)
    main()
    t1 = time.time()
    runtime = t1 - t0
    print("Runtime: %.2f seconds" % runtime)
