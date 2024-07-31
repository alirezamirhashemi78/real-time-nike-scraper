from ast import arg
import time
import random
import requests
import NikeThread as Th
import multiprocessing 

# def operate_save_threads(process_args: list):

#     data = {"products": process_args[0], "reviews": process_args[1]}
#     print(len(data["products"]))
#     for _ in range(2):
#         save_thread = Th.NikeThread(
#                 t_id = 0,
#                 t_name="",
#                 t_type = Th.TYPES.SAVE,
#                 t_catch = data
#             )
#         save_thread.start()

def operate_save_threads():

    for _ in range(2):
        save_thread = Th.NikeThread(
                t_id = 0,
                t_name="",
                t_type = Th.TYPES.SAVE,
                t_catch = None
            )
        save_thread.start()


if __name__ == "__main__":
    nikeThread = Th.NikeThread(t_id=0, t_name="", t_type=Th.TYPES.NONE, t_catch=None)
    threads: list = []
    products_to_save: list = []



    pages_url = nikeThread.pages_url



    while True:
        Th.NikeThread.session = requests.Session()

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


        if pages_url:
            for _ in range(10):
                if pages_url:
                    page_url = pages_url.pop()
                    # print(page_url)
                    retrive_thread = Th.NikeThread(
                        t_id=2,
                        t_name="products",
                        t_type=Th.TYPES.RETRIVE,
                        t_catch = page_url
                    )
                    retrive_thread.start()
                    threads.append(retrive_thread)
                    time.sleep(0.3)
                else:
                    break
        else:
            print("no page added !")  
        time.sleep(1)


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
        time.sleep(0.2)
        

        for i in range(200):
            if nikeThread.reviews_url:
                obj = nikeThread.reviews_url.pop()
                retrive_thread = Th.NikeThread(
                    t_id = 3,
                    t_name="reviews",
                    t_type = Th.TYPES.RETRIVE,
                    t_catch = obj
                )
                retrive_thread.start()
                # s = random.choice([0, 0.1])
                # time.sleep(s)
            else:
                print("naaaa")
                break

        

        # have to bee at least more than 2 threads
        # because it handles two operation of save
        # 1.saving products 2.saving reviews
        # save_process = multiprocessing.Process(target=operate_save_threads, args=( [Th.NikeThread.products, Th.NikeThread.reviews], )) 
        # save_process.start()
        operate_save_threads()

            

