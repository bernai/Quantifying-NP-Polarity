# Quantifying-NP-Polarity

# Quantifying NPs

This readme provides some useful information on the project and its requirements.

## Requirements

1. Change directory to this project and install modules defined in requirements.txt
    ```
    pip install -r requirements.txt
    ```
2. Download word embedding vectors (direct link) and uncompress both

    fasttext:
    [crawl-300d-2M-subword.zip](https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M-subword.zip)

    word2vec:
    [GoogleNews-vectors-negative300.bin.gz](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing)


3. put both unpacked files into *embedding_files* folder


## File Overview
```
📦quantifying-np-polarity
 ┣ 📂comparison_bbc .................................... files related to annotation/evaluation
 ┃ ┣ ...
 ┣ 📂embedding_files ................................... folder with word embedding vector files
 ┃ ┣ ...
 ┣ 📂gold_standard
 ┃ ┣ 📂model_savefiles ................................. savefiles of models created by "quantification.ipynb"
 ┃ ┃ ┣ 📜knn_model_ft.sav
 ┃ ┃ ┣ ...
 ┃ ┃ ┗ 📜svr_model_w.sav
 ┃ ┣ 📂rankings ........................................ rankings created by gold standard models
 ┃ ┃ ┣ 📂bbc_news
 ┃ ┃ ┣ 📂scl_nma
 ┃ ┣ 📂training_file
 ┃ ┃ ┗ 📜NRC-VAD-Lexicon.txt
 ┃ ┣ 📜output_kendall.txt
 ┃ ┗ 📜output_metrics.txt
 ┣ 📂silver_standard
 ┃ ┣ 📂lexicon  ........................................ lexicons for silver standard generation
 ┃ ┃ ┣ ...
 ┃ ┣ 📂model_savefiles ................................. savefiles of models created by "quantification_silver.ipynb"
 ┃ ┃ ┣ 📜knn_model_ft.sav
 ┃ ┃ ┣ ...
 ┃ ┃ ┗ 📜svr_model_w.sav
 ┃ ┣ 📂np_extraction
 ┃ ┃ ┣ 📂news
 ┃ ┃ ┃ ┗ 📜bbc_news_entertainment.zip .................. compressed bbc news files
 ┃ ┣ 📜clean_sample.py ................................. clean noun phrases, sample 200 multi word NPs
 ┃ ┣ 📜npcr.py ......................................... extract noun chunks from all files in "news/" to "nps_spacy_news.txt"
 ┃ ┣ 📜nps_news_clean.txt .............................. clean version of "nps_spacy_news.txt"
 ┃ ┣ 📜nps_news_clean_300_examples.txt ................. 300 multiword NPs from "nps_news_clean.txt"
 ┃ ┣ 📜nps_spacy_news.txt
 ┃ ┣ 📂predictions ..................................... score calculations of silver standard on SCL-NMA
 ┃ ┃ ┣ ...
 ┃ ┣ 📂rankings
 ┃ ┃ ┣ 📂bbc_news
 ┃ ┃ ┣ 📂scl_nma
 ┃ ┣ 📂scl_nma ......................................... General English Sentiment Modifiers Lexicon (SCL-NMA)
 ┃ ┃ ┣ ...
 ┃ ┣ 📜generate_scores_silver_standard.py
 ┃ ┣ 📜kendall_out.txt
 ┃ ┣ 📜metrics_out.txt
 ┃ ┗ 📜predictions_nps.txt ............................. score calculations of silver standard on NPs
 ┣ 📜quantification.ipynb .............................. main file, train gold standard models and create ranking
 ┣ 📜quantification_silver.ipynb ....................... main file, train silver standard models and create ranking
 ┗ 📜requirements.txt
 ```

