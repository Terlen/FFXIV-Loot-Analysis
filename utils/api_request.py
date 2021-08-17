import asyncio
from json.decoder import JSONDecodeError
import pyxivapi
import json
import requests

async def get_item_id(items:list[str]):
    client = pyxivapi.XIVAPIClient(api_key='c43151f09079460b81b20a18b65e3ab0d6541c6cc6ad4fd4b09c709f544c38d3')
    item_ids = {}
    for item in items:
        # Remove HQ identifier for itemID lookup
        if item[-3:] == ' HQ':
            item = item[:-3]
            replace_HQ = True
        else:
            replace_HQ = False
        response = await client.index_search(
            name = item,
            indexes=["item"],
            columns=['ID','Name'],
            page=0
        )
        # Replace HQ identifier if removed
        if replace_HQ:
            item = item+' HQ'
        item_ids[item] = response["Results"][0]["ID"]
    await client.session.close()
    return item_ids

async def universalis_fetch(item_id:dict) -> list[dict]:
    last_sales = {}
    for item,id in item_id.items():
        r = requests.get(f'https://universalis.app/api/history/adamantoise/{id}').content
        try:
            market_board_history = json.loads(r.decode('utf-8'))
            for entry in market_board_history['entries']:
                if entry['hq'] == ('HQ' in item):
                    last_sales[item] = entry
                    break
        except JSONDecodeError:
            if r == b'Not Found':
                last_sales[item] = {'pricePerUnit':"None"}
            else:
                last_sales[item] = {'pricePerUnit':"Error"}
        

    return last_sales

async def get_item_market_price(items:list[str]) -> list[dict]:
    item_ids = await get_item_id(items)
    sale_data = await universalis_fetch(item_ids)
    return sale_data


if __name__ == "__main__":
    asyncio.run(get_item_market_price(["leather","potion HQ"]))


