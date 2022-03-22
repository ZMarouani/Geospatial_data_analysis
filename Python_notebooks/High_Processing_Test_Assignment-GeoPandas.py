# Databricks notebook source
# DBTITLE 1,Installing dependencies
# MAGIC %pip install geopandas
# MAGIC %pip install shapely
# MAGIC %pip install fsspec
# MAGIC %pip install s3fs
# MAGIC %pip install rtree

# COMMAND ----------

# DBTITLE 1,Import pandas ,geopandas and shapely for geometric dataframes 
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame , sjoin
from shapely.geometry import Point, Polygon
from shapely import wkt
import fiona
import seaborn as sns

gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'


# COMMAND ----------

# DBTITLE 1,Map Gps data to Points (using full data) 
csv_path = 's3a://train-data-20221903/train_data/ full_signals/full_data/'

csv_dict = dbutils.fs.ls(f'{csv_path}')
csv_names_path = { fileinfo.name.split('.')[0] : fileinfo.path for fileinfo in csv_dict  }
li = []

for filename,filepath in csv_names_path.items():
    df = pd.read_csv(filepath, index_col=None, header=0, compression='gzip')
    li.append(df)

gps_pandas_df = pd.concat(li, axis=0, ignore_index=True)

gps_pandas_df['utc_timestamp'] = pd.to_datetime(gps_pandas_df['utc_timestamp'], unit='ms', utc=True).dt.date
gps_pandas_df = gps_pandas_df.rename(columns={"Unnamed: 0": "row_id", "lat": "latitude", "lon" : "longitude", "utc_timestamp":"date"})
gps_pandas_df['geometry'] = gps_pandas_df.apply(lambda x : Point(x.longitude , x.latitude) , axis=1)

# Create geopandas dataframe object 
df_crs = { 'init' : 'epsg:4326'}
gps_geopandas_df = GeoDataFrame(gps_pandas_df , crs = df_crs, geometry = gps_pandas_df.geometry )

display(gps_geopandas_df)

# COMMAND ----------

# DBTITLE 1,Map Stores wkt column to polygones
stores_pandas_df = pd.read_csv("s3a://train-data-20221903/train_data/stores.csv")
stores_pandas_df['geometry'] = stores_pandas_df['wkt'].apply(wkt.loads)
stores_pandas_df.drop('wkt', axis=1, inplace=True)


stores_geopandas_df = GeoDataFrame(stores_pandas_df , crs = df_crs, geometry = stores_pandas_df.geometry)

display(stores_geopandas_df)

# COMMAND ----------

# DBTITLE 1,Devices ids of visitors whom went to the store ( using spatial join )
devices_within_stores = gps_geopandas_df.sjoin(stores_geopandas_df , predicate = 'within')
device_store_time = devices_within_stores[["date","store_name", "store_id","device_id"]]

display(device_store_time)

# COMMAND ----------

# DBTITLE 1,Creation of dict with name and path of affinities files
affinities_path = 's3a://train-data-20221903/train_data/affinities/'

affinities_dict = dbutils.fs.ls(f'{affinities_path}')
affinities_name_path = { fileinfo.name.split('.')[0] : fileinfo.path for fileinfo in affinities_dict  }


# COMMAND ----------

# DBTITLE 1,Merge dataframe with affinities tables
merge_df = device_store_time

for file_name in affinities_name_path : 
  affinity_df = pd.read_csv(affinities_name_path[file_name])
  affinity_df.columns = [file_name, 'device_id']
  affinity_df[file_name] = affinity_df['device_id']

  merge_df = merge_df.merge(affinity_df, on='device_id', how='left')
  

display(merge_df)

# COMMAND ----------

# DBTITLE 1,Counting visitors and unique visitor 
# Creation of group by dataframe 
merge_df_group = merge_df.groupby(["date","store_name", "store_id"])

# Aggregation of columns for count of unique visitors 
merge_df_nunique = merge_df_group.nunique(dropna=True).reset_index()

# Insert Total_signals column after store_id column
total_signals_column = (merge_df_group.agg({'device_id':'count'}).reset_index())['device_id']
merge_df_nunique.insert(loc=3, column='Total_signals', value=total_signals_column)

# Replace Null values with zeros in affilities columns and rename device_id column to unique_visits
merge_df_nunique[affinities_name_path.keys()].fillna(0, inplace = True)
merge_df_nunique = merge_df_nunique.rename(columns = {'device_id':'Unique_visits'})

display(merge_df_nunique)

# COMMAND ----------

# DBTITLE 1,Exporting the result data to s3 bucket 
from datetime import datetime

s3_export_path = 's3a://train-data-20221903/Results_data'
current_date = datetime.today().strftime('%Y-%m-%d')
current_time = datetime.now().strftime("%H:%M:%S.%f")

merge_df_nunique.to_csv(path_or_buf= f'{s3_export_path}/{current_date}/results_data_{current_time}.csv', header=True , index=False)


# COMMAND ----------

# DBTITLE 1,Visualizing unique visits per Date for each store 
display(merge_df_nunique)

# COMMAND ----------

# DBTITLE 1,Visualizing unique visits per Date for all stores
display(merge_df_nunique)

# COMMAND ----------

# DBTITLE 1,Visualize GPS data
import matplotlib.pyplot as plt 

fig , ax = plt.subplots(figsize=(10,15))
ax.axis("off")
ax.set_title('Visualisation of devices gps data with different color for each device')

gps_geopandas_df.plot(ax=ax , cmap='jet' , edgecolor='black' , column='device_id')

# COMMAND ----------

# DBTITLE 1,Copy Berlin map from S3 bucket to local file system
# The Berlin map was downloaded from the following website : 
# https://www.suche-postleitzahl.org/berlin.13f
# Afterwards the file was uploaded to the s3 bucket .

dbutils.fs.cp("s3a://train-data-20221903/Berlin_map_data/plz_5-stellig_berlin.kml", "file:/tmp/plz_5-stellig_berlin.kml", recurse = True)
berlin_map = gpd.read_file("file:/tmp/plz_5-stellig_berlin.kml", driver='KML')


# COMMAND ----------

# DBTITLE 1,Visualisation of stores locations inside Berlin
berlin_map.crs = 4326
ax = berlin_map.plot(color = 'lightgreen' , figsize=(20,20))
ax.axis("off")
ax.set_title('Visualisation of stores locations inside Berlin')

stores_geopandas_df.plot(ax=ax , cmap='jet' , edgecolor='black' , column='store_name')

# COMMAND ----------

gps_geopandas_df.memory_usage(deep=True)

# COMMAND ----------

gps_geopandas_df.dtypes

# COMMAND ----------

gps_geopandas_df.memory_usage(deep=True)

# COMMAND ----------

gps_geopandas_df.dtypes
