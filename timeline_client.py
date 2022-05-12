import yaml
import tweepy
import json


# Loading Initial config from config.yaml file
def load_config():
    config_dict = dict()
    with open(r'config.yaml') as file:
        config_dict = yaml.full_load(file)

    return config_dict


# Main Function to get the user timeline from Twitter
def fetch_tweets(user_id, client, config):
    count = 0
    print("******* Inside fetch Tweets")
    next_token = ''
    tweets = ''

    # Attributes required from the tweet
    tweet_fields = config['timeline']['tweet_fields']
    output_file = config['timeline']['output_file']

    tweets = client.get_users_tweets(id=user_id,
                                     tweet_fields=tweet_fields, max_results=100)

    # get Next Token from Metadata
    next_token = tweets.meta.get('next_token')

    # Using Pagination: while next_token is available in the metadata, get the tweets in the batch of max_results (100)
    while next_token is not None:
        tweets = client.get_users_tweets(id=user_id, tweet_fields=tweet_fields, max_results=100,
                                         pagination_token=next_token)

        if tweets.data is None:
            print('******** Null Response is Received. Exit From process *******')
            break
        else:
            for tweet in tweets.data:
                count = count + 1

                # Creating temp directory of fields and values before dumping in Json
                temp_dict = {}
                for col in tweet_fields:
                    temp_dict[col] = tweet[col]

                # Writing the result in OutPut File
                with open(output_file, 'a', encoding='utf8') as json_file:
                    json_file.write(json.dumps(temp_dict, ensure_ascii=False,
                                               sort_keys=True, default=str))
                    json_file.write(',')
                    json_file.write('\n')

        # Just for the verification purpose
        print("Tweets Len ====> ", len(tweets.data))
        print("Tweet Count ====> ", count)

        # Getting next token
        next_token = tweets.meta.get('next_token')
        print("Next Token =====> ", next_token)


# Getting UserId from Config File
# Either userid or username can be mentioned in config.yaml
def get_userid(client, config):
    if config['timeline']['user_id']:
        user_id = config['timeline']['user_id']
    elif config['timeline']['username']:
        username = config['timeline']['username']
        user_id = client.get_user(username=username)[0].id
    else:
        raise Exception("***** Either Provide user_name or user_id parameter")

    return user_id


def main():
    print("Timeline Client has started ......")
    config = load_config()

    # Initializing the tweepy Client using bearer_token
    client = tweepy.Client(
        bearer_token=config['bearer_token'])

    # Getting the userId
    user_id = get_userid(client=client, config=config)

    # Fetching the tweets and storing it in the form of Json
    fetch_tweets(user_id=user_id, client=client, config=config)


if __name__ == '__main__':
    main()
