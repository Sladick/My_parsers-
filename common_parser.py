import datetime
import requests
import json

headers = {
    'Accep': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'X-Is-Ajax-Request': 'X-Is-Ajax-Request',
    'X-Requested-With': 'XMLHttpRequest'
}

start_time = datetime.datetime.now()
# url = 'https://roscarservis.ru/catalog/legkovye/?PAGEN_1=2&isAjax=true'

# r = requests.get(url=url, headers=headers)
#
# with open("r.json", "w", encoding='UTF-8') as file:
#     json.dump(r.json(), file, indent=4, ensure_ascii=False)

with open("r.json", "r", encoding='UTF-8') as file:
    data = json.load(file)

page_count = data['pageCount']
data_list = []
for page in range(1, page_count + 1):
    url = f'https://roscarservis.ru/catalog/legkovye/?PAGEN_1={page}'
    r = requests.get(url=url, headers=headers)
    data = r.json()
    items = data['items']

    possible_stores = ["discountStores", "fortochkiStores", "commonStores"]
    for item in items:
        total_amount = 0

        item_name = item["name"]
        item_price = item["price"]
        item_img = f'https://roscarservis.ru{item["imgSrc"]}'
        item_url = f'https://roscarservis.ru{item["url"]}'

        stores = []
        for ps in possible_stores:
            if ps in item:
                if item[ps] is None or len(item[ps]) < 1:
                    continue
                else:
                    for store in item[ps]:
                        store_name = store["STORE_NAME"]
                        store_price = store["PRICE"]
                        store_amount = store["AMOUNT"]
                        total_amount += int(store["AMOUNT"])

                        stores.append(
                            {
                                "store_name": store_name,
                                "store_price": store_price,
                                "store_amount": store_amount
                            }
                        )
        data_list.append(
            {
                "name": item_name,
                "price": item_price,
                "url": item_url,
                "img_url": item_img,
                "stores": stores,
                "total_amount": total_amount
            }
        )

    print(f"[INFO] Обработал {page}/{page_count}")

cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

with open(f"data_{cur_time}.json", "a", encoding='UTF-8') as file:
    json.dump(data_list, file, indent=4, ensure_ascii=False)

diff_time = datetime.datetime.now() - start_time
print(diff_time)