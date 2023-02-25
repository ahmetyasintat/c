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
        rows = 30
        columnwidth = 20
        randchars = ['*','%','$','&','@','!','^','~','+','?','/','|','<','>']
        os.system('clear')
        
        for i in range(len(tickers)):
            k = i // rows
            sys.stdout.write("\033[%d;%dH" % (i - rows*k, k*columnwidth))
            sys.stdout.write("\033[33m%s%s" % (tickers[i], "-" * (columnwidth - len(tickers[i]))))

        while True:
            tasks = []
            for ticker in tickers:
                task = asyncio.ensure_future(fetch(session, 'https://api.binance.com/api/v3/ticker/price?symbol={}'.format(ticker)))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            for response in responses:
                xposition = 7 + (tickers.index(response['symbol']) // rows) * columnwidth
                sys.stdout.write("\033[%d;%dH" % (tickers.index(response['symbol']) % rows,xposition))
                sys.stdout.write("\033[37m%.2f%s" % (float(response['price']) ,randchars[random.randint(0, len(randchars) - 1)]))
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
            time.sleep(0.5)
            
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(main())
loop.run_until_complete(future)