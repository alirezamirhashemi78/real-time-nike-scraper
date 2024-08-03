from ast import arg
import time
import random
import requests
import NikeThread as Th
import multiprocessing 

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


def operate_set_page_url_threads():
    # for setting pages url and pages count
    for i in range(4):
        set_urls_thread = Th.NikeThread(
            t_id=1,
            t_name="",
            t_type=Th.TYPES.SET_URL,
            t_catch = None
        )
        set_urls_thread.start()
        set_urls_thread.join()


def operate_set_reviews_url_threads():
    # for setting the reviews url:
    for _ in range(4):
        if nikeThread.products:
            set_urls_thread = Th.NikeThread(
                t_id=1,
                t_name="",
                t_type=Th.TYPES.SET_URL,
                t_catch = None
            )
            set_urls_thread.start()
            set_urls_thread.join()
        else:
            pass    


def operate_retrive_threads(threads_count: int, item: list, t_name: str):
    if item:
        for _ in range(threads_count):
            if item:
                # print(page_url)
                retrive_thread = Th.NikeThread(
                    t_id=2,
                    t_name=t_name,
                    t_type=Th.TYPES.RETRIVE,
                    t_catch = item.pop()
                )
                retrive_thread.start()
                threads.append(retrive_thread)
                time.sleep(0.1)
            else:
                print(f"no more {t_name} available !")  
                break
    else:
        print(f"no more {t_name} available !")   


if __name__ == "__main__":
    nikeThread = Th.NikeThread(t_id=0, t_name="", t_type=Th.TYPES.NONE, t_catch=None)
    threads: list = []
    products_to_save: list = []





    while True:
        Th.NikeThread.session = requests.Session()

        operate_set_page_url_threads()

        operate_retrive_threads(threads_count=10, item=nikeThread.pages_url, t_name="products")

        time.sleep(1)

        operate_set_reviews_url_threads()

        time.sleep(0.2)
        
        operate_retrive_threads(threads_count=300, item=nikeThread.reviews_url, t_name="reviews")

        operate_save_threads()

        # if nikeThread.reviews_url:
        #     for i in range(300):
        #         if nikeThread.reviews_url:
        #             obj = nikeThread.reviews_url.pop()
        #             retrive_thread = Th.NikeThread(
        #                 t_id = 3,
        #                 t_name="reviews",
        #                 t_type = Th.TYPES.RETRIVE,
        #                 t_catch = obj
        #             )
        #             retrive_thread.start()
        #             # s = random.choice([0, 0.1])
        #             # time.sleep(s)
        #         else:
        #             print("no more reviews available")
        #             break
        # else:
        #     print("no more reviews available")
        #     break

        


    

            

