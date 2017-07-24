# Create RDD
lines = sc.textFile("README.md")

# Basic Filter with lambda
pythonLines = lines.filter(lambda line: "Python in line")

# Basic Count
pythonLines.count()

# Pull the first line
pythonLines.first()

# Persist an RDD in memory -- useful when needing to use an intermediate RDD
# multiple times
pythonLines.persist

# Parallelize data to create an RDD
lines = sc.parallelize(["pandas", "i like pandas"])

# Create an RDD of a log file and filter on "ERROR" and "WARNING"
inputRDD = sc.textFile("log.txt")
errorsRDD = inputRDD.filter(lambda x: "ERROR" in x)
warningsRDD = inputRDD.filter(lambda x: "WARNING" in x)
badLinesRDD = errorsRDD.union(warningsRDD)
# Print results
print("Input had " + str(badLinesRDD.count()) + " concerning lines")
print("Here are 10 examples:")
for line in badLinesRDDtake(10):
    print(line)

# Filter by passing in a function
def containsError(line):
    return "ERROR" in line
word = inputRDD.filter(containsError)

# Basic map function
nums = sc.parallelize([1, 2, 3, 4])
squared = nums.map(lambda x: x * x).collect() 
for num in squared:
    print ("%i " % (num))

# Basic flat map function
lines = sc.parallelize(["hello world", "hi"]) 
words = lines.flatMap(lambda line: line.split(" ")) 
words.first()

nums_two = sc.parallelize([3,4,5,6])

nums.union(nums_two)
nums.intersection(nums_two)
nums.cartesian(nums_two).collect()

nums.reduce(lambda x,y: x + y)


# Read in data from csv
df = spark.read.format("csv").option("inferSchema", "true").option("header", "true").load("/Users/jeremybakker/Desktop/flight_data.csv")

# Transform dataframe into a table
df.createOrReplaceTempView("flight_data_2017")

# SQL Query to find number of originating flights by destination
sql = spark.sql("""SELECT ORIGIN, count(1) FROM flight_data_2017 GROUP BY ORIGIN ORDER BY count(1) DESC""")
# Same query with dataframe
from pyspark.sql.functions import desc
dfQuery = df.groupBy("ORIGIN").count().sort(desc("count"))

# Show the Spark physical plans - The underlying plans are the same.
sql.explain()
# OUT
# == Physical Plan ==
# *Sort [count(1)#96L DESC NULLS LAST], true, 0
# +- Exchange rangepartitioning(count(1)#96L DESC NULLS LAST, 200)
#    +- *HashAggregate(keys=[ORIGIN#13], functions=[count(1)])
#       +- Exchange hashpartitioning(ORIGIN#13, 200)
#          +- *HashAggregate(keys=[ORIGIN#13], functions=[partial_count(1)])
#             +- *FileScan csv [ORIGIN#13] Batched: false, Format: CSV, Location: InMemoryFileIndex[file:/Users/jeremybakker/Desktop/flight_data.csv], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<ORIGIN:string>
dfQuery.explain()
# OUT== Physical Plan ==
# *Sort [count#292L DESC NULLS LAST], true, 0
# +- Exchange rangepartitioning(count#292L DESC NULLS LAST, 200)
#    +- *HashAggregate(keys=[ORIGIN#13], functions=[count(1)])
#       +- Exchange hashpartitioning(ORIGIN#13, 200)
#          +- *HashAggregate(keys=[ORIGIN#13], functions=[partial_count(1)])
#             +- *FileScan csv [ORIGIN#13] Batched: false, Format: CSV, Location: InMemoryFileIndex[file:/Users/jeremybakker/Desktop/flight_data.csv], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<ORIGIN:string>

# Print schema of the dataframe, which deines the column names and types of a DataFrame
df.printSchema()
df.schema

# Two ways to create columns
from pyspark.sql.functions import col, column
col("columnName")
column("columnName")

# See all columns listed
df.columns

# See first row
df.first()

# Create a row 
from pyspark.sql import Row
myRow = Row("Hello", None, 1, False)

# Access data from Row
myRow[0]

# Add a column that specifies whether the destination and origin country are the same
df.selectExpr("*", "(DEST_COUNTRY = ORIGIN_COUNTRY) as WithinCountry").show(2)

# Aggregate over the entire dataframe with selectExpr
df.selectExpr("avg(NONSTOP_MILES)", "count(distinct(DEST_COUNTRY))").show()

# Add a literal value with an alias
df.select(expr("*"), lit(1).alias("One")).show(2)

# Add a column using withColumn - withColumn takes to arguments: name and expression to create the value for a given row
df.withColumn("numberOne", lit(1)).show(2)

# Rename column
df.withColumnRenamed("DEST_COUNTRY", "Destination Country")

# Drop column
df.drop("DEST_COUNTRY")

# Two different ways to filter - explain() outputs are the same
colCondition = df.filter(col("NONSTOP_MILES") > 1000)
conditional = df.where(col("NONSTOP_MILES") > 1000)


