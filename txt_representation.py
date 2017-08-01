import numpy as np

# power = 1 imply that we select keywords that are overrepresented in clusters
# power = 2 imply that we select keywords that are the most dependent of the clusters
#  (in this case it is absolutely necessary to attribute a score to each keywords in order
#  to know weither the keyword is over-represented or under-represented in the cluster)
power = 2
def independence_test(matrix_pr_inter, matrix_pr_prod):
    """:return the matrix ( P(w and c)-p(w)p(c) )^2 : measure the dependence between a word and a cluster"""
    return np.power(matrix_pr_inter-matrix_pr_prod, power)

#### compute the frequency of a cluster or a word inside the corpus ####
def prob_clusters(labels, number_of_clusters):
    """:return the frequency of each cluster"""
    prob_cluster = []
    for label in range(0,number_of_clusters):
        s = np.sum(labels == label)
        prob_cluster.append(s)
    prob_cluster = np.array(prob_cluster).astype('float')
    to_round_numbers = np.vectorize(round)
    res = prob_cluster/len(labels)

    return to_round_numbers(res, 2)

def prob_words(matrix_count):
    """:return the frequency of each word"""
    matrix_count = matrix_count.astype('float')
    return np.sum(matrix_count, axis=0)/np.sum(matrix_count)

def matrix_prob_product(prob_cluster, prob_words):
    """:return the matrix of (P(cluster=line)*P(word=column))"""
    # nbr of cluster
    n_c = prob_cluster.shape[0]
    # nbr of words in the corpus
    n_w = prob_words.shape[0]
    one = np.ones([n_c, n_w])
    result = np.dot(one,np.diag(prob_words))
    result = np.dot(np.diag(prob_cluster), result)
    return result
########################################################################

#### compute P(w / c) ####
def matrix_prob_cond_word_in_cluster(matrix_count, labels, number_of_clusters):
    """:return the matrix : (P( col=word / line=cluster ))"""
    result = np.ones([number_of_clusters, matrix_count.shape[1]])
    for c in range(0, number_of_clusters):
        idx_of_cluster = (labels == c)
        idx_of_cluster = np.nonzero(idx_of_cluster)
        matrix_cluster = matrix_count[idx_of_cluster].astype('float')
        line_cluster = prob_cond_word_in_cluster(matrix_cluster)
        result[c, :] = line_cluster
    return result

def prob_cond_word_in_cluster(matrix_cluster):
    """:return the conditional probabilities of words inside the cluster represented by 'matrix_cluster'"""
    matrix_cluster = matrix_cluster.astype('float')
    return np.sum(matrix_cluster, axis=0)/np.sum(matrix_cluster)
###########################

#### compute P(w and c) ####
# A renommer
def prob_cluster_AND_word(matrix_count, labels, cluster, number_of_clusters):
    """return the conditional probabilities of the words inside the cluster named 'cluster' """
    idx_of_cluster = (labels == cluster)
    idx_of_cluster = np.nonzero(idx_of_cluster)
    matrix_cluster = matrix_count[idx_of_cluster].astype('float')
    pr_cond_word_in_cluster = prob_cond_word_in_cluster(matrix_cluster)
    prob_cluster = prob_clusters(labels, number_of_clusters)[cluster]
    return prob_cluster * pr_cond_word_in_cluster

def prob_clusters_AND_word(matrix_count, labels, number_of_clusters):
    """return the matrix : (P(l=cluster AND c=word))"""
    result=np.ones([number_of_clusters, matrix_count.shape[1]])
    for c in range(0,number_of_clusters):
        line_cluster=prob_cluster_AND_word(matrix_count, labels, c, number_of_clusters)
        result[c, :]=line_cluster
    return result
#############################

####
def idx_to_vocab(vocab, matrix_of_indexes):
    """give the words associated with each clusters"""
    matrix_of_indexes=matrix_of_indexes.astype('int')
    return vocab[matrix_of_indexes]

