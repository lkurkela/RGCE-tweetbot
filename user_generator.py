from faker import Faker
from transliterate import translit, get_available_language_codes

seed = [('en_US',100,None),('en_GB',50,None),('fi_FI',50,None),('et_EE',50,None),('de_DE',100,None),('sv_SE',50,None),('uk_UA',20,'ru'),('ru_RU',80,'ru')]

def process(uid, name, transliterate):
    if transliterate is None:
        username = str(name.split(' ')[0].lower() + str(uid).zfill(5)).replace('\'','').replace('.','').replace('-','')
        userDict = {'nickname': username, 'fullname': name, 'password': 'trolli'}
    else:
        firstname = translit(name.split(' ')[0].lower(), reversed=True)
        username = str(firstname + str(uid).zfill(5)).replace('\'','').replace('.','').replace('-','')
        userDict = {'nickname': username, 'fullname': translit(name, reversed=True).replace('\'',''), 'password': 'trolli'}

    print ("%s" % (userDict))

uid = 0

for x in seed:
    count = x[1]
    locale = x[0]
    faker = Faker(locale)
    for y in range(0,count):
        transliterate = x[2]
        process(uid, faker.name(), transliterate)
        uid += 1

