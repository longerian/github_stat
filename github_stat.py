import requests
import time
import sys

def getHelp():
	print "read the fucking source code"

def __exit__():
	switch['h']()
	exit()

switch = {
	'h':getHelp
}

# you must provide your github username and password to access api
username = sys.argv[1]
password = sys.argv[2]

#the search api response has max 100 items per_page, max 10 pages, that mean max 1000 result for each query condition, see document
start_time = time.time()

target = open('github_stat.txt', 'w')
start = 100
limit = 250000
step = 1000

page = 1
count = 1
while start <= limit:
	end = start + step
	mod = end % 1000
	if mod != 0:
		end = end - mod
	url = 'https://api.github.com/search/repositories?q=stars:%d..%d&sort=stars&per_page=1&page=%d' % (start, end, page)
	print url
	public_repos = requests.get(url, auth=(username, password)).json()
	total_count = public_repos['total_count']
	print "round %d [%d, %d] %d" % (count, start, end, total_count)
	if total_count > 0:
		target.write("%d-%d\t%d" % (start, end, total_count))
		target.write("\n")
	start = end + 1
	if count % 30 == 0:
		# api call has limit 30 times/m'
		print "sleeping for 61 seconds"
		time.sleep(61)
	count = count + 1
target.close()

finish_time = time.time()
cost = (finish_time - start_time)
print "task finished cost %d seconds" % cost