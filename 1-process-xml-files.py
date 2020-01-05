#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import glob
import datetime
#import lxml.etree as ET
from xml.dom import minidom
import datetime
import pathlib

#get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


date = "20200101"


# In[3]:


datadir = "/home/staeiou/data/arxiv/oai-af/"


# In[4]:


start = datetime.datetime.now()


# In[5]:


def time_elapsed(start):
    end = datetime.datetime.now()

    time_to_run = end - start
    minutes = int(time_to_run.seconds/60)
    seconds = time_to_run.seconds % 60
    return "Total runtime: " + str(minutes) + " minutes, " + str(seconds) + " seconds"


# ## Parse all raw XML files

# In[6]:


fn = glob.glob(datadir + "*")


# In[7]:


len(fn)


# In[8]:


doc = minidom.parse(datadir + "oai:arXiv.org:1503.04358.arXiv.xml")
print(doc.toprettyxml())


# In[9]:


def get_author_text(doc):
    """
    Inputs a minidom doc object, outputs a tuple of (string formatted list of authors, python list of authors).
    
    Helper function for doc_to_dict()
    
    """
    authorlist = []
    authortext = ""
    for author in doc.getElementsByTagName("authors")[0].childNodes:
        keyname = author.getElementsByTagName("keyname")[0].firstChild.data
        try:
            forenames = author.getElementsByTagName("forenames")[0].firstChild.data
        except:
            forenames = ""
        authortext += forenames + " " + keyname + ", "
        authorlist.append(forenames + " " + keyname)
    return authortext[:-2].replace("  ", " "), authorlist


# In[10]:


get_author_text(doc)


# In[11]:


def doc_to_dict(doc):
    """
    Inputs a minidom object, returns a dictionary of all metadata
    
    """
    title = doc.getElementsByTagName("title")[0].firstChild.data
    arxivid = doc.getElementsByTagName("id")[0].firstChild.data
    created = doc.getElementsByTagName("created")[0].firstChild.data
    categories = doc.getElementsByTagName("categories")[0].firstChild.data
    abstract = doc.getElementsByTagName("abstract")[0].firstChild.data
    primary_cat = categories.split(" ")[0]
    
    author_text, author_list = get_author_text(doc)
    
    num_authors = len(author_list)
    
    num_categories = len(categories.split(" "))
    
    try:
        comments = doc.getElementsByTagName("comments")[0].firstChild.data
    except IndexError:
        comments = np.nan
        
    try:
        acm_class = doc.getElementsByTagName("acm-class")[0].firstChild.data
    except IndexError:
        acm_class = np.nan
        
    try:
        updated = doc.getElementsByTagName("updated")[0].firstChild.data
    except IndexError:
        updated = np.nan
        
    try:
        doi = doc.getElementsByTagName("doi")[0].firstChild.data
    except IndexError:
        doi = np.nan         
        
    row = {
           'title':title,
           'updated':updated,
           'arxiv_id':arxivid,
           'created':created,
           'categories':categories.replace(" " , ","),
           'num_categories':num_categories,
           'primary_cat':primary_cat,
           'abstract':abstract,
           'doi':doi,
           'acm_class':acm_class,
           'comments':comments,
           'author_text':author_text,
           'num_authors':num_authors
    }
    
    return row


# ### Iterate through all XML files and parse into list of dictionaries

# In[12]:


df_list = []
dates = []
for file in fn:

    try:
        row = doc_to_dict(minidom.parse(file))
        

        df_list.append(row)

        if len(df_list) % 100000 is 0:
            print(len(df_list), time_elapsed(start))
    
    except IsADirectoryError:
        pass
    


# ### Convert list of dicts to dataframe

# In[13]:


df = pd.DataFrame(df_list)


# ### Remove all rows after 2019

# In[14]:


df = df.query("created < '2020-01-01'")


# In[15]:


len(df)


# ## Spot checking

# In[16]:


len(df)


# In[17]:


df = df.drop_duplicates()
len(df)


# In[18]:


print(df.query("arxiv_id == '1207.2757'").author_text)


# In[19]:


df.query("author_text == 'R. Stuart Geiger'")


# In[20]:


df.query("doi == '10.1145/2702613.2732781'")


# ## Final export

# In[21]:


pathlib.Path("processed_data/" + date).mkdir(parents=True, exist_ok=True) 


# In[22]:


df.to_csv("processed_data/" + date + "/arxiv-oai-af.tsv", sep="\t", index=False)


# In[24]:


# df.to_pickle("processed_data/" + date + "/arxiv-oai-af.pkl")


# In[25]:


time_elapsed(start)

