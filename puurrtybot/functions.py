from sklearn.feature_extraction.text import TfidfVectorizer
from sparse_dot_topn import awesome_cossim_topn
import multiprocessing, pickle, random, datetime, pickle, pandas as pd, numpy as np, puurrtybot
from PIL import Image
import puurrtybot, puurrtybot.assets.get_functions as agf


def ordinal(n: int) -> str:
    return f"{n:d}{'tsnrhtdd'[(n//10%10!=1)*(n%10<4)*n%10::4]}"


def time_to_timestamp(timeformat):
    return int(datetime.datetime.strptime(timeformat,"%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp())


def timestamp_to_utcdatetime(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp)


def timestamp_to_utctime(timestamp):
    return str(datetime.datetime.utcfromtimestamp(timestamp))


def get_utc_time():
    return int(datetime.datetime.now(datetime.timezone.utc).timestamp())


def get_formatted_date(date):
    date = timestamp_to_utcdatetime(date)
    return date.strftime(f'{ordinal(date.day)} %B %Y at %H:%m UTC')


def get_random_between(start: int = 1, end: int = 100):
    return str(random.choice(list(range(start, end+1))))


def get_random_quantity():
    random_q = list(range(2_000_000, 2_999_999))
    return str(random.choice(random_q)/1_000_000)


class FastCandidateFinder(object):
    def __init__(self):
        self.assets = {agf.get_asset_name(asset):asset for asset in puurrtybot.ASSETS.keys()}
        self.ngram_size = 2        
        self.tfidf_vectorizer = None
        self.fit_vectorizer = None
        self.processes: int = multiprocessing.cpu_count() - 1


    def n_grams(self, string: str):
        string=f""" {string.strip().lower()} """
        return [''.join(n_gram) for n_gram in zip(*[string[i:] for i in range(self.ngram_size)])]
    

    def get_tfidf_vectorizer(self, data):
        self.tfidf_vectorizer = TfidfVectorizer(min_df=1, analyzer=self.n_grams)
        self.fit_vectorizer = self.tfidf_vectorizer.fit(data)


    def get_tfidf(self, data):
        return self.fit_vectorizer.transform(data)
    

    def load_tfidf(self, path: str):
        self.fit_vectorizer = pickle.load(open(path, 'rb'))


    def get_cossim(self, A, B, top_n, threshold):

        optional_kwargs = dict()
        if self.processes > 1:
            optional_kwargs = {
                'use_threads': True,
                'n_jobs': self.processes
            }
        return awesome_cossim_topn(A,B, top_n, threshold, **optional_kwargs)
    

def get_matches_list(matches) -> pd.DataFrame:
        non_zeros = matches.nonzero()
        sparserows = non_zeros[0]
        sparsecols = non_zeros[1]
        nr_matches = sparsecols.size
        master_side = np.empty([nr_matches], dtype=int)
        dupe_side = np.empty([nr_matches], dtype=int)
        similarity = np.zeros(nr_matches)

        for index in range(0, nr_matches):
            master_side[index] = sparserows[index]
            dupe_side[index] = sparsecols[index]
            similarity[index] = matches.data[index]

        matches_list = pd.DataFrame({'asset': master_side,
                                     'name': dupe_side,
                                     'similarity': similarity})
        return matches_list

    
def query_asset(search):
    try:
        fcf_matcher = FastCandidateFinder()
        assets_list = list(fcf_matcher.assets.keys())
        fcf_matcher.get_tfidf_vectorizer(data=assets_list)
        fcf_matcher.tfidf_vocabulary = fcf_matcher.assets.keys()

        tfidf_vectorizer = fcf_matcher.fit_vectorizer
        tfidf_matrix = fcf_matcher.get_tfidf(data=assets_list)
        fcf_matcher.fit_vectorizer = fcf_matcher.tfidf_vectorizer

        B = fcf_matcher.get_tfidf([search, search.lower()])
        A = tfidf_matrix 

        candidates = fcf_matcher.get_cossim(A=A, B=B.transpose(), top_n=10, threshold=0.5)
        match = int(get_matches_list(candidates).sort_values('similarity', ascending=False).iloc[0]['asset'])
        name = assets_list[match]
        asset_name = fcf_matcher.assets[name]
        return (name, asset_name)
    except IndexError:
        return (f"""{search}""", f"""Couldn't find a cat with that name, try another name.""")


def resize_image(img, basewidth=1200):
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((basewidth,hsize), Image.ANTIALIAS)