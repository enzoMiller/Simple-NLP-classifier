import urllib
from lxml import etree
import string
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np
from stemming.porter2 import stem

### functions to process texts ###
def text_to_cleanText(text):
    '''input: a string(like a summary)
        output: a string cleaned'''
    text = re.sub("[^a-zA-Z]", " ", text)
    words = text.lower().split()
    stop_words = set(stopwords.words("english"))#removing of useless words like "the", "up",etc
    words = [w for w in words if not w in stop_words]
    words = map(stem,words)#stemming of the words
    return " ".join(words)
##
def textList_to_matrix_count_vocab(text_list):
    '''input: a list of raw strings
        the strings are cleaned
        then transformed in features
        output: a list of vectors (one for each text)'''
    clean_text=map(text_to_cleanText, text_list)
    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=5000)
    matrix_count = vectorizer.fit_transform(clean_text).toarray()
    return {'matrix_count': matrix_count, 'vocabulary': vectorizer.get_feature_names()}
##
def extract_summary_title_category(output_list_item):
    '''useful with map'''
    return output_list_item['summary'] \
           +output_list_item['title'] \
           +output_list_item['category'] + output_list_item['category']

##############################

### beggining of the class 'Processing'###
class Processing:
    def __init__(self, list_title_urlPDF_summary):
        self.matrix_count, self.vocabulary = self.build_matrix_count_and_vocab(
            list_title_urlPDF_summary)
        self.features = self.build_features()

### Building 'matrix_count' and 'vocabulary' ###

    def build_matrix_count_and_vocab(self, list_title_urlPDF_summary):
        """fct de sortie du fichier, avant clustering"""
        list_summaries = map(extract_summary_title_category, list_title_urlPDF_summary)
        matrix_count_vocab = textList_to_matrix_count_vocab(list_summaries)

        return matrix_count_vocab['matrix_count'], matrix_count_vocab['vocabulary']

#############################

### Building 'features', feature enginering will happen here ###
    def tf(self):
        return self.matrix_count.astype(float)/self.matrix_count.sum(axis=1)[:, None]
##
    def idf(self):
        '''input: each line of matrix_count is associated with a document, each column with a word
            output:an array of scores for each word. The more a word is dicriminatory the higher the score is  '''
        bool_matrix = (self.matrix_count != 0)
        column_count = np.sum(bool_matrix, axis=0)
        number_of_doc = float((np.array(self.matrix_count)).shape[0])
        return np.log(number_of_doc / column_count)
##
    def build_features(self):
        idf_word = self.idf()
        tf_word_doc = self.tf()
        features = idf_word * tf_word_doc
        features = normalize(features, axis=1, norm='l2')
        return features
#######################