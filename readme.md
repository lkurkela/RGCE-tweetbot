JYVSECTEC RGCE Twitter "bot" / command line tool
===


Requirements
- Python 3 
  - pip
 
 
To install required libraries:
```
pip install -r requirements.txt
sudo python -m spacy download en
```

Configuration files:
- tuitter.json 
Contains users and server-url
- messages/*.txt
Pregenerated message topic files users can use for tweets, replies and direct messages


Twitter script usage:
```
tuitter.py <command> <args ..>
        
    Commands:
        listusers
            List users            
        listtopics
            List message topics
        register <user>
            Register user with given usernumber or * for all non-registered
            
        tweet [user] <message|#messagetopic>
            > tweet "Allo!"         # tuit with user #0
            > tweet 2 "Alloh"       # tuit with user #2      
            > tweet * "Alloh"       # tweet with random user  
        reply [user] <id> <message|#messagetopic>
            > reply 1234 "Thanks"   # reply with user #0
            > reply 1 1234 "Thanks" # reply with user #1
        dm [user] <nickname> <message|#messagetopic>
            > dm "salomon" "Hi!"
            > dm 1 "salomon" "#positive"
        rt [user] <id>
            > rt 1 123              # re-tweet message 123 with user 1
        like [user] <id>
            > like 1234             # like message 1234
            > like 4 1234
        follow [user] <nickname>
            > follow "salomon"
            > follow 4 "salomon"
            
        mtweet <count> <message|#messagetopic>
            > mtweet 2 "#positive"    # random users will tweet random 'positive'
        mreply <count> <id> <message|messagetopic>
            > mreply 2 1234 "#positive"
        mdm <count> <nickname> <message|#messagetopic>
            > mdm 2 "salomon" "Hello"
        mrt <count> <id>
            > mrt 5 1234
        mfollow <count> <nickname>
            > mfollow 5 "salomon"
        mlike <count> <id>
            > mlike 3 1234
```


User generator -script usage:
```
python user_generator.py
```
Outputs JSON-objects suitable to put into configuration file with types and amounts of identites defined in script.


Text generator -script usage:
```
python text_generator.py shakespeare.txt 100
```
Uses "shakespeare.txt" text file as an input to generate 100 lines of text.
