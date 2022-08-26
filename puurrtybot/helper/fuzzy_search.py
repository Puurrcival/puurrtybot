import multiprocessing

from sklearn.feature_extraction.text import TfidfVectorizer
from sparse_dot_topn import awesome_cossim_topn
import pandas as pd, numpy as np

import puurrtybot.database.query as dq


class FastCandidateFinder(object):
    def __init__(self):
        self.assets = {asset.name:asset.asset_id for asset in dq.get_asset_all()}
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
        return None