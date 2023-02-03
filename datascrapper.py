import snscrape.modules.twitter as sntwitter
import pandas as pd


class DataScrapper():

    def __init__(self, victim, n_twitts=100) -> None:
        self.victim = victim
        self.n_twitts = n_twitts
        self.columns = ['Username', 'Date', 'Replies',
                        'RTs', 'Likes', 'Reply_to', 'Mentions', 'Tweets']

    def get_query(self, query, limit=None):
        if limit is None:
            limit = self.n_twitts
        results = []
        for j, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if j > limit:
                break
            results.append([tweet.user.username, tweet.date, tweet.replyCount, tweet.retweetCount, tweet.likeCount,
                            tweet.inReplyToUser, tweet.mentionedUsers, tweet.rawContent])
        return pd.DataFrame(results, columns=self.columns)

    # devuelve las últimas menciones a victim - sin tener en cuenta el emisor

    def get_all_mentions(self, limit=None):
        # respuestas directas y menciones
        q1 = f'to:{self.victim}'
        q2 = f'@{self.victim}'
        return pd.concat([self.get_query(q1, limit), self.get_query(q2, limit)], axis=0)

    # get_mentions_from -> devuelve los tweets donde user_from responde o menciona a self.victim

    def get_mentions_from(self, user_from, limit=None):
        # respuestas directas y menciones
        q1 = f'from:{user_from} to:{self.victim}'
        q2 = f'@{self.victim} from:{user_from}'
        return pd.concat([self.get_query(q1, limit), self.get_query(q2, limit)], axis=0)

    # get_mentions_to -> devuelve los tweets donde self.victim menciona o responde a user_from
    def get_mentions_to(self, user_to, limit=None):
        # menciones directas y laterales
        q1 = f'from:{self.victim} to:{user_to}'
        q2 = f'@{user_to} from:{self.victim}'
        return pd.concat([self.get_query(q1, limit), self.get_query(q2, limit)], axis=0)

    # get_user -> Devuelve instancia User (snstwitter class)
    def get_user(self, usr):
        user = sntwitter.TwitterUserScraper(usr).entity

    # SCRAPPING LAST TWEETS OF AND TO VICTIM

    # get_inputs -> devuelve los últimos tweets dirigidos a self.victim
    def get_inputs(self, limit=None):
        q = f'to:{self.victim}'
        return self.get_query(q, limit)

    # get_outputs -> devuelve los últimos n_twitts de self.victim
    def get_outputs(self):
        q = f'from:{self.victim}'
        return self.get_query(q)
