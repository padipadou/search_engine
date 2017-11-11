# Variable names:

## Dictionaries:

### *datadict*:
dict with docnum as key, content of each doc as value

### *num_name_dict*:
dict with docnum  as key, name of the doc as value

### *name_num_dict*:
dict with name of the doc as key, docnum as value

### *word_num_dict*:
dict with normalized *(stem, lower, etc regarding to the code options)* word as key, wordnum as value

### *num_word_dict*:
dict with wordnum  as key, normalized *(stem, lower, etc regarding to the code options)* word as value

### *infos_doc_dict*:
dict with docnum  as key, list as value (per doc; list[0]: total nb of words, list[1]: term frequency max)

### *index_dict*:
dict with wordnum as key, dict as value (dict with docnum as key, list of positions OR a count per doc as value)

### *word_dict*:
derives from *index_dict* with:
```python
  word_dict = index_dict.get(wordnum)
```
dict with docnum as key, list of positions OR a count per doc as value

### *tf_idf_dict*:
dict with wordnum as key, dict as value (dict with docnum as key, tf x idf as value per doc)

### *tf_dict*:
**Empty** if bm25 is not used.
dict with wordnum as key, tf as value

### *AAA*:

### *AAA*:

### *AAA*:

### *AAA*:

### *AAA*:

## Other important variables:

### *stopwords*:
set of stopwords from *stopwords-fr.txt*.

