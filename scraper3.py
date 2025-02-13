import http.client

conn = http.client.HTTPSConnection("api.scrapingant.com")

conn.request("GET", "/v2/general?url=https%3A%2F%2Fblog.goo.ne.jp%2Fishiseiji%2Farcv%2F%3Fpage%3D1%26c%3D%26st%3D0&x-api-key=07c0cc0bb3144fd1bd66aaeb7438c78b&proxy_type=residential&proxy_country=JP&browser=false")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))