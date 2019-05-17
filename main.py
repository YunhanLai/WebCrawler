import threading
from queue import Queue
from spider import Spider
from domain_url import *
from general import *

PROJECT_NAME = 'XiaChuFang'
HOME_PAGE = 'http://www.xiachufang.com/'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 3

queue = Queue()
spider = Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME)


# check if there are items in the queue, if so, crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + 'links in the queue')
        create_jobs()


# each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# create worker threads(will die when main exists)
def create_threads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# do the next job in the queue
def work():
    while True:
        url = queue.get()
        spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


create_threads()
crawl()
