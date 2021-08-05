# Meta-tag-Generation-for-SEO-using-LSTM-models

The folders are organized as follows:

1.	Data Gathering folder:
    a.	1_Glossary: has the code to scrape Investopedia and Wikipedia fintech pages.
    b.	2_Link_Lists: generate the bi-grams and tri-grams lists containing the search terms to be used and collect the top 10 links associated with each search term.
    c.	3_Metatag_Extractor_Threading: access each of the links collected previously and extract the “keywords” and “description” meta-tags from them.
    d.	4_Dataframes: put together all the information gathered so far and create the necessary dataframes, each containing the following columns: search_term, url, position, metatags.
    e.	All the text files in this folder are the result from the 2_Link_Lists notebook which will be used in the 3_Metatag_Extractor_Threading Python file.

2.	 Data Cleaning folder:
    a.	5_Data_Cleaning: basic steps to clean and tidy up the text data.
    b.	All of the csv files in this folder are the result from the Data Gathering folder. They are used in the 5_Data_Cleaning  notebook.

3.	Modelling folder:
    a.	Modelling: contains the code for the built model.

4.	Deployment folder:
    a.	To run the deployment run the below command:
        i.	python app.py
    b.	All the other files are used for the GUI of the web page.

5. pickles folder:
    Contains all the files generated from the previous steps as .pkl. They are loaded into some of the notebooks above.

PS: To run the code it is necessary to change all the paths and relative paths wherever applicable.
