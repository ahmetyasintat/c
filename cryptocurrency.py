import asyncio
import aiohttp
import time
import random
import sys
import os 
from tickers import tickers

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        count = 0
        rows = 20
        columnwidth = 30
        randchars = ['*','%','$','&','@','!','^','~','+','?','/','|','<','>']
        os.system('clear')
        
        sys.stdout.write("\033[6;0H")
        sys.stdout.write("\033[34mTicker    Price      CHG%\n")
        sys.stdout.flush()
        
        for i in range(len(tickers)):
            k = i // rows
            sys.stdout.write("\033[%d;%dH" % (i+7 - rows*k, k*columnwidth)) 
            sys.stdout.write("\033[33m%s%s" % (tickers[i], "-" * (columnwidth - len(tickers[i]))))
        
        while True:
            tasks = []
            for ticker in tickers:
                task = asyncio.ensure_future(fetch(session, 'https://api.binance.com/api/v3/ticker/24hr?symbol={}'.format(ticker)))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            for response in responses:
                xposition = 11 + (tickers.index(response['symbol']) // rows) * columnwidth
                sys.stdout.write("\033[%d;%dH" % (tickers.index(response['symbol']) % rows+7,xposition))
                sys.stdout.write("\033[37m%.2f%s" % (float(response['lastPrice']) ,randchars[random.randint(0, len(randchars) - 1)]))
                sys.stdout.write("\033[%d;%dH" % (tickers.index(response['symbol']) % rows+7, 22))
                sys.stdout.write("\033[37m%.2f%s" % (float(response['priceChangePercent']) ,"%"))
                if count % 250 == 0 and count > 0:
                    sys.stdout.write("\033[45;3H")
                    sys.stdout.write("Data Received: {}".format(count))
                    end_time = time.time()
                    sys.stdout.write("\033[46;3H")
                    seconds = int(((end_time - start_time) % 60))
                    sys.stdout.write("Time Elapsed: {}:{}".format(int((end_time - start_time) // 60), "0" + str(seconds) if seconds < 10 else seconds))
                    sys.stdout.write("\033[47;3H")
                    sys.stdout.write("Rate: {}x".format(int(count / (end_time - start_time))))
                sys.stdout.flush()
                count += 1
            time.sleep(1)


loop = asyncio.set_event_loop()
future = asyncio.ensure_future(main())
loop.run_until_complete(future)
