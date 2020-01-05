#!/usr/bin/env python
# coding: utf-8

# # Export .txt files for titles and abstracts
# 
# ## Library imports

# In[1]:


import pandas as pd
import glob
import datetime
import matplotlib.pyplot as plt
import matplotlib
import os
import zipfile

# In[2]:


def time_elapsed(start):
    end = datetime.datetime.now()

    time_to_run = end - start
    minutes = int(time_to_run.seconds/60)
    seconds = time_to_run.seconds % 60
    return "Total runtime: " + str(minutes) + " minutes, " + str(seconds) + " seconds"


# In[3]:


start = datetime.datetime.now()


# ## Import data
# 
# There are two different folders for different slices of ArXiV: `per_category` and `per_year`. The easiest for getting the full dataset is to combine `per_year`.
# 
# Note: it is very important to specify the data types, particularly `arxiv_id`, as Pandas may assume they are floats based on some initial rows, when they are actually strings. 

# In[4]:


dumpdate = "20200101"


# In[5]:


datadir = "processed_data/" + dumpdate + "/per_year/"


# In[6]:


files = glob.glob(datadir + "*.tsv.zip")
len(files)
files.sort()


# In[7]:


dtypes = {
    "abstract": object,
    "acm_class": object,
    "arxiv_id": object,
    "author_text": object,
    "categories": object,
    "comments": object,
    "created": object,
    "doi": object,
    "num_authors": int,
    "num_categories": int,
    "primary_cat": object,
    "title": object,
    "updated": object,
    "created_ym": object
    }


# In[8]:


df_all = pd.DataFrame()

for file in files:
    print(file)
    
    yearly_df = pd.read_csv(file,
                            sep="\t",
                            index_col=0,
                            compression='zip',
                            dtype=dtypes,
                            parse_dates=["created","updated"])
            
    df_all = df_all.append(yearly_df)
    
    print("Records this year: ", len(yearly_df), "Cumulative total: ", len(df_all), "\n")


# ### Checking merged dataframe

# In[9]:


len(df_all)


# In[10]:


df_all = df_all.drop_duplicates()
len(df_all)


# In[11]:


df_all.sample(2).transpose()


# # Export

# In[ ]:





# In[12]:


df_all.abstract.to_csv("processed_data/" + dumpdate + "/arxiv-abstracts-all.txt", index=False)
df_all.title.to_csv("processed_data/" + dumpdate + "/arxiv-titles-all.txt", index=False)


# In[13]:


abs_all_fn = "processed_data/" + dumpdate + "/arxiv-abstracts-all.txt"
title_all_fn = "processed_data/" + dumpdate + "/arxiv-titles-all.txt"

os.system("zip " + abs_all_fn + ".zip " + abs_all_fn)
os.system("zip " + title_all_fn + ".zip " + title_all_fn)


# In[14]:


df_250k = df_all.sample(250000, random_state = 12345)
df_250k.abstract.to_csv("processed_data/" + dumpdate + "/arxiv-abstracts-250k.txt", index=False)
df_250k.title.to_csv("processed_data/" + dumpdate + "/arxiv-titles-250k.txt", index=False)


# In[15]:


abs_250k_fn = "processed_data/" + dumpdate + "/arxiv-abstracts-250k.txt"
title_250k_fn = "processed_data/" + dumpdate + "/arxiv-titles-250k.txt"

os.system("zip " + abs_250k_fn + ".zip " + abs_250k_fn)
os.system("zip " + title_250k_fn + ".zip " + title_250k_fn)


# In[ ]:




