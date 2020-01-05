#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import glob
import os
import datetime
import pathlib


# In[2]:


dumpdate = "20200101"


# In[3]:


def time_elapsed(start):
    end = datetime.datetime.now()

    time_to_run = end - start
    minutes = int(time_to_run.seconds/60)
    seconds = time_to_run.seconds % 60
    return "Total runtime: " + str(minutes) + " minutes, " + str(seconds) + " seconds"


# In[4]:


start = datetime.datetime.now()


# ## Import processed data 

# In[5]:


df_all = pd.read_csv("processed_data/" + dumpdate + "/arxiv-oai-af.tsv", sep="\t")
len(df_all)


# In[6]:


df_all[51:54].transpose()


# ## Processing
# 

# In[7]:


def list_to_string(l):
    return ', '.join(l)


# In[8]:


def remove_initial_space(s):
    if s[0] == ' ':
        return s[1:]
    else:
        return s


# In[9]:


df_all.abstract = df_all.abstract.apply(str.replace,args=("\n"," "))
df_all.abstract = df_all.abstract.apply(str.replace,args=("  "," "))
df_all.abstract = df_all.abstract.apply(str.replace,args=("  "," "))
df_all.abstract = df_all.abstract.apply(remove_initial_space)
df_all.title = df_all.title.apply(str.replace,args=("\n"," "))
df_all.title = df_all.title.apply(str.replace,args=("  "," "))
df_all.title = df_all.title.apply(str.replace,args=("  "," "))


# In[10]:


df_all.iloc[5].abstract


# ### Get to one dataframe for each category

# In[11]:


df_all['categories_list'] = df_all.categories.apply(str.split,args=",")


# In[12]:


df_all.iloc[3].categories_list


# In[13]:


categories = []

for row in df_all.iterrows():
    for cat in row[1].categories_list:
        #print(cat)
        if cat not in categories:
            categories.append(cat)
      


# In[14]:


categories.sort()
print(len(categories))


# In[15]:


df_dict = {}

for cat in categories:
   # print(cat)
    df_dict[cat] = df_all[df_all['categories'].str.contains(cat)]
    
    df_dict[cat] = df_dict[cat].sort_values(by='created')
   # print(len(df_dict[cat]))


# In[ ]:





# In[16]:


print(df_all.query("doi=='10.1103/PhysRevD.86.101501'"))


# # File output

# In[17]:


os.system("rm processed_data/" + dumpdate + "/per_month/*")
pathlib.Path("processed_data/" + dumpdate + "/per_month/").mkdir(parents=True, exist_ok=True)


# In[18]:


def get_month(s):
    return s[0:7]


# In[19]:


df_all = df_all.drop("categories_list", axis=1)
df_all['created_ym'] = df_all.created.apply(get_month)


# In[20]:


def get_year(s):
    return s[0:4]


# In[21]:


os.system("rm processed_data/" + dumpdate + "/per_year/*")
pathlib.Path("processed_data/" + dumpdate + "/per_year/").mkdir(parents=True, exist_ok=True) 


# In[22]:


df_all['created_year'] = df_all.created.apply(get_year)

for year in range(1993,2020):


    query = "created_year == '" + str(year) + "'"

    yearly_df = df_all.query(query)
    
    yearly_df = yearly_df.sort_values(by='created')
    
    filename = "processed_data/" + dumpdate + "/per_year/" + str(year) + ".tsv"

    yearly_df.drop("created_year", axis=1).to_csv(filename, sep="\t")

    zip_str = "zip -9 " + filename + ".zip " + filename
    os.system(zip_str)

    zip_size = round(os.path.getsize(filename + ".zip")/1024/1024,2)

    print(str(year), len(yearly_df), zip_size)


# In[ ]:





# In[23]:


os.system("rm processed_data/" + dumpdate + "/arxiv_oaiaf_catkey.h5")


# In[24]:


os.system("rm processed_data/" + dumpdate + "/per_category/*")


# In[25]:


pathlib.Path("processed_data/" + dumpdate + "/per_category/").mkdir(parents=True, exist_ok=True) 


# In[26]:


for cat in categories:
    fn = "processed_data/" + dumpdate + "/per_category/" + cat
    df_dict[cat].to_csv(fn+".tsv", sep="\t", mode="w")
    #df_dict_generic[cat].to_hdf(fn+".h5", key="df", mode="w")
    
    zip_str = "zip -9 " + fn+".tsv.zip " + fn + ".tsv"
    bzip2_str = "bzip2 -kz9 " + fn + ".tsv"
    xz_str = "xz -kz9 " + fn + ".tsv"

        
    #os.system(zip_str)
    #os.system(bzip2_str)
    os.system(xz_str)
    
    xz_size = round(os.path.getsize(fn+".tsv.xz")/1024/1024,2)
    
    print(fn, xz_size, "M")
    
    # for h5 export
    
    # cat_key = cat.replace(".","_")
    # cat_key = cat_key.replace("-","_")
    # df_dict[cat].to_hdf("processed_data/" + dumpdate + "/arxiv_oaiaf_catkey.h5",
    #                            key=cat_key, mode="a")
    


# In[27]:


print(time_elapsed(start))

