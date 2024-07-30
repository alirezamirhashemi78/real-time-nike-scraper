import time
import random
from urllib import request 
import NikeThread as Th

if __name__ == "__main__":
    nikeThread = Th.NikeThread(t_id=0, t_type=Th.TYPES.NONE, t_catch=None)
    threads: list = []
    products_to_save: list = []



    threads_pages_url = nikeThread.threads_pages_url


    t_id = 0
    while True:

        t_id += 1

        # for setting pages url and pages count
        for i in range(3):
            set_urls_thread = Th.NikeThread(
                t_id=1,
                t_type=Th.TYPES.SET_URL,
                t_catch = None
            )
            set_urls_thread.start()
            set_urls_thread.join()


        if threads_pages_url:
            for _ in range(7):
                if threads_pages_url:
                    page_url = threads_pages_url.pop()
                    # print(page_url)
                    retrive_product_thread = Th.NikeThread(
                        t_id=t_id,
                        t_type=Th.TYPES.PRODUCT,
                        t_catch = page_url
                    )
                    retrive_product_thread.start()
                    threads.append(retrive_product_thread)
                    time.sleep(0.6)
                else:
                    break
        else:
            print("no page added !")  
        time.sleep(1)


        # for setting the reviews url:
        for _ in range(4):
            if nikeThread.products:
                # print("main: threads_review_products: ", len(nikeThread.threads_review_products))
                set_urls_thread = Th.NikeThread(
                    t_id=1,
                    t_type=Th.TYPES.SET_URL,
                    t_catch = None
                )
                set_urls_thread.start()
                set_urls_thread.join()
            else:
                pass
        time.sleep(0.2)
        

        for i in range(200):
            if nikeThread.threads_reviews_url:
                obj = nikeThread.threads_reviews_url.pop()
                retrive_review_thread = Th.NikeThread(
                    t_id = t_id,
                    t_type = Th.TYPES.REVIEW,
                    t_catch = obj
                )
                retrive_review_thread.start()
                s = random.choice([0, 0.1, 0.2])
                # time.sleep(s)
            else:
                print("naaaa")
                break
        
        if nikeThread.threads_reviews_url:
            save_review_thread = Th.NikeThread(
                    t_id = t_id,
                    t_type = Th.TYPES.SAVE_REVIEW,
                    t_catch = None
                )
            save_review_thread.start()
        else:
            print("no reviews available!!")

            

