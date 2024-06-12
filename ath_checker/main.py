import aiohttp
import asyncio
import json

async def fetch_wallet_data(session, url, headers, address):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                token_qualified = data.get("data", {}).get("pipelines", {}).get("tokenQualified", 0)
                print(f"Wallet: {address}, tokenQualified: {token_qualified}")
                return token_qualified
            else:
                print(f"Failed to retrieve data for wallet: {address}, status code: {response.status}")
                return 0
    except aiohttp.ClientError as e:
        print(f"Request failed for wallet: {address} with exception: {e}")
        return 0

async def main():
    
    with open('wallet_addresses.txt', 'r') as file:
        wallet_addresses = [line.strip() for line in file]

    total_token_qualified = 0
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://claims.aethir.com/",
        "Cookie": "ai_user=cuJKn25+Md49/5QWigZO7m|2024-06-12T10:28:17.890Z; _ga=GA1.1.978469649.1718188098; ai_session=hQC08cZsqbBEC+Bic4xpuF|1718188098780|1718188098780; _ga_L4GB10BMGM=GS1.1.1718188098.1.0.1718188107.0.0.0",
        "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Traceparent": "00-7925fa3dcce5474d911be33db55eb38b-c41a61f3b6fd4a33-01"
    }

    async with aiohttp.ClientSession() as session:
        tasks = []
        for address in wallet_addresses:
            url = f"https://claims.aethir.com/clique-aethir-api/campaign/aethir/credentials?walletAddress={address}"
            tasks.append(fetch_wallet_data(session, url, headers, address))
            await asyncio.sleep(0.1)

        results = await asyncio.gather(*tasks)
        total_token_qualified = sum(results)

    print(f"Total tokenQualified: {total_token_qualified}")

if __name__ == '__main__':
    asyncio.run(main())
