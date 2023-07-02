import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import keyboard

async def authenticate(page):

    await page.type('#rawUserName', 'username')
    await page.click('#identitySubmitBtn')
    await asyncio.sleep(0.5)  # Wait for 1 second
    await page.type('#j_password', 'password')
    await page.click('.btn.btn--people')

async def launch_cond():
    while True:
        command = await asyncio.get_event_loop().run_in_executor(None, input, 'Enter "start" to start scraping: ')
        if command.lower() == 'start':
            break

async def scrape_data(page1, page2):

    while True:
        if keyboard.is_pressed('shift'):
            print("Scraping paused")
            break

        data_total_agent = []
        data_total_queue = []

        html_content = await page1.evaluate('document.documentElement.outerHTML')

        soup = BeautifulSoup(html_content, 'html.parser')

        for i in range(0, 62):

            table_rows = soup.select('#dgrid_0-row-' + str(i))

            columns = table_rows[0].select('td')
            row_data = [column.get_text(strip=True) for column in columns]

            if row_data[0] == 'abc':
                break

            data_total_agent.append(row_data)

        html_content = await page2.evaluate('document.documentElement.outerHTML')

        soup = BeautifulSoup(html_content, 'html.parser')

        for i in range(0, 3):
            table_rows = soup.select('#dgrid_0-row-' + str(i))

            columns = table_rows[0].select('td')
            row_data = [column.get_text(strip=True) for column in columns]

            data_total_queue.append(row_data)

        print(data_total_agent)
        print(data_total_queue)
        await asyncio.sleep(1)  # Wait for 1 second

async def page_setup():
    edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    browser = await launch(executablePath=edge_path, headless=False) #visibility arg: headless=False
    page1 = await browser.newPage()
    await page1.goto('https://callcenter1.telecom.tamu.edu:8444/cuicui/Main.jsp')

    await asyncio.sleep(3)  # Wait for 3 seconds
    await authenticate(page1)
    await asyncio.sleep(1)  # Wait for 1 second

    page2 = await browser.newPage()
    await page1.goto('https://callcenter1.telecom.tamu.edu:8444/cuicui/permalink/?viewId=C0FF9E401000017B0006C90D0A120216&linkType=htmlType&viewType=Grid&refreshRate=3600')
    await page2.goto('https://callcenter1.telecom.tamu.edu:8444/cuicui/permalink/?viewId=566E9BC9DAE44D9BA227B85D74C7C69E&linkType=htmlType&viewType=Grid&refreshRate=3600')

    await launch_cond()

    quit = False
    while not quit:
        await scrape_data(page1, page2)

        while True:
            command = await asyncio.get_event_loop().run_in_executor(None, input, 'Enter "close" to exit or anything else to resume: ')
            if command.lower() == 'close':
                quit = True
            break

        if quit == True:
            await browser.close()

asyncio.get_event_loop().run_until_complete(page_setup())