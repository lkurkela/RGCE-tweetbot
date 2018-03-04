#!/usr/bin/python3
# -*- coding: utf-8 -*-
import glob
import json
import random
import os.path
import re
import sys
from gnusocial import accounts
from gnusocial import direct_messages
from gnusocial import friendships
from gnusocial import statuses


def usage():
    print('''
    Usage:
        x.py <command> <args ..>
        
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
''')


def read_config():
    with open('tuitter.json', encoding='utf-8') as f:
        read_data = f.read()
        jason = json.loads(read_data)
    return jason


def write_config(config):
    json_string = json.dumps(config, sort_keys=True, indent=2)
    with open('tuitter.json', 'w', encoding='utf-8') as f:
        f.write(json_string)


def get_users_count(config):
    userlist = config['users']
    usercount = len(userlist)
    return usercount


def read_message_file(topic):
    if os.path.isfile('messages/%s.txt' % topic):
        with open('messages/%s.txt' % topic, encoding='utf-8') as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        return content

    else:
        return None


def get_messages_count(config, msgtype):
    msglist = read_message_file(msgtype)
    if msglist is not None:
        msgcount = len(msglist)
        return msgcount
    else:
        return 0


def parse_message(config, message, usedmessages=None):
    if message[0] == "#":
        msg = random_message(config, message[1:], usedlist=usedmessages)
    else:
        msg = message

    return msg


def parse_user(config, userid):
    if userid == '*':
        user = random_user(config)
    else:
        user = config['users'][int(userid)]
    return user


def random_message(config, msgtype, usedlist=None):
    msglist = read_message_file(msgtype)
    if msglist is not None:
        msgcount = len(msglist)
        msgrandom = random.randrange(0, msgcount)
        if usedlist is not None:
            while msgrandom in usedlist:
                msgrandom = random.randrange(0, msgcount)
            usedlist.append(msgrandom)
        return msglist[msgrandom]
    else:
        return None


def random_user(config, usedlist=None):
    userlist = config['users']
    usercount = len(userlist)
    userrandom = random.randrange(0, usercount)
    if usedlist is not None:
        while userrandom in usedlist:
            userrandom = random.randrange(0, usercount)
        usedlist.append(userrandom)
    return userlist[userrandom]


def listusers(config):
    userlist = config['users']
    digitcount = len(str(len(userlist)))
    userid = 0
    for user in userlist:
        print("#%s: %s, %s" % (str(userid).zfill(digitcount), user['nickname'], user['fullname']))
        userid += 1


def listtopics(config):
    for topicfile in glob.glob("messages/*.txt"):
        m = re.search('/(.*).txt', topicfile)
        topic = m.group(1)
        topic_content = read_message_file(topic)
        print("%s - %d lines" % (topic, len(topic_content)))


def register(config):
    userlist = config['users']
    for user in userlist:
        if 'registered' not in user:
            print("register: %s" % (user))
            r = accounts.register(config['server'],
                                  data={'nickname': user['nickname'], 'password': user['password'],
                                        'confirm': user['password'], 'fullname': user['fullname']})
            print(r)
            user['registered'] = True
    return config


def tweet(config, params):
    if len(params) > 1:
        user = parse_user(config, params[0])
        message = parse_message(config, params[1])
    else:
        user = config['users'][0]
        message = parse_message(config, params[0])

    print("%s -> %s" % (user, message))
    r = statuses.update(config['server'], data={'status': message}, auth=(user['nickname'], user['password']))
    print(r)


def mtweet(config, params):
    tweetcount = int(params[0])
    message = params[1]
    usedusers = [] if get_users_count(config) > tweetcount else None
    usedmsgs = [] if get_messages_count(config, message[1:]) > tweetcount else None

    for i in range(0, tweetcount):
        usr = random_user(config, usedlist=usedusers)
        msg = parse_message(config, message, usedmessages=usedmsgs)

        print("%s: %s -> %s" % (i, usr, msg))
        r = statuses.update(config['server'], data={'status': msg}, auth=(usr['nickname'], usr['password']))
        print(r)


def reply(config, params):
    if len(params) > 2:
        user = parse_user(config, params[0])
        replyto = params[1]
        message = parse_message(config, params[2])
    else:
        user = config['users'][0]
        replyto = params[0]
        message = parse_message(config, params[1])

    print("%s - %s -> %s" % (user, replyto, message))
    r = statuses.update(config['server'],
                        data={'in_reply_to_status_id': replyto, 'status': message},
                        auth=(user['nickname'], user['password']))
    print(r)


def mreply(config, params):
    replycount = int(params[0])
    replyto = params[1]
    message = params[2]
    usedusers = [] if get_users_count(config) > replycount else None
    usedmsgs = [] if get_messages_count(config, message[1:]) > replycount else None

    for i in range(0, replycount):
        usr = random_user(config, usedlist=usedusers)
        msg = parse_message(config, message, usedmessages=usedmsgs)

        print("%s: %s - %s -> %s" % (i, usr, replyto, msg))
        r = statuses.update(config['server'],
                            data={'in_reply_to_status_id': replyto, 'status': msg},
                            auth=(usr['nickname'], usr['password']))
        print(r)


