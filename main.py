from url_to_text import Url_to_texts
from processing import Processing
from clustering import Clustering
from txt_representation import Representation
from html import html_cluster
import time

nbr_of_doc = 200
nbr_of_clusters = 3
nbr_of_keywords = 10
topic = "sport"
topic2 = "sport"
topic3 = "sport"
url='http://export.arxiv.org/api/query?search_query=all:{topic}+OR+all:' \
    '{topic2}+OR+all:{topic3}&max_results={nbr_of_doc}'.format(nbr_of_doc=nbr_of_doc,
                                                               topic=topic,
                                                               topic2=topic2,
                                                               topic3=topic3)

start_time1 = time.time()
print(url)
txt = Url_to_texts(url)
print(" %s in total for parsing the API " % (time.time() - start_time1))

start_time2 = time.time()
processed_txt = Processing(txt.list_title_urlPDF_summary_category)
print(" %s in total for processing " % (time.time() - start_time2))

start_time3 = time.time()
cluster = Clustering(processed_txt.features, nbr_of_clusters)
print(" %s in total for clustering " % (time.time() - start_time3))

start_time4 = time.time()
representation = Representation(processed_txt, cluster, nbr_of_keywords)
print(" %s in total for representing " % (time.time() - start_time4))

print(" %s in total " % (time.time() - start_time1))

representation.display()
html_cluster(txt.list_title_urlPDF_summary_category, cluster.labels, nbr_of_clusters)


