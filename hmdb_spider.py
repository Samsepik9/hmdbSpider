#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: samsepi0l ~For my girl CHAO~
# time: 2024/05/11
# 导入需要的模块

import requests
from lxml import etree
from requests.exceptions import RequestException
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import re
import time
import logging

# 配置日志
os.makedirs("log", exist_ok=True)
logging.basicConfig(filename='log/hmdbSpider1.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s' )

def load_datafile(path):
    check_data_list = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            check_data_list.append(line.strip())
    return check_data_list

def write_resultfile(result_path, results):
    with open(result_path, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入表头
        writer.writerow(["name", "hmdb_id", "url", "blood_tag", "endogenous_tag", "animal_tag"])
        # 写入结果
        for result in results:
            writer.writerow([result["name"], result["hmdb_id"], result["url"], result["blood_tag"], result["endogenous_tag"], result["animal_tag"]])

def format_hmdb_id(name):
    # 使用正则表达式提取HMDB后面的数字
    match = re.search(r'HMDB\d{7}', name)

    if match:
        hmdb_id = match.group()
    return hmdb_id

def parse_hmdb_info(hmdb_id, proxies=None):
    try:
        print("Now Search And Parse HMDBID: {}".format(hmdb_id))
        logging.info("Now Search And Parse HMDBID: {}".format(hmdb_id))
        url = f"https://hmdb.ca/metabolites/{hmdb_id}"
        response = requests.get(url, proxies=proxies, timeout=20)        
        if response and response.status_code == 200:
            response.encoding='utf-8'
            # print(response.text)
            # 使用etree解析HTML
            html = etree.HTML(response.text)
            name = html.xpath('//body/main/div[3]/h1/text()')[0].strip() if html.xpath('//body/main/div[3]/h1/text()')[0] else "Name not found"
            # chemical_formula = root.xpath('//dt[text()="Chemical Formula"]/following-sibling::dd/text()')[0].strip() if root.xpath('//dt[text()="Chemical Formula"]') else "Chemical Formula not found"
            blood_location = html.xpath('//li[@class="level-inner"]/a[contains(@class, "leaf-ontnode") and contains(@href, "https://en.wikipedia.org/wiki/Blood") and contains(text(), "Blood")]/text()') 
            endogenous_location = html.xpath('//li[@class="level-inner"]/a[contains(@class, "leaf-ontnode") and contains(@href, "https://en.wikipedia.org/wiki/Endogenous") and contains(text(), "Endogenous")]/text()')
            animal_location = html.xpath('//li[@class="level-inner"]/a[contains(@class, "leaf-ontnode") and contains(@href, "https://en.wikipedia.org/wiki/Animal") and contains(text(), "Animal")]/text()') 

            blood_str = blood_location[0] if blood_location else None
            endogenous_str = endogenous_location[0] if endogenous_location else None
            animal_str = animal_location[0] if animal_location else None

            if blood_str and endogenous_str and animal_str:
                hmdb_info =  {
                        "name": name[len('Showing metabocard for '):],
                        "hmdb_id": format_hmdb_id(name),
                        "url": url,  
                        "blood_tag": blood_str,
                        "endogenous_tag": endogenous_str,
                        "animal_tag": animal_str
                        }
                print("Parse HMDBID: {} Success".format(hmdb_id))
                logging.info("Parse HMDBID: {} Success".format(hmdb_id))
                return hmdb_info

        elif response and response.status_code == 404:
            print(f"Not found HMDBID: {hmdb_id}, URL requests failed with status code {response.status_code}")
            logging.error(f"Not found HMDBID: {hmdb_id}, URL requests failed with status code {response.status_code}")
            return None
            
        else:
            print(f"Not found HMDBID: {hmdb_id}, URL requests error with status code {response.status_code}")
            logging.error(f"Not found HMDBID: {hmdb_id}, URL requests error with status code {response.status_code}")
            return None
    except RequestException as e:
        print(f"Failed to retrieve information for metabolite {hmdb_id}: {e}")
        logging.error(f"Failed to retrieve information for metabolite {hmdb_id}: {e}")
        return None  


if __name__ == "__main__":

    proxies = {
        # 'http': 'http://127.0.0.1:1087',
        'http': 'http://192.168.1.177:10811',
        # 'https': 'http://10.10.1.10:1080',
    }   # proxies = None

    # metabolite_id = "HMDB0035674"  #HMDB0035674   HMDB0000792
    # info = get_metabolite_info(metabolite_id, proxies)
    # print(info)

    data_path = 'data/data1.txt'
    check_data_list = load_datafile(data_path)
    # 使用线程池进行并发查询
    with ThreadPoolExecutor(max_workers=10) as pools:
        futures = [pools.submit(parse_hmdb_info, data, proxies) for data in check_data_list]
        time.sleep(1)
        results = []
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                results.append(result)

    # 过滤掉None值的结果
    results = [result for result in results if result is not None]

    # 写入结果文件
    result_path = 'data/check_result1.csv'

    print("Now Write result to file: {}".format(result_path))
    write_resultfile(result_path, results)
    print("Search And Parse Done!")
    logging.info("Search And Parse Done!")
