Hiss
====

Hiss is a python twitter client that can be used from the terminal.

Configuring Hiss
====

Hiss must be configured before you use it. First, you have to edit *hiss_config.py* and enter your consumer and consumer secret keys (you need to create a twitter app before use this client).
There are other options you can change:
* num_tweets: The number of tweets to retrieve from the timeline. Value must be an integer lower than 200.
* use_dark_style: if is set to True it will use the dark scheme, for dark terminals. If set to False it will use the light scheme. *This feature is not implemented yet*.

Running Hiss
====

To run Hiss you just have to navigate to hiss directory with your terminal (cd /path/to/hiss) and then enter python hiss.py.
If this is the first time you access hiss.py you will not have a token.txt file and you will be asked to authorize the application in order to retrieve information from twitter.
Once you have done that, you will be able to access twitter from your terminal.

Hiss commands
====

* t: send a tweet and loads new tweets.
* to: send a tweet but not loads the timeline.
* rt: retweets a tweet.
* fav: favs a tweet.
* reply: send a reply to another tweet. Remember to include @username_to_reply if you want it to work.
* load: loads the timeline.
* block: blocks an user.
* report: reports an user for spam.
* exit: exits Hiss.

Roadmap
====

* Add color schemes (dark/light).
* Add support for spanish language.

Disclaimer
====

Hiss uses a library called oauth2 licensed with the MIT license. You can find this library here: https://github.com/simplegeo/python-oauth2