# Spark and MinIO

we need to install the following packages In the /opt/bitnami/spark/jars

```
curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.30/aws-java-sdk-1.11.30.jar --output aws-java-sdk-1.11.30.jar 
curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.7.3/hadoop-aws-2.7.3.jar --output hadoop-aws-2.7.3.jar
curl https://repo1.maven.org/maven2/net/java/dev/jets3t/jets3t/0.9.4/jets3t-0.9.4.jar --output jets3t-0.9.4.jar
```

# Could not create folder with jupyter notebook
Just
```
chmod 777 /path/dir
```
and it should work