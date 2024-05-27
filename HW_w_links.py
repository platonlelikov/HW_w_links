import aiohttp
import aiofiles
import random
import asyncio
from urllib.parse import urljoin
from bs4 import BeautifulSoup

async def get_links(session: aiohttp.ClientSession, url: str) -> list[str]:
    try:
        async with session.get(url, allow_redirects=True) as response:
            if response.status in (200, 404):
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                return [urljoin(url, link.get('href')) for link in soup.find_all('a') if link.get('href') and link.get('href').startswith(('http://', 'https://'))]
            return []
    except aiohttp.ClientError as e:
        print(f"Client error occurred while fetching {url}: {e}")
        return []

async def main() -> None:
    urls = [
        'https://regex101.com/',
        'https://docs.python.org/3/this-url-will-404.html',
        'https://www.nytimes.com/guides/',
        'https://www.mediamatters.org/',
        'https://1.1.1.1/',
        'https://www.politico.com/tipsheets/morning-money',
        'https://www.bloomberg.com/markets/economics',
        'https://www.ietf.org/rfc/rfc2616.txt'
    ]

    async with aiohttp.ClientSession() as session, aiofiles.open('file_w_links.txt', 'w') as f:
        tasks = [asyncio.create_task(get_links(session, url)) for url in urls]
        for task in asyncio.as_completed(tasks):
            links = await task
            if links:
                try:
                    await f.write('\n'.join(links) + '\n')
                except aiofiles.Error as e:
                    print(f"Error occurred while writing to the file: {e}")
            await asyncio.sleep(random.uniform(0.1, 0.3))

if __name__ == "__main__":
    asyncio.run(main())
