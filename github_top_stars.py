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

start_time = time.time()

target = open('github_top_stars.txt', 'w')
detail_stat = open('github_detail_stat.txt', 'w')

start = 2000
limit = 248000
step = 10

page = 1
count = 1
while start <= limit:
	end = start + step
	mod = end % step
	if mod != 0:
		end = end - mod
	url = 'https://api.github.com/search/repositories?q=stars:%d..%d&sort=stars&per_page=100&page=%d&order=asc' % (start, end, page)
	print url
	public_repos = requests.get(url, auth=(username, password)).json()
	total_count = public_repos['total_count']
	print "round %d [%d, %d] %d" % (count, start, end, total_count)
	if total_count > 0:
		detail_stat.write("%d-%d\t%d" % (start, end, total_count))
		detail_stat.write("\n")
	if total_count > 0:
		repos = public_repos['items']
		for repo in repos:
			name = repo['name']
			owner = repo['owner']['login']
			stars = repo['stargazers_count']
			watchers = repo['watchers_count']
			language = repo['language']
			forks_count = repo['forks_count']
			issues_count = repo['open_issues_count']
			target.write("%d-%d\t%s\t%s\t%d\t%d\t%s\t%d\t%d" % (start, end, name, owner, stars, watchers, language, forks_count, issues_count))
			target.write("\n")
	start = end + 1
	if start >= 3200:
		step = 100
	if start >= 9000:
		step = 1000
	if count % 30 == 0:
		# api call has limit 30 times/m'
		print "sleeping for 61 seconds"
		time.sleep(61)
	count = count + 1
detail_stat.close()
target.close()

finish_time = time.time()
cost = (finish_time - start_time)
print "task finished cost %d seconds" % cost