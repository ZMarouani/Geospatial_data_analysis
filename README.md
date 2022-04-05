# Geospatial_data_analysis

# Project structure :

In this project i used geopandas with python to analyse various files containing informations about gps positions and stores positions in order to analyse the costumers behaviour .<br/>
Coding this project was possible through the usage of databricks service hosted on Aws cloud platform running through  Ec2 instances as the cluster, also using Aws S3 cloud object storage to upload our training data , sample data and finally store our results ( you will also find a csv copy of the results in this repo ) .<br/>
The s3 bucket was mounted to the databricks dbfs (Databricks File System) using Aws instance profile , which will allow us to explore it's paths and files (using databricks dbutils) as if the s3 bucket was a local file system . <br/>
The python notebooks were exported on three different formats (ipynb , python source code and HTML) , the three different formats were uploaded to this github repoistory .<br/>

# How to run the script : 

You can check the .HTML version of the notebook in order to see the code with the execution and results . 

To run the script you can upload any of the different formats to your databricks platform and simply execute it (after changing the files paths or simply mounting your own s3 bucket) or simply running locally the oython source code version of the notebooks.

The notebook's cluster already contains the necessary dependecies that were installed through pip : <br/>
%pip install geopandas <br/>
%pip install shapely <br/>
%pip install fsspec <br/>
%pip install s3fs  <br/>
%pip install rtree  <br/>

( if you are going to run it locally you will probably need also to pip install pandas , fiona and gdal )

# The data 
The S3 bucket contains three different data sources:
- GPS signals of users 
- Berlin store polygons
- User affinity datasets

The S3 bucket had the following structure :

https://s3.console.aws.amazon.com/s3/buckets/train-data-20221903 : <br/>
|-Berlin_map_data/plz_5-stellig_berlin.kml  : .kml file containg berlin map informations for geopandas <br/>
|- oregon-prod/ : contains jobs logs and meta data <br/>
|- Results_data/ : seperated in folders with names as 'year-month-day' format  , each folder contains the results data of the corresponding day . <br/>
|- sample_data/	: contains sample gps data <br/>
|- train_data/ : contains gps full data , store polygones and affinity datasets <br/>

The Berlin map was downloaded from  : https://www.suche-postleitzahl.org/berlin.13f
                                                                
# Data visualization 

After applying spatial join between the gps signals dataframes and the stores dataframe , here are some vizualisations and insights : 

# The trend of unique visits for all places : 

In the first visualization we see the sum of unique visitors on all stores for each day , we can detect some anomalies where we hace very low number of unique visitors to all stores compared to the rest of the days , on the following dates : <br/>
- 2021-01-01  corresponds to Friday and the first day of the new year <br/>
- 2021-01-03 corresponds to Sunday   <br/>
- 2021-01-10  corresponds to Sunday  <br/>
- 2021-01-17  corresponds to Sunday <br/>

So on Sundays the we have the lowest number of visitors or consumers to the stores .

![uniqvisit_All](https://user-images.githubusercontent.com/17991782/159584401-b30eb670-1b4c-4b0e-929e-b73bc5fde517.png)

In the Second visualization , where we have a more detailed view , we see that on the mentioned dates ( 2021-01-01/03/10/17 ) , fast food business (like mcdonalds and Burger king) are an exception to the rule and keep having unique visitors close to their average unique visitors number unlike hypermarket and retail business ( like Aldi , Kaufland , Rewe ) .

![uniqvisit_each](https://user-images.githubusercontent.com/17991782/159584411-63e1d20b-5960-4c4e-b4ba-4ecda4017a20.png)



# GPS data visualization : 

The vizualisation or distribution of all the gps signals looks like a polygone , which means that the devices locations are not random so we can predict the various locations for consumer behaviour or the best places to open new stors and get more people to come .<br/>

![Gps_vizualization](https://user-images.githubusercontent.com/17991782/159584439-79a9dc5a-baaa-44a2-9a0b-682ea89afa2c.png)



# Stores locations visualization : 

At this part we observe the locations of the stores but more specifically in Berlin which allows us to interpret the variations between the numbers of unique visitors to each store through the relation of the distance of the store from the center of Berlin or the diamant shape of the Gps visualization .



![stores_in_Berlin_Big](https://user-images.githubusercontent.com/17991782/159584472-025bdeca-3568-436f-b4fd-22a3efcbe29d.png)











