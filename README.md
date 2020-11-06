# Love Letter

Automatically send unique messages to someone special. 💘

## Planning

### Architecture

Persistent message storage + message sending service + controller + interface to add more messages

- Persistent storage: Database
- Message sending service: sms api
- Controller: AWS Lambda
- Interface to add more messages: Form on static site (Netlify site + Netlify form) with Netlify function w/ creds in env that submits message to dynamodb database

### Database Planning

_Picked AWS DynamoDB._

**Keep used and unused messages in different tables.** Instead of keeping all messages in one table, keep the used and unused messages in separate tables. Then, we don't have to scan the table to find unused messages. Instead, we can scan the unused table for the first ~10, which we know will all be unused, and can just pick one randomly of those ten.

**Only scan first ~30 messages in table when reading, they are all unused anyways.** Limit the result set to no more than 30. If unused messages are kept in their own table, then we know they are all unused, and we can just pick some randomly from there.

### Message Picking Algorithm

1. Scan 30 messages from unused message table.
1. Pick one randomly.
1. Add message to UsedTable
1. Delete message from UnusedTable

### DB Choice

**Winner**: AWS DynamoDB

Cheap enough, based on usage and not uptime. Like to stick with AWS for learning it as a tool that's commonly requested by other jobs.

#### AWS DocumentDB

Don't need structure of a relational database, document-style is good enough.

Estimates of [Amazon Document DB](https://aws.amazon.com/documentdb/pricing/) price:

```
On-demand instance type: db.t3.medium
Price/instance/hour consumed: $0.076
Instance/hour minumum billed duration: 10 minutes
Price/instance/hour @ 10 minute minimum billed duration: $0.076 / 6 = $0.013
10 minute billed instances/day = 3 (based on sending 3 messages a day)
Total monthly price = 3 * $0.013 * 30/days = $1.17/month
```

A complication with using DocumentDB would be that the instance has to be started before use and stopped after use to reduce instance/hour costs.

#### AWS DynamoDB

[Amazon DynamoDB](https://aws.amazon.com/dynamodb/) might be good, there's a free tier that allows 25GB storage, and 25KB read & write per day.

#### Google Sheets

Could keep used messages in one Google sheet tab, and unused ones in another.

#### Other DB Notes

Instead of having all messages in one part of the document db and searching through each message to find those that haven't been sent yet, unsent messages could be kept in one part and already sent messages kept in another. That way we can just reach in to either part and grab the first message we see instead of worrying about whether or not it has been sent already.

There is an educational and job skills benefit to developing with just AWS resources, instead of Netlify and Google Sheets.

### Frontend Choice

This frontend would be what is used to add more messages to be sent in the future.

#### Netlify Forms

Host a static site with Netlify that can collect 100 form submissions per month. A Netlify function could recieve these forms and insert them in the DB. To get around the 100 submissions/month limit, multiple messages could be submit in each form.
