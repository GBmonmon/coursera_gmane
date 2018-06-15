import time
import sqlite3
import zlib

conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

howmany = int(input('how many: '))

senders = dict()
cur.execute('SELECT id, sender FROM Senders')
for message_row in cur:
    senders[message_row[0]] = message_row[1]

subjects = dict()
cur.execute('SELECT id, subject FROM Subjects')
for message_row in cur:
    subjects[message_row[0]] = message_row[1]

messages = dict()
cur.execute('SELECT id, guid, sender_id, subject_id, sent_at FROM Messages')
for message_row in cur:
    messages[message_row[0]] = (message_row[1],message_row[2],message_row[3],message_row[4])

print("Loaded messages=",len(messages),"subjects=",len(subjects),"senders=",len(senders))


sendcounts = dict()
sendorgs = dict()

for message_id, message in list(messages.items()):
    sender = message[1]
    sendcounts[sender] = sendcounts.get(sender,0)+1
    pieces = senders[sender].split('@')
    if len(pieces) != 2: continue
    dns = pieces[1]
    sendorgs[dns] = sendorgs.get(dns,0)+1

x = sorted(sendcounts,key = sendcounts.get,reverse=True)
#print(type(x))

#print(senders,'=======')
#print(sendcounts,'=======')
print('')
print('Top',howmany,'Email list participants')
for k in x[:howmany]:
    print(senders[k], sendcounts[k])
    if sendcounts[k] < 10 : break


x = sorted(sendorgs, key=sendorgs.get, reverse=True)
#print(sendorgs,'======')
#print(x)
print('')
print('Top',howmany,'Email list organizations')
for k in x[:howmany]:
    print(k, sendorgs[k])
    if sendorgs[k] < 10 : break
