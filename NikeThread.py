import enum
import os
import requests
import threading

import math
from typing import Any
from fake_useragent import UserAgent
import ujson

class TYPES(enum.Enum):
    NONE = 0

    # for set all urls that process need to coctinue in the lists!
    # 1.products_count, 2.pages_url, 3.products_url, 4.
    SET_URL = 1

    # request and retrive all items
    # 1.products,  2.reviews
    RETRIVE = 2

    # save all item that recived and stored in lists to json files
    # 1.product, 2.reviews
    SAVE = 3
 

class NikeThread(threading.Thread):

    t_id: int = 0
    t_name: str = ""
    t_type: TYPES = TYPES.NONE
    t_catch: Any = None

    is_record_finished: bool = False
    is_first_record: bool = True
    can_set_review: bool = True

    products_save_counter: int = 1
    reviews_save_counter: int = 1
    products_count: int = 0
    set_pages_counter: int = 0
    failed_request_counter: int = 0
    pages_url: list = []
    products: list = []
    products_id: list = []
    reviews_url: list = []
    poped_reviews_url: list = []
    reviews: list = []

    headers = {
        'authority': 'www.nike.com',
        'origin': 'https://www.nike.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'content-type': 'application/json',
        'user-agent': 'PostmanRuntime/7.35.0',
        'nike-api-caller-id': 'nike:dotcom:browse:wall.client:2.0'
    }

    session = None

    anchor: int = 24
    count: int = 24
    # products_api_url: str = "https://api.nike.com//discover/product_wall/v1/marketplace/TR/language/tr/consumerChannelId/d9a5bc42-4b9c-4976-858a-f159cf99c647?path=/tr/w/yeni-cikanlar-erkek-3n82yznik1&attributeIds=53e430ba-a5de-4881-8015-68eb1cff459f,0f64ecc7-d624-4e91-b171-b83a03dd8550&queryType=PRODUCTS&anchor={anchor}&count={count}"
    products_api_url: str = "https://api.nike.com//discover/product_wall/v1/marketplace/TR/language/tr/consumerChannelId/d9a5bc42-4b9c-4976-858a-f159cf99c647?path=/t/w&anchor={anchor}&count={count}"


    def __init__(
        self, group=None, 
        target=None, name=None, args=(), kwargs=None, *, daemon=None,
        t_id, t_name, t_type, t_catch:Any):

        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.t_id = t_id
        self.t_name = t_name
        self.t_type = t_type
        self.t_catch = t_catch


    @staticmethod
    def load_data(file_name):
        with open(file_name, "rb") as f:
            content = ujson.loads(f.read())
        return content


    @staticmethod
    def save_data(data, file_name):
        # print("==========LEN ARGS: ============", len(data))
        if NikeThread.is_first_record:
            pass
        else:
            if os.path.exists(file_name):
                content = NikeThread.load_data(file_name)
                data.extend(content)

        with threading.Lock():
            with open(file_name, "w") as f:
                ujson.dump(data, f)
        return


    def set_products_count(self):
        url = NikeThread.products_api_url.format(anchor=NikeThread.anchor, count=NikeThread.count)
        response = requests.get(url, headers=NikeThread.headers)
        NikeThread.products_count = response.json()["pages"]["totalResources"]
    

    def set_pages_url(self):
        pages_count: int = math.ceil(NikeThread.products_count / NikeThread.count)
        url = NikeThread.products_api_url
        for i in range(0, pages_count+1):
            if (i*24) < NikeThread.products_count:
                NikeThread.pages_url.append(url.format(anchor=(i * 24), count=24))
            else:
                NikeThread.pages_url.append(url.format(anchor=(i*24) - ((i*24) - NikeThread.products_count), count=24))


    def set_reviews_url(self):
        reviews_sample_url: str = "https://cdn-ws.turnto.com/v5/sitedata/78GDJmj4zEDYwwHsite/{p_id}/d/review/en_GB/0/50/%7B%7D/LOCAL/true/true/?"  
        NikeThread.reviews_url.extend(
            [
                wl_rev 
                for product in NikeThread.products
                if 
                (wl_rev := {
                    "url": reviews_sample_url.format(p_id=product[0]["productCode"]), 
                    "globalProductId": product[0]["globalProductId"] 
                }) 
                not in NikeThread.reviews_url and wl_rev not in NikeThread.poped_reviews_url
            ]
        )


    def retrive_product(self):
        url: str = self.t_catch
        try:
            response = requests.get(url, headers=self.headers)

        
            data = response.json()["productGroupings"]
            products = [
                item["products"] for item in data
                if item["products"][0]["globalProductId"] not in NikeThread.products_id
            ]

            NikeThread.products.extend(products)

            ids = [item["products"][0]["globalProductId"] for item in data]
            NikeThread.products_id.extend(ids)
            NikeThread.products_id = list(set(NikeThread.products_id))

            print("LEN PRODUCTS: ", len(NikeThread.products))
        except:
            NikeThread.failed_request_counter += 1
            print(response.status_code)
            print("error in func:<retrive_product>")


    def retrive_review(self):
        url: str = self.t_catch["url"]
        c_id: str = self.t_catch["globalProductId"]
        ua = UserAgent(browsers=['edge', 'chrome'])
        headers = self.headers
        headers["user-agent"] = ua.random
        try:
            response = NikeThread.session.get(url, headers=headers)


            reviews = {"cloudProductId": c_id, "response": response.json()}
            NikeThread.reviews.append(reviews)
        except:
            NikeThread.failed_request_counter += 1
            print("request failed!!: <url>")
        
    

    def run(self):

        match self.t_type:

            case TYPES.SET_URL:

                if self.t_name == "page":
                    if NikeThread.products_count == 0:
                        self.set_products_count()
                        print("P COUNT: ", NikeThread.products_count)

                    if len(NikeThread.pages_url) == 0 :
                        self.set_pages_url()

                elif self.t_name == "review":
                    if NikeThread.can_set_review:
                        self.set_reviews_url()
                    else:
                        print("no more new product to get its reviews...")

            case TYPES.RETRIVE:
                
                if self.t_name == "products" :
                    self.retrive_product()
                

                if self.t_name == "reviews":
                    if len(NikeThread.reviews_url) > 0:
                        self.retrive_review()
                        print("retrive reviews: ", len(NikeThread.reviews))       
                    else:
                        print("no reviews available!!")           
            

            case TYPES.SAVE:

                # products:
                # creating template size with range 140 for saving each 1000 product (the number is changable by variable 'size')
                # i had to add range to it because the absoulute size  may passed by the threades cause of their speeds
        
                size = 500

                if len(NikeThread.products[(NikeThread.products_save_counter-1) * size : (NikeThread.products_save_counter) * size]) - size in range(-70, 70):
                    print("---->",NikeThread.products_save_counter, "/", (NikeThread.products_count // size)," ",  NikeThread.products_save_counter == (NikeThread.products_count // size))
                    self.save_data(NikeThread.products, file_name="products.json")
                    print("LEN reviews_url_data", len(NikeThread.reviews_url))
                    NikeThread.products_save_counter += 1
                else:
                    if len(NikeThread.pages_url) == 0:
                        try:
                            NikeThread.save_data(NikeThread.products, file_name=f"products.json")

                        except:
                            print("ERROR in func:<run> 1")
                


                # reviews:
                r_size = 700
                if len(NikeThread.reviews[(NikeThread.reviews_save_counter-1) * r_size : (NikeThread.reviews_save_counter) * r_size]) - r_size in range(-70, 70):
                    print("savin reviews...")
                    self.save_data(NikeThread.reviews, file_name="reviews.json")
                    NikeThread.reviews_save_counter += 1
                    print("------------------------SAVED------------------------")
                else:
                    if len(NikeThread.reviews_url) == 0:
                        try:
                            NikeThread.save_data(NikeThread.reviews, file_name="reviews.json")

                        except:
                            print("ERROR in func:<run> 2")  



