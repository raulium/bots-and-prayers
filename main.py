#!/user/bin/env python
import evaluator
import string
import tweepy, random, feedparser, collections
from nltk.tag import pos_tag
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
from config import FEEDS
from config import NEG_PRETAGS, NEG_POSTTAGS, NEG_WORDS, POS_POSTTAGS, POS_PRETAGS, POS_WORDS


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# api.update_status("Hello world!")

def get_news_vector():
    src = random.choice(FEEDS)
    d = feedparser.parse(src)
    i = random.randint(0, len(d['entries'])-1)
    title = d['entries'][i]['title']
    summary = d['entries'][i]['summary']
    link = d['entries'][i]['link']

    return [title, summary, link]


def get_proper_nouns(input_string):
    tagged = pos_tag(input_string.split())
    return [word for word, pos in tagged if pos == 'NNP']


def sentiment(input_string):
    return evaluator.evaluate_sentence(input_string, evaluator.vocabulary)


def gen_post():
    d = []
    check = None
    while not check:
        d = get_news_vector()
        try:
            check = sentiment(d[0])
        except (ValueError, IndexError):
            continue
    t = get_proper_nouns(d[0]) + get_proper_nouns(d[1])
    counter = collections.Counter(t)
    topic = counter.most_common(1)[0][0]

    exclude = set(string.punctuation)
    topic = ''.join(ch for ch in topic if ch not in exclude)

    if check == 'NEG':
        tag1 = random.choice(NEG_PRETAGS) + topic
        tag2 = '#' + topic + random.choice(NEG_POSTTAGS)
        words = random.choice(NEG_WORDS)
    else:
        tag1 = random.choice(POS_PRETAGS) + topic
        tag2 = '#' + topic + random.choice(POS_POSTTAGS)
        nums = list()
        while len(nums) < 3:
            i = random.randint(0,len(POS_WORDS)-1)
            if i not in nums:
                nums.append(i)
        print nums
        words = '#blessed ' + POS_WORDS[nums[0]] + ' ' + POS_WORDS[nums[1]] + ' ' + POS_WORDS[nums[2]]

    return [words, tag1, tag2, d[2]]


def main():
    p = gen_post()
    post = ' '.join(p)
    api.update_status(post)

if __name__ == "__main__":
    main()