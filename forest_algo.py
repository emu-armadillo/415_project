from pyspark.sql import SparkSession

input_uri = "mongodb+srv://Guest:Password@415cluster01.4lf0c.mongodb.net/AmazonCopurchasing.ProductMetaData"
output_uri = "mongodb+srv://Guest:Password@415cluster01.4lf0c.mongodb.net/AmazonCopurchasing.ProductMetaData"

spark = SparkSession.builder \
    .appName("myProject") \
    .config("spark.mongodb.input.uri", input_uri) \
    .config("spark.mongodb.output.uri", output_uri) \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.2") \
    .getOrCreate()


df_read = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()


df_read.printSchema()




def get_data_element(id):
    n = df_read.filter(df_read.ASIN==id).head(1)
    if len(n)>0:
        n = n[0]
        return n
    else:
        return None
    


def get_similar_ids(id):
    n = df_read.filter(df_read.ASIN==id).head(1)
    print(type(n[0]))
   
    return n[0]["similar"]["items"]
def get_category_set(id):
    cat = get_data_element(id)["categories"]['details']
    cat = "".join(cat)
    cat = cat.split("|")
    cat = set(cat)
    # print("here")
    # print(type(cat))
    # print(cat)
    

    return cat

def get_similar_items(id):
    max_depth = 3
    depth = 1
    nodes_to_process = []
    curr_level = []
    nodes_scores = []
    #find better solution
    #can make hash table to speed up
    #previously visited nodes
    n_levels = [[id],[],[],[],[],[],[]]
    nodes_to_process.extend(get_similar_ids(id))
    cat = get_category_set(id)
    cat = set(cat)
    print(cat)
    print(nodes_to_process)
    while(depth <= max_depth):

        for node_id in nodes_to_process:
           # print(node_id)
            node = get_data_element(node_id)
            if node is not None:
                print("valid")
                quality = node["reviews"]["avg_rating"]* node["reviews"]["total"]
                cur_cat = get_category_set(node_id)
                cur_cat = set(cur_cat)
                print(f"type cat {type(cat)}")
                c_num_match = len(cat.intersection(cur_cat))
                print(cur_cat)
                print(cat)
                print(f"same catagories: {c_num_match}")
                quality += c_num_match
                cur_id = node_id   
                #adds a multiplier if it links back to previous nodes 1 1/2 1/3 ... ect 
                multi = 1.0
                for i in range(0,depth):
                    
                    ins = set(n_levels[i]).intersection(set(get_similar_ids(node_id)))
                    multi += len(ins)/(i+1)
                nodes_scores.append((cur_id,quality,multi))
                curr_level.append((cur_id,quality,multi))
                n_levels[depth].append(node_id)
            else:
                print("node does not exist")
        nodes_to_process.clear()
       # print(len(curr_level))
        temp_get_max = sorted(curr_level, key=lambda x: x[1] * x[2], reverse=True)
       # print(temp_get_max)
        nodes_to_process.extend(get_similar_ids(temp_get_max[0][0]))
       # print(len(curr_level))
        curr_level.clear()
        print("depth +=")
        print(nodes_scores)
        depth+=1

    best =  sorted(nodes_scores, key=lambda x: x[1] * x[2], reverse=True)

    return best


#if __name__ == "main":
 #   mongodb+srv://Guest:Password@415cluster01.4lf0c.mongodb.net/




# test = collection.find().limit(10)

# for i in test:
#     print(i)
#     get_similare_items("0231118597")
# for i in ['B000067D0Y', '0375727191', '080148605X', '1560232579', '0300089023']:
#     print(get_data_element(i))
print(get_similar_ids("0231118597"))
j = get_similar_items('B000067D0Y')
print(j)
seen = []
for i in  j:
    if i[0] not in seen:
        print(get_data_element(i[0])["title"])
        seen.append(i[0])

print(get_data_element("B000067D0Y"))
