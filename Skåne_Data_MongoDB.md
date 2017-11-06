# OpenStreetMap Data Wrangling with MongoDB

### Map Area

Skåne, Sweden

* https://www.openstreetmap.org/relation/54409#map=8/55.837/13.126
* https://mapzen.com/data/metro-extracts/your-extracts/e6c75631ddab

So why this area? First, I'm interested to know how it looks like around Skåne. Second, this regoin seems unpopular, which could most probably generate uncompleted data. Therefore, it would be worth the effort to get started to work on the data somehow.

### Problems Encountered in the Selected Region

After exploring a sample size of the Skåne area via audit.py, I noticed the following main problems with the data, discussed as follows:

* Incorrect extract area: extracted some regional data from Denmark, taking the following as an example:     
  ```html
   <tag k="addr:country" v="DK" />          
  ```     
* Duplicated information: the same information was pulled from OSAK Danish database, e.g. 'osak:house_no' and 'addr:housenumber', 'osak:street_name' and 'addr:street'.
   ```html
  <tag k="addr:street" v="Give Alle" />
  <tag k="osak:house_no" v="12" />

  <tag k="addr:housenumber" v="12" />
  <tag k="osak:street_name" v="Give Alle" />
  ```
* Problematic characters: 17 problematic tags in the bigger sample data and 2 problematic tags in the smaller sample data
* Incomplete data: Some areas missing data, like postcode, country, etc.
  ```html
  <tag k="addr:city" v="Helsingborg" />
  <tag k="addr:street" v="Tågagatan" />
  <tag k="addr:country" v="SE" />
  <tag k="addr:postcode" v="252 22" />
  <tag k="source:address" v="Helsingborgs kommun" />
  <tag k="addr:housenumber" v="18C" />
  ```
  ```html
  <tag k="addr:city" v="Lund" />
  <tag k="addr:street" v="Hospitalsgatan" />
  <tag k="addr:country" v="SE" />
  <tag k="addr:housenumber" v="3" /> 
  ```
* Inconsistent postal code format:
  ```html
  <tag k="addr:postcode" v="26253" />
  <tag k="addr:postcode" v="262 63" />
  <tag k="addr:postcode" v="262 80" />
  <tag k="addr:postcode" v="23691" />
  ```
#### General information for extracted data
Before turning the data into JSON, I excluded all the problemtic strings, the duplicated information and turned all the existed Swedish postal codes into a standard format, for instance, "26253" becomes "262 53", etc. Once the data was imported to MongoDB, some basic querying revealed that this metro extract included the areas outside Skåne and there were some missing data in postcode, country, etc.

```python
# Sort countries by count 
countries=db.nodes.aggregate([{"$group":{"_id":"$address.country", "count":{"$sum":1}}}])
for co in countries:
    print co
```
{u'count': 131098, u'_id': u'SE'}    
{u'count': 269198, u'_id': u'DK'}    
{u'count': 5830732, u'_id': None}  

```python
# Check if there are missing data in cities for Region Skåne
cities=db.nodes.aggregate([{"$match":{"$and":[{"address.country":{"$eq":'SE'}}, {"address.city":{"$eq": None}}]}}, {"$group":{"_id":"$address.city", "count":{"$sum":1}}}])
for cit in cities:
    print cit    
```
{u'count': 8765, u'_id': None}

```python
# Check if there are missing data in postcodes for Region Skåne
posts=db.nodes.aggregate([{"$match":{"$and":[{"address.country":{"$eq":'SE'}}, {"address.postcode":{"$eq": None}}]}}, {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}])
for po in posts:
    print po    
```
{u'count': 82633, u'_id': None}

These outputs confirmed the inclusion of surrounding cities in Denmark and missing/incompleted data in country, city and postal code for Region Skåne.

#### Postal codes

```python
# Sort postcodes by count, descending 
post=db.nodes.aggregate([{"$group":
{"_id":"$address.postcode", "count":{"$sum":1}}}, {"$sort":{"count": -1}}, {"$limit":3}])
for pid in post:
    print pid
```
{u'count': 6181982, u'_id': None}  
{u'count': 1004, u'_id': u'241 35'}    
{u'count': 764, u'_id': u'212 31'}    

When grouped together with this query, a huge amount of unwanted or missing postal codes surfaced besides confirming the standardization of all the inconsistent Swedish postal codes.

### Data Overview
This section contains basic statistics about the Skåne OpenStreetMap dataset and the MongoDB queries used to gather them.
File size
* SkåneMap.osm --------- 1.31G
* SkåneMap.osm.json --------- 1.39G

```python
# Number of documents
print db.nodes.find().count()
```
6231028

```python
# Number of nodes
print db.nodes.find({"type":"node"}).count()
```
5502191

```python
# Number of ways
print db.nodes.find({"type":"way"}).count()
```
728789

```python
# Number of unique users
print len(db.nodes.distinct("created.user"))
```
2618