def like(config, params):
    if len(params) > 1:
        user = parse_user(config, params[0])
        messageid = params[1]
    else:
        user = config['users'][0]
        messageid = params[0]

    print("%s -> %s" % (user, messageid))
    r = statuses.favorite(config['server'], messageid, auth=(user['nickname'], user['password']))
    print(r)


def mlike(config, params):
    likecount = int(params[0])
    messageid = params[1]
    usedusers = [] if get_users_count(config) > likecount else None

    for i in range(0, likecount):
        usr = random_user(config, usedlist=usedusers)

        print("%s: %s -> %s" % (i, usr, messageid))
        r = statuses.favorite(config['server'], messageid, auth=(usr['nickname'], usr['password']))
        print(r)


def rt(config, params):
    if len(params) > 1:
        user = parse_user(config, params[0])
        messageid = params[1]
    else:
        user = config['users'][0]
        messageid = params[0]

    print("%s -> %s" % (user, messageid))
    r = statuses.repeat(config['server'], messageid, auth=(user['nickname'], user['password']))
    print(r)


def mrt(config, params):
    likecount = int(params[0])
    messageid = params[1]
    usedusers = [] if get_users_count(config) > likecount else None

    for i in range(0, likecount):
        usr = random_user(config, usedlist=usedusers)

        print("%s: %s -> %s" % (i, usr, messageid))
        r = statuses.repeat(config['server'], messageid, auth=(usr['nickname'], usr['password']))
        print(r)


def follow(config, params):
    if len(params) > 1:
        user = parse_user(config, params[0])
        followuser = params[1]
    else:
        user = config['users'][0]
        followuser = params[0]

    print("%s -> %s" % (user, followuser))
    r = friendships.create(config['server'],
                           data={'screen_name': followuser},
                           auth=(user['nickname'], user['password']))
    print(r)


def mfollow(config, params):
    followcount = int(params[0])
    followuser = params[1]
    usedusers = [] if get_users_count(config) > followcount else None

    for i in range(0, followcount):
        usr = random_user(config, usedlist=usedusers)

        print("%s: %s -> %s" % (i, usr, followuser))
        r = friendships.create(config['server'],
                               data={'screen_name': followuser},
                               auth=(usr['nickname'], usr['password']))
        print(r)


def dm(config, params):
    if len(params) > 2:
        user = parse_user(config, params[0])
        sendto = params[1]
        message = params[2]
    else:
        user = config['users'][0]
        sendto = params[0]
        message = params[1]

    msg = parse_message(config, message)

    print("%s - %s -> %s" % (user, sendto, msg))
    r = direct_messages.new(config['server'],
                            data={'screen_name': sendto, 'text': msg},
                            auth=(user['nickname'], user['password']))
    print(r)


def mdm(config, params):
    replycount = int(params[0])
    sendto = params[1]
    message = params[2]
    usedusers = [] if get_users_count(config) > replycount else None
    usedmsgs = [] if get_messages_count(config, message[1:]) > replycount else None

    for i in range(0, replycount):
        usr = random_user(config, usedlist=usedusers)
        msg = parse_message(config, message, usedmessages=usedmsgs)

        print("%s: %s - %s -> %s" % (i, usr, sendto, msg))
        r = direct_messages.new(config['server'],
                                data={'screen_name': sendto, 'text': msg},
                                auth=(usr['nickname'], usr['password']))
        print(r)


def main():
    config = read_config()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'listusers':
            listusers(config)
        elif cmd == 'listtopics':
            listtopics(config)
        elif cmd == 'register':
            config = register(config)
            write_config(config)
        elif cmd == 'tweet':
            tweet(config, sys.argv[2:])
        elif cmd == 'mtweet':
            mtweet(config, sys.argv[2:])
        elif cmd == 'reply':
            reply(config, sys.argv[2:])
        elif cmd == 'mreply':
            mreply(config, sys.argv[2:])
        elif cmd == 'like':
            like(config, sys.argv[2:])
        elif cmd == 'mlike':
            mlike(config, sys.argv[2:])
        elif cmd == 'follow':
            follow(config, sys.argv[2:])
        elif cmd == 'mfollow':
            mfollow(config, sys.argv[2:])
        elif cmd == 'dm':
            dm(config, sys.argv[2:])
        elif cmd == 'mdm':
            mdm(config, sys.argv[2:])
        elif cmd == 'rt':
            rt(config, sys.argv[2:])
        elif cmd == 'mrt':
            mrt(config, sys.argv[2:])
        else:
            usage()
    else:
        usage()


if __name__ == "__main__":
    main()
