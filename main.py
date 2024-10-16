from ast import arg
import time
import random
import requests
import NikeThread as Th
import multiprocessing 
import pyfiglet 



def operate_save_threads():
    # have to bee at least 2 threads because it handles two operation of save: 1.saving products 2.saving reviews
    for _ in range(2):
        save_thread = Th.NikeThread(
            t_id = 0,
            t_name="",
            t_type = Th.TYPES.SAVE,
            t_catch = None
        )
        # q.put(save_thread)
        save_thread.start()


def operate_set_url_threads(t_name):
    # for setting pages url and pages count
    for i in range(3):
        set_urls_thread = Th.NikeThread(
            t_id=1,
            t_name=t_name,
            t_type=Th.TYPES.SET_URL,
            t_catch = None
        )
        set_urls_thread.start()
        set_urls_thread.join()


def operate_retrive_product_threads(threads_count: int, item: list, t_name: str):
    if nikeThread.pages_url:
        nikeThread.can_set_review = True
        
        for _ in range(threads_count):
            if  nikeThread.pages_url:
                # print(page_url)
                retrive_thread = Th.NikeThread(
                    t_id=2,
                    t_name=t_name,
                    t_type=Th.TYPES.RETRIVE,
                    t_catch = nikeThread.pages_url.pop()
                )
                retrive_thread.start()
                # threads.append(retrive_thread)
                time.sleep(0.2)
            else:
                print(f"1. no more {t_name} available !")  
                break
    else:
        nikeThread.can_set_review = False
        print("set_review threads is off")
        print(f"2. no more {t_name} available !")   


def operate_retrive_review_threads(threads_count: int, item: list, t_name: str):
    threads =  []
    if nikeThread.reviews_url:
        for _ in range(threads_count):
            if  nikeThread.reviews_url:
                # print(page_url)
                url = nikeThread.reviews_url.pop()
                nikeThread.poped_reviews_url.append(url)
                retrive_thread = Th.NikeThread(
                    t_id=2,
                    t_name=t_name,
                    t_type=Th.TYPES.RETRIVE,
                    t_catch = url
                )
                retrive_thread.start()

                threads.append(retrive_thread)
                # time.sleep(0.1)
            else:
                print(f"1. no more {t_name} available !")  
                break
    else:
        print(f"2. no more {t_name} available !")   
        
    [t.join() for t in threads]


if __name__ == "__main__":

    Th.NikeThread.session = requests.Session()
    nikeThread = Th.NikeThread(t_id=0, t_name="", t_type=Th.TYPES.NONE, t_catch=None)

    styled_text=pyfiglet.figlet_format('real-time scraper')
    print(styled_text)
    
    operate_set_url_threads(t_name="page")
    print("program starts in 3s...")
    time.sleep(3)




    while True:
        if not nikeThread.can_set_review and not nikeThread.reviews_url:
            print("recording has been done successfuly")
            print("FAILED REQUESTS COUNT: ", nikeThread.failed_request_counter)
            break


        Th.NikeThread.session = requests.Session()

        operate_retrive_product_threads(threads_count=10, item=nikeThread.pages_url, t_name="products")
        operate_set_url_threads(t_name="review")
        print("***************** LEN REVIEWS: ",  len(nikeThread.reviews_url))
        operate_retrive_review_threads(threads_count=350, item=nikeThread.reviews_url, t_name="reviews")

        # print("FAILED REQUESTS COUNT: ", nikeThread.failed_request_counter)

        operate_save_threads()


        