```python
# Top 1 contributing users for Region Skåne 
contr_users=db.nodes.aggregate([{"$match":{"address.country":{"$eq":'SE'}}}, {"$group":{"_id":"$created.user", "count":
{"$sum":1}}}, {"$sort":{"count": -1}}, {"$limit":1}])
for top_user in contr_users:
    print top_user
```

```python
# Number of users appearing only once (having 1 post) for Regoin Skåne
contr_users=db.nodes.aggregate([{"$match":{"address.country":{"$eq":'SE'}}}, {"$group":{"_id":"$created.user", "count":
{"$sum":1}}}, {"$group":{"_id":"$count", "num_users":{"$sum":1}}}, {"$sort":
{"_id":1}}, {"$limit":1}])
for top_user in contr_users:
    print top_user

# “_id” represents postcount
```
{u'num_users': 84, u'_id': 1}

### Additional Ideas
#### Additional data exploration using MongoDB queries

```python
# Top 10 appearing amenities for Region Skåne
amenities=db.nodes.aggregate([{"$match":{"address.country":{"$eq":'SE'}, "amenity":{"$exists":1}}}, {"$group":
{"_id":"$amenity",
"count":{"$sum":1}}}, {"$sort":{"count": -1}}, {"$limit":10}])
for ame in amenities:
    print ame
```
 {u'count': 170, u'_id': u'restaurant'}  
 {u'count': 73, u'_id': u'place_of_worship'}  
 {u'count': 65, u'_id': u'fast_food'}  
 {u'count': 57, u'_id': u'cafe'}  
 {u'count': 54, u'_id': u'school'}  
 {u'count': 45, u'_id': u'kindergarten'}  
 {u'count': 45, u'_id': u'fuel'}  
 {u'count': 17, u'_id': u'bank'}  
 {u'count': 15, u'_id': u'pharmacy'}  
 {u'count': 15, u'_id': u'library'}  

```python 
# Top 5 popular cuisines for Region Skåne
cuisines=db.nodes.aggregate([{"$match":{"$or":[{"address.country":{"$eq":'SE'}}, {"address.postcode":{"$ne":None}}], "$and":[{"amenity":{"$exists":1}, "amenity":"restaurant"}, {"cuisine":{"$ne":None}}]}}, {"$group":{"_id":"$cuisine", "count":
{"$sum":1}}}, {"$sort":{"count": -1}}, {"$limit":5}])
for cuis in cuisines:
    print cuis
```
 {u'count': 30, u'_id': u'pizza'}  
 {u'count': 21, u'_id': u'regional'}  
 {u'count': 9, u'_id': u'thai'}  
 {u'count': 6, u'_id': u'italian'}  
 {u'count': 5, u'_id': u'indian'}  

```python
# Top 10 cities with the highest number and percentages of wheelchair access in Skåne 
wheel_percentages=db.nodes.aggregate([{"$match":{"$and":[{"address.country":{"$eq":'SE'}}, {"wheelchair":{"$exists":1}, "wheelchair":"yes"}, {"address.city":{"$ne":None}}]}}, {"$group":{"_id":"$address.city", "count":
{"$sum":1}}}, {"$sort": {"count": -1}}, {"$limit":10}, { "$group" : {  "_id" : 0,
         "cities" : { "$push" : "$_id" },
         "totalCount" : { "$push" : "$count" },
         "total" : { "$sum" : "$count" } }
     }, { "$project" : {
         "cities" : "$cities",
         "totalCount" : "$totalCount",
         "percentages" : { "$map" : { "input" : "$totalCount", "as" : "s",
"in" : { "$divide" : ["$$s", "$total"] } } } }
     }])
for wp in wheel_percentages:
    pprint.pprint(wp)
```
```
{u'_id': 0,
 u'cities': [u'Lund',
             u'Malm\xf6',
             u'Helsingborg',
             u'Sj\xf6bo',
             u'Ystad',
             u'Kristianstad',
             u'Lomma',
             u'Dalby',
             u'Esl\xf6v',
             u'S\xf6dra Sandby'],
 u'percentages': [0.4,
                  0.232,
                  0.112,
                  0.064,
                  0.04,
                  0.04,
                  0.04,
                  0.024,
                  0.024,
                  0.024],
 u'totalCount': [50, 29, 14, 8, 5, 5, 5, 3, 3, 3]}
```
As a student town, Lund stands out to be the top one in wheelchair access, which makes a lot of sense.

#### Visulization in user percentages and wheelchair accessibility

