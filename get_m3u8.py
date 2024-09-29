from downloader import Download

headers = {
    "Host": "tmstr3.luminousstreamhaven.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://ate60vs7zcjhsjo5qgv8.com/",
    "Origin": "https://ate60vs7zcjhsjo5qgv8.com",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "TE": "trailers"
}


Download("https://tmstr3.luminousstreamhaven.com/stream_new/H4sIAAAAAAAAAw3MWVaDMBQA0C3lJQziJ2USm3AYQoC_DPUUCIX2YKWuXu8CrgTiY6WJrwOPeD4gIGA0dskXICUd7_2M2J2igfUIQt4NuEi2o03h0LDJKt1PRXa96iTPxXy9q9Q9NbC6Pd.IsoOnphhzfNzEUo003lbZmEFwODNho7ILYYjCqOnYKF97X6SM8qYHJZJJZ6bm9f6QkXVlEzsmaSWNws.S29Ig58HGfaFpQAxanyWqmMS2qNL23tyS.iLQs54s7ef8xMTxrBPL_q9S4Z1RQl9iPhxVBxMf316UQ1Pz_fuM4FG2RmjMVj3bic.xQ1M2t13eikVDP_GfS1dhHn0g2rFOZVVWLTM2vyj4A2S1kSNBAQAA/index-2.m3u8",
         "index-2.m3u8", headers).start()

Download.wait_downloads()