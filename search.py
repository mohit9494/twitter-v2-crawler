import yaml
import tweepy
import json


def load_config():
    config_dict = dict()
    with open(r'config.yaml') as file:
        config_dict = yaml.full_load(file)

    return config_dict


def main():
    config = load_config()
    print('Getting User TimeLines ....')

    client = tweepy.Client(
        bearer_token=config['bearer_token'])

    if config['search']['user_name']:
        username = config['search']['user_name']
    elif config['search']['user_id']:
        username = client.get_user(
            id=config['search']['user_id']).data.username
    else:
        raise Exception("***** Either Provide user_name or user_id parameter")

    query = f'from:{username}'

    start_time = config['search']['start_time']
    end_time = config['search']['end_time']

    if (start_time == None) or (end_time == None):
        fullsearch = False
    else:
        fullsearch = True

    tweet_count = config['search']['client']['tweet_count']
    print(tweet_count)

    tweets = None

    if fullsearch:
        tweets = client.search_all_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],
                                          start_time=start_time,
                                          end_time=end_time, max_results=tweet_count)
    else:
        tweets = tweepy.Paginator(client.search_recent_tweets, query=query,
                                  tweet_fields=['context_annotations', 'created_at'], max_results=20).flatten(
            limit=tweet_count)

        # // getusertweets -

    cols = ['attachments', 'author_id', 'context_annotations', 'conversation_id', 'created_at', 'data', 'entities',
            'geo', 'get', 'id', 'in_reply_to_user_id', 'items', 'keys', 'lang',
            'non_public_metrics', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics',
            'referenced_tweets', 'reply_settings', 'source', 'text', 'values', 'withheld']

    result = []
    for i, tweet in enumerate(tweets):

        temp_dict = {}
        for col in cols:
            temp_dict[col] = tweet[col]

        # with open('data.json', 'a+', encoding='utf-8') as f:
        #     json.dump(temp_dict, f, ensure_ascii=False, indent=4, default=str)

        json_str = json.dumps(
            temp_dict, sort_keys=True, default=str)

        result.append(json_str)

    print(result)

    # Writing result to a file


if __name__ == '__main__':
    main()
