# twitter-timelines-v2
Timeline Crawler for Twitter API v2

### Steps to run:
- Install pyyaml, tweepy libraries using pip command 
- Configure config.yaml file
    - Add bearer_token for access
    - Add either valid user_id or username and output filename
    - Configure required fields in tweet_fileds attribute
- Run timeline_client to get the user timeline in output file
