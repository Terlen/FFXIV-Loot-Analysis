import asyncio
from json.decoder import JSONDecodeError
import pyxivapi
import json
import requests
import datetime
from statistics import median

def get_week_median_unit_price(item_name: str,sales_history: list[dict]):
    week_timestamp = (datetime.datetime.now() - datetime.timedelta(7)).timestamp()
    
    weekly_sales = [entry['pricePerUnit'] for entry in sales_history if entry['timestamp'] > week_timestamp and entry['hq'] == ('HQ' in item_name)]
    
    # Return median unitPrice for the last week. If there weren't any sales in the last week, instead return most recent unitPrice
    if len(weekly_sales) >= 1:
        return median(weekly_sales)
    else:
        return sales_history[0]['pricePerUnit']



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
    median_sale_prices = {}
    for item,id in item_id.items():
        r = requests.get(f'https://universalis.app/api/history/adamantoise/{id}').content
        try:
            market_board_history = json.loads(r.decode('utf-8'))
            median_sale_prices[item] = get_week_median_unit_price(item, market_board_history['entries'])
            
        except (JSONDecodeError, KeyError):
            median_sale_prices[item] = 0
           

    return median_sale_prices

async def get_item_market_price(items:list[str]) -> list[dict]:
    item_ids = await get_item_id(items)
    sale_data = await universalis_fetch(item_ids)
    return sale_data


if __name__ == "__main__":
    asyncio.run(get_item_market_price(["leather","potion HQ"]))


