from multiprocessing import AuthenticationError
from os import access
import yaml
import tweepy


def load_config():
    config_dict = dict()
    with open(r'config.yaml') as file:
        config_dict = yaml.full_load(file)

    return config_dict


def authenticate_user(config):
    auth = tweepy.OAuthHandler(consumer_key=config["consumer_key"],
                               consumer_secret=config["consumer_secret"])

    auth.set_access_token(config["access_token"],
                          config["access_token_secret"])

    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Verify Authentication
    try:
        api.verify_credentials()
        print("User is Authenticated")
    except:
        raise AuthenticationError(
            "Authentication Failed. Please set the keys in config.yaml file")

    return api


def main():

    config = load_config()
    api = authenticate_user(config)


if __name__ == '__main__':
    print('Application Started ...........')
    main()
