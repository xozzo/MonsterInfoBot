**UPDATE (2015): Because Kiranico's site structure has changed, this program/bot no longer works as intended. A newer, better version of this bot will be written once Kiranico releases a developer API.**  

MonsterInfoBot
===============  

**[Reddit Link](http://www.reddit.com/r/MonsterHunter/comments/229ljg/introducing_umonsterinfobot/)**  

A reddit bot for /r/MonsterHunter that filters comments for @monster-names and fetches relevant information from kiranico.com  

Features
===============  
- The bot only gives you its damage chart (hitzones and elemental weaknesses) at the moment. See below for future plans.  
- Use `@` to prefix a monster name in your comment, e.g. `@sand-barioth`, `@lagiacrus`. It's case insensitive.  
- One monster per comment only. Bot only reads the first '@ word' it sees - even wrong ones.  
- The bot can read edited comments.
- Large monsters only.  
- The bot only works for MH3U monsters since Kiranico only has information for that game.  
- The bot deletes any of its posts that has a negative comment score.  
- The bot does not post same information twice in the same submission. If there is a duplicate, the bot will post a reply saying so.

Running Locally  
===============  
1. Fork/clone the project.  
2. Install python 2.6+ (not 3.x).  
3. Get [pip](http://www.pip-installer.org/en/latest/installing.html) or easy_install.  
4. Use pip or easy_install to get `beautifulsoup4`.  
5. Use pip or easy_install to get `praw`.  
6. Run `python main.py`.  
7. Do not point to /r/MonsterHunter to prevent duplicate posts!  

Changelog
===============
**4.6.14**  
- Added functionality where bot deletes post if comment score <=-1.  

**4.8.14**  
- Creates `commentid.txt` if not found in local directory.  

Merged pull request by icbat:  
- Factoring out code and placed them into functions
- Prepping code for implementation of new functions  

**4.12.14**
- Made a login function and added exception handling for failed logins  
- Changed method names in preparation for carve/drop feature implementation  
- Changed some console logs to improve comprehensibility  

**4.19.14**
- Bot no longer replies with duplicate information.
- Replaced `get_comments with` `comment_stream`.
- Bot will retry connection if connection to Reddit/Kiranico fails.  

**4.20.14**  
Merged pull request by icbat:  
- Fixed regex problem where it doesn't detect 3 word names.  
- Created .gitignore.  

**4.24.14**  
- Reverted back to `get_comments` from `comment_stream` as it was interfering with `check_scores`.  
- Shortened reply for duplicate posts to prevent page bloat.  
- Removed `bigmonster.txt` dependency; monster list is now initialized in program.  

**4.25.14**  
- Steve is here!  
- Removed some redundant lines of code at the cost of some readability.  

**4.29.14**  
- Removed `commentid.txt` dependency. With the new code, the bot can now process edited comments.  
- Removed some redundant lines of code.  

**3.30.16**  
- Removed 'Steve' code and other clutter.  
- Updated license year.  
- Updated TODO

To Do
===============
- Host bot online on a remote server.
- Possibly ignore invalid @ names and search the rest of the comment for a valid one?  
- Explain why there are two values in certain charts.  

Contributors
===============
icbat
