import feedparser
d = feedparser.parse('http://www.nyaa.se/?page=rss&user=64513')
print(d['feed']['title'])
for x in d['entries']:
    if "720" not in x['title']:
        continue
    show = x['title'].rsplit(' ', 3)[0]
    episode = x['title'].rsplit(' ', 1)[0]
    episode = episode.split('-', 1)[1]
    print(show.split(' ', 1)[1], "|", episode)
