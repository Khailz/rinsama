import requests, json, time

print("Searching for new users")

url = "{}".format(settings.api_url)
headers = {'Content-type': 'application/json'}
start = time.time()
r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.user))).elapsed.total_seconds()
end = time.time()
print(r)
