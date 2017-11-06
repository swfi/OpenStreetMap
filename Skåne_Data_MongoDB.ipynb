# OpenStreetMap Data Wrangling with MongoDB

### Map Area

Skåne, Sweden

* https://www.openstreetmap.org/relation/54409#map=8/55.837/13.126
* https://mapzen.com/data/metro-extracts/your-extracts/e6c75631ddab

So why this area? First, I'm interested to know how it looks like around Skåne. Second, this regoin seems unpopular, which could most probably generate uncompleted data. Therefore, it would be worth the effort to get started to work on the data somehow.

### Problems Encountered in the Selected Region

After exploring a sample size of the Skåne area via audit.py, I noticed the following main problems with the data, discussed as follows:

* Incorrect extract area: extracted some regional data from Denmark, taking the following as an example:
   <tag k="addr:country" v="DK" />   
* Duplicated information: the same information was pulled from OSAK Danish database, e.g. 'osak:house_no' and 'addr:housenumber', 'osak:street_name' and 'addr:street'.
  <tag k="addr:street" v="Give Alle" />
  <tag k="osak:house_no" v="12" />

  <tag k="addr:housenumber" v="12" />
  <tag k="osak:street_name" v="Give Alle" />
* Problematic characters: 17 problematic tags in the bigger sample data and 2 problematic tags in the smaller sample data
* Incomplete data: Some areas missing data, like postcode, country, etc.
  '''
  <tag k="addr:city" v="Helsingborg" />
  <tag k="addr:street" v="Tågagatan" />
  <tag k="addr:country" v="SE" />
  <tag k="addr:postcode" v="252 22" />
  <tag k="source:address" v="Helsingborgs kommun" />
  <tag k="addr:housenumber" v="18C" />

  '''
  <tag k="addr:city" v="Lund" />
  <tag k="addr:street" v="Hospitalsgatan" />
  <tag k="addr:country" v="SE" />
  <tag k="addr:housenumber" v="3" />   
* Inconsistent postal code format:
  <tag k="addr:postcode" v="26253" />
  <tag k="addr:postcode" v="262 63" />
  <tag k="addr:postcode" v="262 80" />
  <tag k="addr:postcode" v="23691" />
  
### General information for extracted data
Before turning the data into JSON, I excluded all the problemtic strings, the duplicated information and turned all the existed Swedish postal codes into a standard format, for instance, "26253" becomes "262 53", etc. Once the data was imported to MongoDB, some basic querying revealed that this metro extract included the areas outside Skåne and there were some missing data in postcode, country, etc.

```DB
# Sort countries by count 
countries=db.nodes.aggregate([{"$group":{"_id":"$address.country", "count":{"$sum":1}}}])
for co in countries:
    print co
```
* {u'count': 131098, u'_id': u'SE'}
* {u'count': 269198, u'_id': u'DK'}
* {u'count': 5830732, u'_id': None}

```MongoDB

# Check if there are missing data in cities for Region Skåne
cities=db.nodes.aggregate([{"$match":{"$and":[{"address.country":{"$eq":'SE'}}, {"address.city":{"$eq": None}}]}}, {"$group":{"_id":"$address.city", "count":{"$sum":1}}}])
for cit in cities:
    print cit
    
```
* {u'count': 8765, u'_id': None}

```MongoDB

# Check if there are missing data in postcodes for Region Skåne
posts=db.nodes.aggregate([{"$match":{"$and":[{"address.country":{"$eq":'SE'}}, {"address.postcode":{"$eq": None}}]}}, {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}])
for po in posts:
    print po
    
```
* {u'count': 82633, u'_id': None}

These outputs confirmed the inclusion of surrounding cities in Denmark and missing/incompleted data in country, city and postal code for Region Skåne.

