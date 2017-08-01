####html functions
import numpy as np

def html_title(title, url):
    return "<h2><a href="+url+">"+title+"</a></h2>"

def html_summary(summary):
    return "<p>"+summary+"</p>"

def html_entry(title, summary):
    return title + "\n" + summary + "\n"


def dict_to_html(vect_dict, html_tite):
    '''create an html file outputting the results contained in vect_dict'''
    html_document = open(html_tite, 'w')
    n = len(vect_dict)
    message=""
    for i in range(0, n, 1):
        summary = html_summary(vect_dict[i]["summary"])
        title=html_title(vect_dict[i]["title"],vect_dict[i]["url_pdf"] )
        entry=html_entry(title, summary)
        message+=entry
    html_document.write(message.encode('ascii', 'ignore'))
    html_document.close()

def html_cluster(vect_dict,labels, numbers_of_clusters ):
    for c in range(0, numbers_of_clusters):
        idx_of_cluster = (labels == c)
        idx_of_cluster = np.nonzero(idx_of_cluster)
        #print(vect_dict[[1,2]])
        vect_dict=np.array(vect_dict)
        cluster = vect_dict[idx_of_cluster[0]]
        dict_to_html("cluster_" + cluster, str(c)+".html")