```python
# Pie chart for top 5 contributing user percenatages for Region Skåne
import matplotlib.pyplot as plt
# Data to plot
contr_users=db.nodes.aggregate([{"$match":{"address.country":{"$eq":'SE'}}}, {"$group":{"_id":"$created.user", "count":
{"$sum":1}}}, {"$sort":{"count": -1}}, { "$group" : {  "_id" : 0,
         "users" : { "$push" : "$_id" },
         "totalCount" : { "$push" : "$count" },
         "total" : { "$sum" : "$count" } }
     }, { "$project" : {
         "users" : "$users",
         "totalCount" : "$totalCount",
         "percentages" : { "$map" : { "input" : "$totalCount", "as" : "s",
"in" : { "$divide" : ["$$s", "$total"] } } } }
     }])

for top_user in contr_users:
    users=top_user['users'][0:5]
    percentages=top_user['percentages'][0:5]
    users.append('Others')
    percentages.append(1-sum(percentages))
 
    # Plot
    plt.pie(percentages, explode=(0.05, 0.05, 0.05, 0.15, 0.05, 0), labels=users,
        autopct='%1.1f%%', shadow=False, startangle=120)

    plt.axis('equal')
    plt.show()
```
![Top5ContributingUserPercentage](https://github.com/swfi/OpenStreetMap/blob/master/PieChart_ContributingUser.jpg)

It appears that more than half of the data contribution was made by one user named 'Grillo', which might display either incorrectnesses in data collection on user contribution or less user engagement. To fix the possible issues in data collection, we could enhance the way that records were captured perhaps by using something like ALLCapture. In this way, all the activities would be recorded no matter which channel used for editting maps. In terms of user engagement, there are a number of ways to increase it. For instance, highlighting recent activity would help users quickly get an overview of what's going on across the dataset, which would be more likely to increase user participation. Another way is to provide certain types of recognition to contributors based on the amount of contributions made. Although monetary rewards are considered to have a strong impact on human motivation and performance, non-monetary rewards, like user ranks or experience levels should work as well. Once users feel their contributions recognized, they will most likely get more motivated to keep up the good work. However, if OpenStreetMap, as an open database, uses commercial software, like ALLCapture or monetary/non-monetary rewards, extra expense will be unavoidable. And adding extra features, like showing recent activities, setting up user ranks/ experience levels would require extra site maintenance. All of these seem not very practical to an open source, though it could be solved by getting more funding.

```python
# Pie chart for top 5 cities/towns with highest percenatages of wheelchair access in Skåne

# Data to plot
wheel_percentages=db.nodes.aggregate([{"$match":{"$and":[{"address.country":{"$eq":'SE'}}, {"wheelchair":{"$exists":1}, "wheelchair":"yes"}, {"address.city":{"$ne":None}}]}}, {"$group":{"_id":"$address.city", "count":
{"$sum":1}}}, {"$sort": {"count": -1}}, { "$group" : {  "_id" : 0,
         "cities" : { "$push" : "$_id" },
         "totalCount" : { "$push" : "$count" },
         "total" : { "$sum" : "$count" } }
     }, { "$project" : {
         "cities" : "$cities",
         "percentages" : { "$map" : { "input" : "$totalCount", "as" : "s",
"in" : { "$divide" : ["$$s", "$total"] } } } }
     }])

for wp in wheel_percentages:
    cities=wp['cities'][0:5]
    percentages=wp['percentages'][0:5]
    cities.append('Others')
    percentages.append(1-sum(percentages))
    
    # Plot
    plt.pie(percentages, explode=(0.05, 0, 0, 0, 0, 0), labels=cities,
        autopct='%1.1f%%', shadow=False, startangle=120)
 
    plt.axis('equal')
    plt.show()
 ```
 ![Top5WheelchairAccess](https://github.com/swfi/OpenStreetMap/blob/master/PieChart_WheelchairAccess.jpg)
 
Due to missing data in variable 'country', those cities that belong to Skåne were left out by the query. Therefore, this pie chart just displayed a rough overview of the wheelchair accessibility in Skåne. One way to improve this is to add data entry restrictions to the OpenStreetMap dataset. Once some missing data exists, data submission won't go through and a pop-up message will be displayed to explain what needs to be fixed. In this way, users would most likely submit completed data. Meanwhile, using the data from Lantmäteriet, the Swedish National Land Survey, could add more detailed and completed land information to the dataset.

### Conclusion

Although the Skåne OpenStreetMap dataset is large yet uncompleted, the data has been relatively cleaned for the purposes of this project. It would have avoided extracting unwanted area in Denmark if the coordinates were used to get polygon boundires on Skåne. Through several MongoDB queries, I got a better overview of Skåne. It is obvious that the dataset is very useful, though there are areas for improvement. For instance, using review or setting practical data accuracy goals can improve data entry accuracy. Working with a more robust data processor can improve data processing efficiency.

### References

[Aggregation - Ratio/Percentage of Total. Grokbase.](http://grokbase.com/t/gg/mongodb-user/1492v7dk19/aggregation-ratio-percentage-of-total)  
Aguinis, H., Joo, H. & Gottfredson, R. K. (2013). What monetary rewards can and cannot do: How to show employees the money. Business Horizons, 56, 241—249.  
[ALLCapture.](http://www.allcapture.com/eng/index.php)  
[Markdown-Cheatsheet. Github.](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)  
[Matplotlib Pie chart. Python Tutorials.](https://pythonspot.com/en/matplotlib-pie-chart/)  
[MongoDB Manual. MongoDB.](https://docs.mongodb.com/manual/)  
[Lantmateriet.](https://www.lantmateriet.se/en/About-Lantmateriet/About-us/Anvand-var-information/)  
