import enum
import json

from operator import le
import os
import requests
import threading
import time
import math
from typing import Any
from fake_useragent import UserAgent
import orjson

class TYPES(enum.Enum):
    NONE = 0
    SET_PAGES = 1
    PRODUCT = 2
    REVIEW = 3
    SAVE_REVIEW = 4
    SET_REVIEW = 5

class NikeThread(threading.Thread):
    t_id: int = 0
    t_type: TYPES = TYPES.NONE
    t_catch: Any = None
    products_save_counter: int = 1
    reviews_save_counter: int = 1
    is_record_finished: bool = False
    is_saving_finished: bool = False
    is_first_record: bool = True
    headers = {
        'authority': 'www.nike.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'content-type': 'application/json',
        'user-agent': 'PostmanRuntime/7.35.0',
    }

    session = requests.Session()

    anchor: int = 0
    count: int = 48
    products_api_url: str = "https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=5E48B6B609950906C05E0BAE3406ABE4&country=at&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(AT)%26filter%3Dlanguage(en-GB)%26filter%3DemployeePrice(true)%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D{count}&language=en-GB&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D"

    products_count: int = 0
    threads_pages_url: list = []
    threads_products: list = []
    threads_review_products: list = []
    threads_reviews_url: list = []
    threads_reviews: list = []
    products_id: list = []
    products: list = []
    reviews: list = []



    def __init__(
        self, group=None, 
        target=None, name=None, args=(), kwargs=None, *, daemon=None,
        t_id, t_type, t_catch:Any):

        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.t_id = t_id
        self.t_type = t_type
        self.t_catch = t_catch


    @staticmethod
    def load_data(file_name):
        with open(file_name, "rb") as f:
            content = json.loads(f.read())
        return content


    @staticmethod
    def save_data(data, file_name):
        if NikeThread.is_first_record:
            pass
        else:
            if os.path.exists(file_name):
                content = NikeThread.load_data(file_name)
                data.extend(content)

        # if type(data) == dict:
        #     items.append(data)
        # elif type(data) == list:
        #     items.extend(data)

        with threading.Lock():
            with open(file_name, "w") as f:
                json.dump(data, f)
        return


    def set_products_count(self):
        url = NikeThread.products_api_url.format(anchor=NikeThread.anchor, count=NikeThread.count)
        response = requests.get(url, headers=NikeThread.headers)
        NikeThread.products_count = response.json()["data"]["products"]["pages"]["totalResources"]
    

    def set_pages_url(self):
        pages_count: int = math.ceil(NikeThread.products_count / NikeThread.count)
        url = NikeThread.products_api_url
        for i in range(0, pages_count+1):
            if (i*48) < NikeThread.products_count:
                NikeThread.threads_pages_url.append(url.format(anchor=(i * 48), count=48))
            else:
                NikeThread.threads_pages_url.append(url.format(anchor=(i*48) - ((i*48) - NikeThread.products_count), count=48))


    def retrive_product(self):
        url: str = self.t_catch
        response = requests.get(url, headers=self.headers)
        data = response.json()["data"]["products"]["products"]

        products = [
            product for product in data
            if product["cloudProductId"] not in NikeThread.products_id
        ]
        NikeThread.threads_products.extend(products)

        ids = [product["cloudProductId"] for product in data]
        NikeThread.products_id.extend(ids)
        NikeThread.products_id = list(set(NikeThread.products_id))
        
        # TODO: this part of function have to set on another function for 'set reviews':
        reviews_sample_url = str = "https://cdn-ws.turnto.com/v5/sitedata/78GDJmj4zEDYwwHsite/{p_id}/d/review/en_GB/0/50/%7B%7D/LOCAL/true/true/?"  
        NikeThread.threads_reviews_url.extend(
            [
                {
                    "url": reviews_sample_url.format(p_id=product["url"].split("/")[-1].split("-")[0]), 
                    "cloudProductId": product["cloudProductId"] 
                }
                for product in products
            ]
        )
        print("LEN PRODUCTS: ", len(NikeThread.threads_products))
    

    # def save_products(self, size):
    #     products = [
    #         pr for _ in range(size) if NikeThread.threads_products and (pr := NikeThread.threads_products.pop()) not in NikeThread.products
    #     ] 

    #     NikeThread.products.extend(products)

    #     NikeThread.save_data(NikeThread.threads_products, file_name=f"products.json")
        
        # with open("products.json", "w") as f:
        #     json.dump(NikeThread.products, f)
        # return   

    def set_reviews_url(self):
        pass


    def retrive_review(self):
        url: str = self.t_catch["url"]
        c_id: str = self.t_catch["cloudProductId"]
        ua = UserAgent(browsers=['edge', 'chrome'])
        headers = self.headers
        headers["user-agent"] = ua.random
        response = NikeThread.session.get(url, headers=headers)
        reviews = {"cloudProductId": c_id, "response": response.json()}
        NikeThread.threads_reviews.append(reviews)
    

    # def save_reviews(self, size):
    #     reviews = [
    #         rw for _ in range(size) if NikeThread.threads_reviews and (rw := NikeThread.threads_reviews.pop()) not in NikeThread.reviews 
    #     ]
    #     NikeThread.reviews.extend(reviews)

    #     NikeThread.save_data(NikeThread.reviews, file_name="reviews.json")

        # with open("reviews.json", "w") as f:
        #     json.dump(NikeThread.reviews, f)
        # return        
        # print("------------------------SAVED------------------------")


    def run(self):

        match self.t_type:

            case TYPES.SET_PAGES:
                if NikeThread.products_count == 0:
                    self.set_products_count()
                    print("P COUNT: ", NikeThread.products_count)
                else:
                    self.set_pages_url()
                    

            case TYPES.PRODUCT:
                self.retrive_product()

                size = 500
                # creating template size with range 140 for saving each 1000 product (the number is changable by variable 'size')
                # i had to add range to it because the absoulute size  may passed by the threades cause of their speeds
                if len(NikeThread.threads_products[(NikeThread.products_save_counter-1) * size : (NikeThread.products_save_counter) * size]) - size in range(-70, 70):
                    print("---->",NikeThread.products_save_counter, "/", (NikeThread.products_count // size)," ",  NikeThread.products_save_counter == (NikeThread.products_count // size))
                    self.save_data(NikeThread.threads_products, file_name="products.json")
                    print("LEN reviews_url_data", len(NikeThread.threads_reviews_url))
                    NikeThread.products_save_counter += 1

                else:
                    if len(NikeThread.threads_pages_url) == 0:
                        try:
                            NikeThread.save_data(NikeThread.threads_products, file_name=f"products.json")
                        except:
                            print("ERROR in func:<run> 1")
            

            # case TYPES.SET_REVIEW:
            #     self.set_reviews_url()

            case TYPES.REVIEW:
                if len(NikeThread.threads_reviews_url) > 0:
                    self.retrive_review()
                    print("retrive reviews: ", len(NikeThread.threads_reviews))


            case TYPES.SAVE_REVIEW:
                r_size = 500
                # if len(NikeThread.threads_reviews) >= r_size:
                if len(NikeThread.threads_reviews[(NikeThread.reviews_save_counter-1) * r_size : (NikeThread.reviews_save_counter) * r_size]) - r_size in range(-70, 70):
                    print("savin reviews...")
                    self.save_data(NikeThread.threads_reviews, file_name="reviews.json")
                    NikeThread.reviews_save_counter += 1
                    print("------------------------SAVED------------------------")
                else:
                    if len(NikeThread.threads_reviews_url) == 0:
                        try:
                            NikeThread.save_data(NikeThread.threads_reviews, file_name="reviews.json")
                        except:
                            print("ERROR in func:<run> 2")                

