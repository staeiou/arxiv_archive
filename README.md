# arxiv_archive

This is a full archive of metadata about papers on arxiv.org, from the start of the site in 1993 to the end of 2019, including the python scripts used to process the dataset and Jupyter notebooks for unpacking and analyzing it. Note that if you just want to work with the data, it is best to download [the zip folder for this repository](https://github.com/staeiou/arxiv_archive/archive/master.zip) as opposed to running `git clone` (which will take up about 2x size on disk due to the git history). 

I used `oai-harvest` to collect metadata for every paper on arxiv.org from their OAI endpoint, which stores the metadata for each paper in a separate XML file. The python scripts in `/code/` include scripts that were used to generate the dumps from the original ArXiV XML OAI data harvests. These XML files are not included in this repository, but the scripts are included for purposes of reproducibility and open science. The code in `/code/analysis-examples.ipynb` shows you how to unpack the processed data in this repository and runs a number of sample analyses on the dataset. More details about the harvesting and processing approach are below. 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1463242.svg)](https://doi.org/10.5281/zenodo.1463242)

If you use this data or code, please cite it as (or use the `citation.bib` file):

``` R. Stuart Geiger (2020). "ArXiV Archive: A Tidy and Complete Archive of Metadata for Papers on arxiv.org." Zenodo. http://doi.org/10.5281/zenodo.1463242  ```


# Data documentation

## Inventory

### Titles and abstracts only

 - `processed_data/DATE/arxiv-titles-all.txt.zip`: All titles from all ArXiV papers in TXT format, with one title per line.
 - `processed_data/DATE/arxiv-titles-250k.txt.zip`: 250,000 randomly selected titles in TXT format, with one title per line.
 - `processed_data/DATE/arxiv-abstracts-250k.txt.zip`: 250,000 randomly selected abstracts in TXT format, with one abstract per line. These are the same set of 250,000 papers in the same order, so the two files can be easily combined.

### Full metadata for papers

The files in the folders `processed_data/DATE/per_category` and `processed_data/DATE/per_year` are compressed TSV files containing the same data, but organized differently. The `per_year` folder contains one TSV file per year, compressed in .zip format. The `per_category` contains one TSV file per Arxiv category, compressed in .xz format. Arxiv papers have primary and secondary categories (posting and cross-posting), and papers are in a category's dataset if they were either posted or cross-posted to that category. 

To recreate the full dataset, it is recommended to merge all files in the `per_year` folder, as merging all files in the `per_category` folder will have many duplicates.

## Data dictionary for full metadata files

These files are in `processed_data/DUMP_DATE/per_year/YEAR.tsv.zip` and `processed_data/DUMP_DATE/per_category/CATEGORY_NAME.tsv.zip`, with one row per line and tab-separated.

| Variable name  | Definition                                                                                  | Example                                           |
|----------------|---------------------------------------------------------------------------------------------|---------------------------------------------------|
| abstract       | Text of the abstract, may include LaTeX formatting.                                         | We find the natural embedding of the (R+R^2)-i... |
| acm_class      | ACM Classification (manually entered by authors, if exists)                                 |                                                |
| arxiv_id       | Arxiv internal ID. Can get to PDF by appending "https://arxiv.org/pdf/" + arxiv_id + ".pdf" | 1011.0240                                         |
| author_text    | Comma-separated list of authors                                                             | Sergei V. Ketov, Alexei A. Starobinsky            |
| categories     | Comma-separated list of all categories the paper was submitted to (posted and cross-posted) | hep-th,astro-ph.CO,gr-qc                          |
| comments       | Author comments                                                                             | 4 pages, revtex, no figures (very minor additi... |
| created        | Date created (YYYY-MM-DD)                                                                   | 2010-10-31                                        |
| doi            | DOI (manually entered by authors, if exists)                                                | 10.1103/PhysRevD.83.063512                        |
| num_authors    | Number of authors                                                                           | 2                                                 |
| num_categories | Number of categories                                                                        | 3                                                 |
| primary_cat    | Primary category the paper was submitted to                                                 | hep-th                                            |
| title          | Paper title, may include LaTeX                                                              | Embedding (R+R^2)-Inflation into Supergravity     |
| updated        | Date last updated (YYYY-MM-DD)                                                              | 2011-02-28                                        |
| created_ym     | Year and month created                                                                      | 2010-10                                           |

## Steps taken to generate the data

### Step 0: Query from arxiv.org

Arxiv's main permitted means of bulk downloading article metadata is through its [OAI-PMH API](https://arxiv.org/help/bulk_data). I used the [oai-harvest](https://github.com/bloomonkey/oai-harvest) program to download this, which stores the records in one XML file per paper, for a total of about 1.4 million files. These files are too large to be uploaded here. The oai-harvest logs and configuration details are in `/logs/`. The last run was completed on 2020-01-02 at 02:51:30 GMT. Note that papers can be updated at any time.

### Step 1: Process XML files

In the python script `/code/1-process-xml-files.ipynb`, the individual XML files are processed into a single large Pandas DataFrame, which is stored in TSV and pickle formats. These files are too large to be uploaded here.

### Step 2: Process categories and output to per_year and per_category TSVs

In the python script `/code/2-process-categories-out.ipynb`, the large TSV file created in step 1 is parsed and separated into two different batched outputs in the `processed_data/per_year` and `processed_data/per_category` folder. 

### Step 3: Export raw titles and abstracts

In the python script `/code/3-abstracts-export.ipynb`, the `per_year` datasets are unpacked and merged, then two sets of files are created for 1) just abstracts and 2) just titles, with one title or abstract per line. This creates zipped files for all items (too large to upload on GitHub) and a random sample of 250k items, which can be found in `processed_data/DUMP_DATE/arxiv-abstracts-250k.txt.zip` and `processed_data/DUMP_DATE/arxiv-titles-250k.txt.zip`.

### Step 4: Unpack datasets and analyze

In the Jupyter notebook `/code/analysis-examples.ipynb`, the `per_year` datasets are unpacked and merged to one large dataframe, which is then analyzed in various ways. If you are looking to use this data to do an analysis on the entire Arxiv, you may find this notebook useful to start.
