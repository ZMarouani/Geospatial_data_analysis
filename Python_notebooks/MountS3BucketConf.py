# Databricks notebook source
# DBTITLE 1,Mount S3 bucket using Aws instance profile
aws_bucket_name = "train-data-20221903"
mount_name = "s3-bucket-mount"
dbutils.fs.mount("s3a://%s" % aws_bucket_name, "/mnt/%s" % mount_name)
display(dbutils.fs.ls("/mnt/%s" % mount_name))

# COMMAND ----------

# DBTITLE 1,Unmount S3 bucket
# dbutils.fs.unmount(f"/mnt/{mount_name}")

# COMMAND ----------

# DBTITLE 1,Test read permission 
dbutils.fs.ls("s3a://train-data-20221903/train_data/affinities/affinities/")

# COMMAND ----------

dbutils.fs.ls("dbfs:/mnt/s3-bucket-mount/train_data/stores.csv")

# COMMAND ----------


