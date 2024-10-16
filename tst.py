# #TODO:
# @staticmethod
# def is_id_exist(product_id):
#     ids = []
#     file = "ids.json"
#     is_exist = False
#     if os.path.exists(file):
#         file_contents = NikeThread.load_data(file)
#         ids.extend(file_contents)

#         if product_id in file_contents:
#             print(f"ID<{product_id}> is exist!")
#             is_exist = True

#     ids.append(product_id)
#     with open(file, "w") as f:
#         json.dump(ids, f)
#     return is_exist

#------------------------------------------------------------

# pages_count = 4
# products_count = 35
# steps = [i for i in range(products_count)]

# x = 0
# for i in range(0, (pages_count *10), len(steps[x: x+10])):
#     print(i + len(steps[x: x+10]))
#     # print("i: ", i)
#     x += 10
# print(steps)

#------------------------------------------------------------

# ids = [1, 2, 3, 4, 1 , 2, 3, 3, 4]

# ids2 = [2, 2, 6, 7]

# # ids = list(set(ids.extend(ids2)))

# ids.extend(ids2)
# ids = list(set(ids))
# print(ids)

#------------------------------------------------------------

# x = 6833

# print(x // 500)

# def foo(nums: list):
#     return set([sorted(nums).count(i) for i in sorted(nums)]) == {1}

# nums = [1, 2, 3, 4,1, 4]

# print(foo(nums))

#-------------------------------------------------------------
# from urllib import request
# import requests
# import threading
# import time
# import asyncio
# from time import perf_counter
# import aiohttp
# s = requests.Session()

# urls = [
#     "https://cdn-ws.turnto.com/v5/sitedata/78GDJmj4zEDYwwHsite/BV1021/d/review/en_GB/0/200/%7B%7D/LOCAL/true/true/?"
#     for _ in range(60)
# ]

# # def simple_request(url):
# #     response = requests.get(url)
# #     print(response.status_code)


# threads = []

# # for i in urls:
# #     url = urls.pop()
# #     t1 = threading.Thread(target=simple_request, args=(url, ))
# #     threads.append(t1)
# #     t1.start()


# def get_without_session(url):
#     response = requests.get(url)
#     print(response.status_code)

# def get_with_session(url):
#     response = s.get(url)
#     print(response.status_code)


# if __name__ == "__main__":

#     s = requests.Session()
#     start = time.time()
#     for i in range(len(urls)):
#         url = urls.pop()
#         t1 = threading.Thread(target=get_with_session, args=(url, ))

#         t1.start()
#         threads.append(t1)
    
#     for thread in threads:
#         thread.join()


#     end = time.time()
#     print("time: ", end - start)


#-------------------------------------------------------------
# import json

# class Writer:
#     import threading, queue
#     def __init__(self, file_name):
#         self.fname = file_name
#         self.buf = []
#         self.q = self.queue.Queue(128)
#         self.t = self.threading.Thread(
#             target = self._fileWrite)
#         self.t.start()

#     def finish(self):
#         self.q.put(self.buf)
#         self.buf = []
#         self.q.put(None)
#         self.t.join()

#     def write(self, obj):
#         self.buf.append(obj)
#         if len(self.buf) >= 50_000:
#             self.q.put(self.buf)
#             self.buf = []

#     def _fileWrite(self):
#         with open(self.fname, 'wb') as f:
#             while True:
#                 buf = self.q.get()
#                 if buf is None:
#                     break
#                 data = b''
#                 for e in buf:
#                     data += e.encode('ascii')
#                 f.write(data)

# # Example of usage

# with open("products.json", "r") as f:
#     content = f.read()

# writer = Writer('out.json')
# for i in range(1_00):
#     writer.write(content)
# writer.finish()

# import os
# print('Resulting file size:', os.path.getsize('out.json'))




#-------------------------------------------------------------
# import multiprocessing
# import threading


# numbers = []
# results = []

# def add_to_numbers(numbers):
#     num = len(numbers)
#     while True:
#         if len(numbers) > 100:
#             break
#         numbers.append(num)
#         num += 1
    
# def operate_numbers():
#     for _ in range(len(numbers)):
#         num = numbers.pop()
#         results.append(num * 2)

# if __name__ == "__main__":
#     with multiprocessing.Manager() as manager:

#         p1 = multiprocessing.Process(target=add_to_numbers, args=(numbers, ))
#         # p2 = multiprocessing.Process(target=operate_numbers, args=(numbers, ))
#         p1.start()
#         # p2.start()
#         p1.join()
#         # p2.join()
#         operate_numbers()
#         print(numbers)
#         print(results)


#-------------------------------------------------------------
# from ast import arg
# import multiprocessing
# import threading
# from time import time
# from tkinter import W
# from types import FunctionType


# numbers = [_ for _ in range(1, 10)]


# new_numbers = []


# def _sum():
#     s = 0
#     for i in numbers:
#         s += i
#     print("S :", s)


# def _mul():
#     m = 1
#     for i in numbers: 
#         m *= i
#     print("M :", m)


# def _add_numbers(args):
#     ns = args["numbers"]
#     q = args["queue"]
#     for n in ns:
#         q.put(n)

# def _print_new_numbers(new_numbers):
#     print(":man injam", len(new_numbers))
#     for i in new_numbers:
#         print(i+2, end=", ")


# def multi_function_process_runer(args):
#     functions = args["functions"]
#     inputs = args["inputs"]
#     for func in functions:
#         try:
#             func(inputs[func])
#         except:
#             func()



# # process_runer(_sum, _mul)
# if __name__ == '__main__':
#     q = multiprocessing.Queue()
#     args = {
#         "functions": (_add_numbers, _sum, _mul), 
#         "inputs": {
#             _add_numbers: {"numbers": numbers, 'queue': q},
#         }
#     }


#     p1 = multiprocessing.Process(target=multi_function_process_runer, args=(args, ))

#     p1.start()

#     p1.join()
    
#     while not q.empty():
#         new_numbers.append(q.get())
#     print("new_numbers: ", new_numbers)
    

#     p2 = multiprocessing.Process(target=_print_new_numbers, args=(new_numbers, ))
#     p2.start()
#     p2.join()


#-------------------------------------------------------------
# import json
# import ujson
# import time

# with open("products.json", "r") as file:
#     content = ujson.loads(file.read())

# s = time.time()
# with open("p.json", "w") as file:
#     json.dump(content, file)
# e = time.time()
# print("JSON: ", len(content),  "data in ", e-s, "s" )

# s = time.time()
# with open("p_ujson.json", "w") as file:
#     ujson.dump(content, file)
# e = time.time()
# print("uJSON: ", len(content),  "data in ", e-s, "s" )

#-------------------------------------------------------------
# l = []
# t = False   
# f = False

# print(not l and not t)

