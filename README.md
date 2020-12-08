# Love Machine

Automatically send unique messages to someone special. 💘

## Todo

- [x] create `love_machine-used_messages` & `love_machine-unused_messages` AWS DynamoDB tables (2020-11-05)
- [x] access local dynamodb docker container w/ python (2020-11-14)
- [x] setup aws iam role for lambda `love_machine-manage-messages_iam-role` (2020-11-14)
  - will need to generate credentials for role I think
- [x] create UsedMessages AWS DynamoDB table (2020-11-05)
- [x] create UnusedMessages AWS DynamoDB table (2020-11-05)
- [x] write scripts for database setup & teardown (2020-11-21)
- should these go in a message model instead of a db model? Db doesn't really describe it.
- [x] create model for creating a message (2020-12-06)
- [x] create model for deleting a message (2020-12-06)
- [x] create model for moveUnusedMessageToUsed
- [x] create method for getting a random message (2020-12-08)
- [ ] create local function in lambda shape for sending an sms message (stub sms api)
  - _do not create an entire local openwhisk deployment for this_
  - <https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html>
  - just use whatever test script they provide for running the function with the correct parameter shape
- [ ] create local function in lambda shape for recieving a "new messages" form submission and adding it to the db
- [ ] figure out how to give lambda role with correct policies
  - already created role (above)
  - maybe have to generate credentials for role?
- [ ] try uploading & running lamda
- [ ] Fill out section "Free Data Transfer Limits"
  - Given the free tier limits on DynamoDB and how many messages I want to be able to pull over just one second, I should be able to figure out how long a message can be. For example, if I can only request 25 KB per second and want to pull 30 messages in one second without breaking that free tier speed limit, then each message can be at most 833 bytes (`25000 bytes / 30 messages = 833 bytes / message`).
  - The information I need: [dynamodb developer guide: data types](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html#limits-data-types)
- [ ] test out sms api outside code stuff
- [ ] implement sms api
- [ ] setup rule for triggering lambad on interval (use aws Cloud Watch) <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html>

### Improvements

- [ ] use asyncio module to perform remote actions asynchronously
  - could create used message and delete unused message at same time

## Planning

### Architecture

Persistent message storage + message sending service + controller + interface to add more messages.

- Message storage: DynamoDB
- Message sending controller: AWS Lambda + Trigger + SMS Api
- New message api: AWS Lambda exposed with https endpoint (takes a password)
- New message form: Netlify site + Netlify form + Netlify function

### Database Planning

_Picked AWS DynamoDB._

**Keep used and unused messages in different tables.** Instead of keeping all messages in one table, keep the used and unused messages in separate tables. Then, we don't have to scan the table to find unused messages. Instead, we can scan the unused table for the first ~10, which we know will all be unused, and can just pick one randomly of those ten.

**Only scan first ~30 messages in table when reading, they are all unused anyways.** Limit the result set to no more than 30. If unused messages are kept in their own table, then we know they are all unused, and we can just pick some randomly from there.

**DynamoDB Tables**:

- love_machine-unused_messages
- love_machine-used_messages

#### Data shape

```JSON
"unusedMessage": {
  "messageId": "jekidjklwer",
  "text": "Aren't you a spicy cucumber ;O",
  "createdAt": "2020-11-06T02:18:59.238Z"
}

"usedMessage": {
  "messageId": "jekidjklwer",
  "text": "Aren't you a spicy cucumber ;O",
  "createdAt": "2020-11-06T02:18:59.238Z",
  "sentAt": "2020-11-08T22:21:55.843Z"
}
```

#### Message Picking Algorithm

1. Scan 30 messages from unused message table.
1. Pick one randomly.
1. Add message to UsedTable
1. Delete message from UnusedTable

#### Running DB Locally

Use docker-compose to run file. After, you can use the aws cli to talk to it. `AWS_ACCESS_KEY_ID=123 AWS_SECRET_ACCESS_KEY=456 aws dynamodb list-tables --endpoint-url http://localhost:8000 --region oz` The two env vars for access key id and secret access key and the `--region` option just have to be defined, they can be whatever you want, but make sure they match the values in the .env file so that the app is using the same arbitrary values.

```bash
export AWS_ACCESS_KEY_ID=123
export AWS_SECRET_ACCESS_KEY=456
export AWS_DEFAULT_REGION=oz
aws dynamodb list-tables --endpoint-url http://localhost:8000
```

##### Database Setup

Use a python interpreter to run functions `up()` and `down()` in `db.py`. Up creates database tables, down deletes them.

#### Free Data Transfer Limits

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

[Amazon DynamoDB](https://aws.amazon.com/dynamodb/) might be good, there's a free tier that allows 25GB storage, and 25KB read & write per ~day~ second.

#### Google Sheets

Could keep used messages in one Google sheet tab, and unused ones in another.

#### Other DB Notes

Instead of having all messages in one part of the document db and searching through each message to find those that haven't been sent yet, unsent messages could be kept in one part and already sent messages kept in another. That way we can just reach in to either part and grab the first message we see instead of worrying about whether or not it has been sent already.

There is an educational and job skills benefit to developing with just AWS resources, instead of Netlify and Google Sheets.

### Frontend Choice

This frontend would be what is used to add more messages to be sent in the future.

#### Netlify Forms

Host a static site with Netlify that can collect 100 form submissions per month. A Netlify function could recieve these forms and insert them in the DB. To get around the 100 submissions/month limit, multiple messages could be submit in each form.
