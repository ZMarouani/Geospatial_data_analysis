# Geospatial_data_analysis

# Project structure :

In this project i used geopandas with python to analyse various files containing informations about gps positions and stores positions in order to analyse the costumers behaviour . Coding this project was possible through the usage of databricks service hosted on Aws cloud platform running through  Ec2 instances as the cluster, also using Aws S3 cloud object storage to upload our training data , sample data and finally store our results ( you will also find a csv copy of the results in this repo ) . The s3 bucket was mounted to the databricks dbfs (Databricks File System) using Aws instance profile , which will allow us to explore it's paths and files (using databricks dbutils) as if the s3 bucket was a local file system .    . 
The python notebooks were exported on three different formats (ipynb , python source code and HTML) , the three different formats were uploaded to this github repoistory .

# How to run the script : 

You can check the .HTML version of the notebook in order to see the code with the execution and results . 

To run the script you can upload any of the different formats to your databricks platform and simply execute it (after changing the files paths or simply mounting your own s3 bucket) . The notebook already contains the necessary dependecies that were installed through pip : 
%pip install geopandas
%pip install shapely
%pip install fsspec
%pip install s3fs
%pip install rtree

( if you are going to run it locally you will probably need also to pip install pandas , fiona and gdal )

# The data 
The S3 bucket contains three different data sources:
- GPS signals of users 
- Berlin store polygons
- User affinity datasets

The S3 bucket had the following structure :

https://s3.console.aws.amazon.com/s3/buckets/train-data-20221903 : 
                                                                |-Berlin_map_data/plz_5-stellig_berlin.kml  : .kml file containg berlin map informations for geopandas 
                                                                |- oregon-prod/ : contains jobs logs and meta data
                                                                |- Results_data/ : contains the results data 
                                                                |- sample_data/	: contains sample gps data
                                                                |- train_data/ : contains gps full data , store polygones and affinity datasets
                                                                
# Data visualization 

After applying spatial join between the gps signals dataframes and the stores dataframe , here are some vizualisations and insights : 

# The trend of unique visits for all places : 

Restaurants and fastfood has in general more visitors per day than other supermarkets or retail companies , we can see here that mackdonalds had much more unique visitors per day than Mercedes for example , this also can be explained buy the date wich might reflect some kind of discount , also through this we get a consumer bhaviour in commun between these different visitor which can be used further by recommending to each other something that a different visitor is used to buy or consume . 


![bar_chart_uniquevisits](https://user-images.githubusercontent.com/17991782/159183689-49205fe6-a3b8-44a2-9e4d-9022a3b83247.png)




![pie_chart](https://user-images.githubusercontent.com/17991782/159183882-4bcd40be-6be3-47f2-b1f7-3b791dcd7036.png)



# GPS data visualization : 

The vizualisation of all the gps signals looks like a polygone or diamant shape and very concentrated in the middle ( which totally intersects with the center of Berlin) , which means that the devices locations are not random so we can predict the various locations for consumer behaviour or the best places to open new stors and get more people to come .

In the second photo we see that the gps signals are not totaly contained in Berlin , and that various places in Berlin have not been visited by the devices holders .


![Gps_positions_Visualization](https://user-images.githubusercontent.com/17991782/159183907-48dfefac-b4c9-499b-a588-26cf7bc65daf.png)


![Berlin_map_Gps_positions_Visualization](https://user-images.githubusercontent.com/17991782/159184029-f1560412-774f-45ce-9214-b76228b3c6ef.png)


# Stores locations visualization : 

At this part we observe the locations of the stores but more specifically in Berlin which allows us to interpret the variations between the numbers of unique visitors to each store through the relation of the distance of the store from the center of Berlin or the diamant shape of the Gps visualization .





![stores_in_Berlin](https://user-images.githubusercontent.com/17991782/159184046-d4df9ba9-1d54-4e3f-a65b-b64393ff3cce.png)











