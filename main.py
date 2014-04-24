from bs4 import BeautifulSoup
import praw, re, time, datetime, urllib2, sys, os

# @([\w-]+[LHG]) : regex for low, high, G rank carves. Syntax: @dire-miralis-G / @barioth-L

##########
# CONFIG #
##########

hdr = {'User-Agent': 'MonsterInfoBot from Reddit made by /u/xozzo',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

user_agent = (
"MonsterInfoBot for /r/MonsterHunter on Reddit"
"version 1.0 by /u/xozzo"
)

reddit = praw.Reddit(user_agent = user_agent)

monsterList = ["great-jaggi", "great-baggi", "great-wroggi", "arzuros", "lagombi", "volvidon", 
"qurupeco", "crimson-qurupeco", "barroth", "jade-barroth", "uragaan", "steel-uragaan", 
"duramboros", "rust-duramboros", "rathian", "pink-rathian", "gold-rathian", "rathalos", 
"azure-rathalos", "silver-rathalos", "diablos", "black-diablos", "gigginox", "baleful-gigginox", 
"barioth", "sand-barioth", "royal-ludroth", "purple-ludroth", "gobul", "nibelsnarf", "lagiacrus",
"ivory-lagiacrus", "abyssal-lagiacrus", "agnaktor", "glacial-agnaktor", "nargacuga", 
"green-nargacuga", "lucent-nargacuga", "zinogre", "stygian-zinogre", "plesioth", "green-plesioth",
"brachydios", "ceadeus", "goldbeard-ceadeus", "deviljho", "savage-deviljho", "jhen-mohran", 
"hallowed-jhen-mohran", "alatreon", "dire-miralis"]
	
##############	
# END CONFIG #
##############

#############	
# FUNCTIONS #
#############
def login():
	TryingLogin = True
	while TryingLogin:
		try:
			global bot_user, bot_pass
			bot_user = raw_input("Bot username?\n> ")
			bot_pass = raw_input("Bot password?\n> ")
			print "Logging in.."
			reddit.login(bot_user, bot_pass)
			print "Successfully logged in as %s" % bot_user
			TryingLogin = False
			
		except praw.errors.InvalidUserPass:
			print 'Username/Password is wrong. Please re-enter username and password.'
		
		except Exception as e:
			if 'ratelimit' in e:
				print 'You tried logging in too many times in a short interval. Try again in 45 seconds, from %s' % datetime.datetime.now().time()
				time.sleep(45)
			else:
				print 'Exception: %s. Trying again.' % e
				time.sleep(2)


def get_monster_damage(monstername): 
	while True:
		try:
			monstername = monstername.lower() #must be lowercase or Kiranico's analytics goes crazy
			text = []
			print 'Getting source code from Kiranico..'
			site = 'http://www.kiranico.com/monster/%s' % monstername
			request = urllib2.Request(site, headers=hdr) 
			connect = urllib2.urlopen(request)
			soup = BeautifulSoup(connect)
			print 'Site source obtained for %s' % monstername
			damageTable = soup.find('div', id='damage-chart-panel').findAll('tr')
			for tr in damageTable:
				tags = '<[^>]+>' #pattern for <anything enclosed in these things>
				raw = str(tr)
				sub1 = re.sub(tags, '|', raw)
				sub2 = re.sub('\n\|', ' ', sub1)
				row = re.sub('\xe2\x80\x94', '-', sub2)
				row = row[1:-2] #get rid of some of the extra pipes (|) 
				text.append(row)
			return text
			
		except urllib2.URLError:
			print 'URLError raised. Could not get site source. Trying again in 5 minutes..'
			time.sleep(300)
			continue	
			
		except urllib2.HTTPError:
			print 'HTTPError raised. Could not get site source. Trying again in 5 minutes..'
			time.sleep(300)
			continue
			
def check_scores():
	print 'Checking scores..'
	me = reddit.get_redditor(bot_user)
	myComments = me.get_comments(limit=100)
	for post in myComments:
		if post.score<=(-1):
			post.delete()
			print 'Post deleted.'
			time.sleep(2)
	print '..done'
	time.sleep(2)

def find_tagged_monster_name(comment):
	monster_name_pattern = '@' + '([\w-]+)'
	return re.search(monster_name_pattern, comment.body, re.IGNORECASE)	
	
def logCommentId(comment):
	if os.path.isfile('commentid.txt'):
		with open('commentid.txt', 'a') as idfile:
			idfile.write(comment.id+'\n')
		print "Comment ID stored."
	else:
		open('commentid.txt', 'w').close()
		print 'commentid.txt could not be found. File created.'
		with open('commentid.txt', 'a') as idfile:
			idfile.write(comment.id+'\n')
		print "Comment ID stored."

def reply_with_damage_table(comment, name):
	print "Found match to monster list."
	reply_string = ''
	monster_damage = get_monster_damage(name.lower())
	
	for item in monster_damage:
		if item == monster_damage[0]:
			reply_string += item+'\n'
			reply_string += "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"
		else:
			reply_string += item+'\n'

	comment.reply("**[" + name.title() + "](http://www.kiranico.com/monster/" + name.lower() + ")**  \n\n" + reply_string + "  \n* * *  \n^(Summon: prefix monster name with '@'. If there is more than 1 word, substitute the space for a hyphen, e.g. @barioth, @dire-miralis.)  \n^(Will delete post if score is below 0.)  \n^(Have a bug to report/suggestion to make? Message my creator at /u/xozzo!)")
	print "Replied."
	logCommentId(comment)
	print "Sleeping for 2 minutes, starting %s" % datetime.datetime.now().time()
	time.sleep(120)
		
def logInvalidMonster(comment, name):
	print "Name does not exist in monster list. String entered: " + name
	logCommentId(comment)
	print "Sleeping for 15 seconds, starting %s" % datetime.datetime.now().time()
	time.sleep(15)
	
def isDuplicate(comment, name):
	tree = comment.submission.comments
	flat_tree = praw.helpers.flatten_tree(tree, nested_attr=u'replies', depth_first=False)
	
	for comm in flat_tree:
		subspecies = re.search('(?=(-'+name+'))', comm.body, re.IGNORECASE)
		if comm.author.name in ["MonsterInfoBot", bot_user] and name in comm.body and comm != comment and not subspecies:
			return True
			

#################	
# END FUNCTIONS #
#################

#############
# MAIN LOOP #
#############

login()

while True:
	try:
		check_scores()
		#Fellow programmers - do NOT run this bot in /r/MonsterHunter: /u/MonsterInfoBot is already running!
		comments_generator = reddit.get_subreddit('test').get_comments(limit = 50)
		
		print 'New comment generator fetched.'
		
		for comment in comments_generator:
			idList = [] #this list is reinitialized for every comment
			with open('commentid.txt', 'r') as idfile:
				idList = [line.rstrip() for line in idfile]
			
			searchObject = find_tagged_monster_name(comment)
			
			if searchObject and comment.id not in idList and comment.author.name not in ["MonsterInfoBot", bot_user]:
				print 'Found word with @ prefix.'
				name = searchObject.group(1).lower()
				
				if name in monsterList:
					isDuplicate(comment, name)
					
					if not isDuplicate(comment, name):
						reply_with_damage_table(comment, name)
						
					elif isDuplicate(comment, name):
						comment.reply("It appears that the information for " + name.title() + " has already been posted somewhere in this thread.  \n\nUse Ctrl+F, or if you're on a Mac, Cmd+F to look for the relevant information.")
						print 'There is already a post in this submission with this information (' + name + ').'
						logCommentId(comment)
						print 'Sleeping for 2 minutes, starting %s' % datetime.datetime.now().time()
						time.sleep(120)
									
				else:
					logInvalidMonster(comment, name)
						
			else:
				#Comment has no match, or author is bot_user
				if comment.id not in idList:
					print 'Could not find match in comment. Trying next comment..'
					logCommentId(comment)
					time.sleep(2)
					
				#Comment has already been processed
				elif comment.id in idList:
					print 'Comment already in ID list. Trying next comment..'
					time.sleep(2)
	
	except urllib2.HTTPError as e:
		print "Could not connect to Reddit (%s). Sleeping for 3 minutes." % e.code
		print 'Time: %s' % datetime.datetime.now().time()
		time.sleep(180)
		continue
				
	#TODO: Catching all exceptions is a faux-pas. Rewrite this!
	except Exception as e:
		print 'Error: %s. Sleeping for 3 minutes.' % e
		print 'Time: %s' % datetime.datetime.now().time()
		time.sleep(180)
		continue
		
#################
# END MAIN LOOP #
#################