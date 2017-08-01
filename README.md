# NLP-classifier

This code aims at classifying papers from arxiv. 
To do so, we do the following : 
* We call the arxiv API `<https://arxiv.org/help/api/index> `
* We clusters the results given by the API, in an unsupervised manner
* We attribute a list of keywords to each clusters to know what is inside them


## Finding relevant keywords for each clusters 

Once the clusters are done, we give each clusters `n` keywords (`n`we is a parameter you can find in main.py). How do we choose these latters? We do the following :

for each cluster :
* then for each clusters we choose `n` word for which the **( P(word  AND cluster) - P(word).P(cluster) )^2** is maximal
* So at that point we have words that are correlated to the clusters but we don't know whether they are so because they are over-represented or under-respresented. 
* That's why we need an another metric. We then compute the following : **P( word / cluster ) / ( sumOverClusters{ P( word / cluster_i ) })** . If that quantity is 1, that means that our cluster is the only one that have this word  in its corpus. If it's zero, that means the cluster doesn't have at all that word. 

## Output
### Output in the console 
Below is what we print in the console; In that example the request was `sport` the number of clusters 3 and the total number of articles 200 :
 
* **Cluster(0)** `freq = 0.74 score_of_rep = 0.73`  : visual: 0.033 |  : tempor: 0.129 |  : learn: 0.127 |  : rank: 0.908 |  : spatio: 0.009 |  : sky: 0.0 |  : object: 0.06 |  : action: 0.048 |  : polar: 0.0 |  : video: 0.021 | 
* **Cluster(1)** `freq = 0.06 score_of_rep = 0.761`  : background: 0.925 |  : cosmolog: 1.0 |  : ghz: 0.908 |  : station: 0.994 |  : instrument: 0.983 |  : emiss: 0.995 |  : microwav: 1.0 |  : phastro: 0.981 |  : sky: 1.0 |  : polar: 1.0 | 
* **Cluster(2)** `freq = 0.2 score_of_rep = 0.654`  : track: 0.879 |  : annot: 1.0 |  : visual: 0.967 |  : tempor: 0.871 |  : learn: 0.873 |  : approach: 0.843 |  : spatio: 0.991 |  : object: 0.808 |  : action: 0.952 |  : video: 0.979 | 

`Freq` represents the proportion of articles in the cluster. `score_of_rep` should be a metric related to how well the keywords represents the clusters; right now I'm not happy with it :(. The rest is the list of keywords that represents the clusters, with their scores which a number between 0 and 1 (cf the 3rd point in the `Finding relevant keywords for each clusters` section)

### Output : html files
To see an example of the results, you can look at the file `O.html`, `1.html` and `3.html` who were obtained by calling the API with the request "sport". As shown by the output result in the console, the `Cluster(1)` is about an experiment about polarisation whose name was Sport.


## Depedencies 