def keyword_score(matrix_count, labels, number_of_clusters, matrix_cluster_kwords):
    """for each cluster, give a score for each word that describe the cluster (0: the word is sub-respresented inside the cluster, 1: sur-represented inside the cluster)"""
    # for each cluster, compute the conditional probabilities of the words
    pr_cond = matrix_prob_cond_word_in_cluster(matrix_count, labels, number_of_clusters)
    # matrix_cluster_kwords is a matrix : nbr_of_clusters*nbr_of_keywords(that will describe the cluster)
    nbr_of_keywords = matrix_cluster_kwords.shape[1]
    # for each cluster, compute the score of the keywords := P(w/C) / sum(P(w/c), c=1...nbr_of_clusters)
    matrix_cluster_scoreOFkwords = np.ones([number_of_clusters, nbr_of_keywords])
    for c in range(number_of_clusters):
        col = np.array(matrix_cluster_kwords[c, :]).astype('int')
        s = np.sum(pr_cond[:, col], axis=0)
        matrix_cluster_scoreOFkwords[c, ] = pr_cond[c, col]/s

    to_round_numbers = np.vectorize(round)
    return to_round_numbers(matrix_cluster_scoreOFkwords, 3)


#*********************************************************#
class Representation:
    def __init__(self, processed_texts, clusters, nbr_of_keywords):
        n_clter = clusters.nbr_clusters
        matrix_count = processed_texts.features # processed_texts.matrix_count
        labels = clusters.labels
        vocabulary = np.array(processed_texts.vocabulary)

        pr_w = prob_words(matrix_count)

        # compute the weight of each clusters
        pr_c = prob_clusters(labels, n_clter)
        # compute the probability of (cluster AND word) for each cluster and for each word
        pr_w_and_c = prob_clusters_AND_word(matrix_count, labels, n_clter)
        # compute the quantity of ( P(c)*P(w) ) for each cluster and for each word
        mat_pr_prod = matrix_prob_product(pr_c, pr_w)
        # compute the independence test, the higher the number the more dependent
        measure_of_independence = independence_test(pr_w_and_c, mat_pr_prod)
        # for each cluster, compute the index of the more dependent word
        idx_cluster_kwords = np.ones([n_clter, nbr_of_keywords])
        for c in range(0, n_clter):
            idx_cluster_kwords[c, :] = np.argsort(measure_of_independence[c, :])[-nbr_of_keywords:]
        # for each cluster, give a score for each word that describe the cluster (0: the word is sub-respresented inside the cluster, 1: sur-represented inside the cluster)
        matrix_cluster_scoreOFkwords = keyword_score(matrix_count,
                                                     labels, n_clter, idx_cluster_kwords)
        # give the words associated with each clusters
        keywords_of_clusters = idx_to_vocab(vocabulary, idx_cluster_kwords)

        self.scores = matrix_cluster_scoreOFkwords
        self.keywords = keywords_of_clusters
        self.prob_clusters = pr_c
        self.value_of_representation = self.value()

    def value(self):
        """Pour l'instant c'est de la merde """
        scores = self.scores
        value = np.mean(1+np.log(scores + 0.0001)*scores*np.e, axis=0)

        to_round_numbers = np.vectorize(round)
        return to_round_numbers(value, 3)


    def display(self):
        keywords = self.keywords
        n_c, n_k = keywords.shape
        str_to_display = ""
        for i in range(0, n_c):
            str_to_display += 'Cluster(' + str(i) + ')'+\
                              ' freq = ' + self.prob_clusters[i].astype('str') +\
                              ' score_of_rep = '  + self.value_of_representation[i].astype('str') + ' '
            for j in range(0, n_k):
                str_to_display += ' : ' + keywords[i, j] \
                                  + ': ' + str(self.scores[i, j]) + ' | '
            str_to_display += '\n'
        print(str_to_display)


