# Love Letter

Automatically send unique messages to someone special. 💘

## Planning

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

Instead of having all messages in one part of the document db and searching through each message to find those that haven't been sent yet, unsent messages could be kept in one part and already sent messages kept in another. That way we can just reach in to either part and grab the first message we see instead of worrying about whether or not it has been sent already.
