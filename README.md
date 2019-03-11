# InsBot
  An instagram robot which provides all kinds of **APIs** for you to **interact** with your personal Instagram accounts and makes it easier to **grab user data** online without/with login.
  >  **NOTE: I'm not responsible for the results of using this tool or anything happens to your accounts.**
##  Dependency 
* Python 3.x
* MongoDB
*  Requirements:
    * requests 
    * pymongo    
    * w3lib    
    * requests-toolbelt       
 
 You can install the requirements by：`python install requirements.py`
## API
*  **[Accounts Login](accounts-login)**   
    * [x] user login
*  **[User Registration](user-registration)** 
    * [ ] send sign up sms code to phone    
    * [ ] create account
*  **[Without Login](without-login)**    
    * [x] get user info    
    * [x] get posts of a user    
    * [x] get a posted media page info     
    * [x] get comments of a posted media page    
    * [x] get recommends by keyword  
    * [x] get posts by tag name 
    * [x] explore posts of locations
*  **[Login Required Operations](login-required-operations)**
     * **Logined account operations**
        * [x] get account info    
        * [x] get my favorite posts
        * [x] follow tags
        * [x] unfollow tags
        * [x] follow user     
        * [x] unfollow user    
        * [x] like a posted media   
        * [x] unlike a posted media
        * [x] like a comment under a posted media 
        * [x] unlike a comment under a posted media
        * [x] save a posted media
        * [x] unsave a posted media 
        * [x] add a comment to a posted media 
        * [x] reply to any comment
        * [x] block user     
        * [x] unblock user    
        * [x] set account as a private account    
        * [x] unset account as a private account
        * [x] disable stroies sharing    
        * [x] enable stories sharing    
        * [x] disable showing presence    
        * [x] enable showing presence    
        * [x] set comments filter keywords    
        * [x] reset password    
        * [x] upload profile picture    
        * [x] remove profile picture    
        * [x] edit and update profiles   
        * [x] get push infos 
        * [x] get account activity notifications
        * [x] post photos  
        * [x] post story of photos
        * [x] delete a posted media/story
        * [x] delete a comment 
        * [x] mark checked notifications
     * **Data Crawling**
        * [x] get user followers    
        * [x] get user followings
        * [x] get user following tags     
        * [x] get user tagged posts    
        * [x] get user channel posts 
        * [x] get a posted media likers
        * [x] get a comment likers
     * **TO DO API**
         * [ ] send message
         * [ ] create favorite folder
         * [ ] get recommended users that maybe you are interested in
## Usage
> Due to the unti-spider systerm of Instagram，you should never crawl a great amount of data from Instagram at once，or you will get your IP blocked for a while by Ins instead.This tool is created for fun but not for bussiness use.If you have some IP proxies with a high anonymity，please minimize the number of the data requests to Instagram.

###  Accounts login
You can login your Instagram account by configuring **==``USERNAME``==**  and **==```PASSWORD```==** of ```config.py``` in InsBot's source code or just:
```python
from InsBot import Instagram,config
config.USERNAME = "XXX"
config.PASSWORD = "XXX"
account = Instagram()
account.login()
```
Another way to login:
```python
from InsBot import Instagram,config
account = Instagram()
account.login('username','password')
```
Or 
```python
from InsBot import Instagram,config
account = Instagram('username','password')
account.login()
```

## Changelog
> CREATED: 2019/03/02
> * created InsBot.
> 
> UPDATE:2019/03/08
> * add get user following tags
> * add get posts of a specified tag
> * add follow tags

