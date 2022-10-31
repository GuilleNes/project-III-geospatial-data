

# ***PROJECT 3.0 - geospatial-data***


![](../images/portada.jpg)


***Guillermo Nespral***







**1. INTRODUCTION**
   
_______________________________________

 - **GOAL OF THE PROJECT**



>The main goal of this project is finding the best spot to place our new company, based on some requirements from our employees and with the best enviroment to grow. 




>To collect all the information, I have used a MongoDB with companies from Crunchbase and a Foursquare API where I have found all the information about the cities facilities.

>In order to get and clean all the data, I have created a [main](https://github.com/GuilleNes/project-III-geospatial-data/blob/main/src/Main.ipynb) document and a [functions](https://github.com/GuilleNes/project-III-geospatial-data/blob/main/src/functions.py) document where all the code has been saved.


**1. CLEANING PROCESS**

First of all we connect with the MongoDB and extracting the data based on two of the requirements that are directly related to other companies:

- *Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.*
- *Developers like to be near successful tech startups that have raised at least 1 Million dollars.*

According to this, we established the filters for the DB and looked for the companies that adjusted to the requirement. After this I had a dataframe of 385 different companies.
  
```ruby
condition_one = {"description": {"$regex": "design"}}
condition_two = {"tag_list": {"$regex": "design"}}
condition_three = {"name": {"$regex": "design"}}
condition_four = {"category_code": {"$regex": "design"}}
condition_five = {"total_money_raised": {"$regex": "M"}}
condition_six = {"total_money_raised": {"$regex": "B"}}

projection = {"name": 1, "number_of_employees": 1, "offices": 1,"_id":0}
result = list(c.find({
    "$or": [condition_one, condition_two, condition_three, condition_four, condition_five, condition_six],
    "number_of_employees": {"$gte": 100}
}, projection))


df = pd.DataFrame(result)
```

After making a value count based on the different cities, I decided to base my search on 5 different cities: **San Francisco, Seattle, Chicago, London and Cambridge(USA)**

This decision is based on the fact that they are some of the cities with most companies and they are located in different areas.

The next step I took was searching the different locations thar our employees required (starbucks, pet grooming, basketball court, airports). I did it separately by city and category. I chose a random location in each city to set the company and looked for the facilities around.

```ruby
starbucks_SF = fun.get_results("starbucks", San_Francisco, 10, 3000, token_foursquare)
df_SF = fun.clean_results_first(starbucks_SF, "Coffee")

starbucks_SE = fun.get_results("starbucks", Seattle, 10, 3000, token_foursquare)
df_SE = fun.clean_results_first(starbucks_SE, "Coffee")

starbucks_LO = fun.get_results("starbucks", London, 10, 3000, token_foursquare)
df_LO = fun.clean_results_first_lo(starbucks_LO, "Coffee")

starbucks_CA = fun.get_results("starbucks", Cambridge, 10, 3000, token_foursquare)
df_CA = fun.clean_results_first(starbucks_CA, "Coffee")

starbucks_CH = fun.get_results("starbucks", Chicago, 10, 3000, token_foursquare)
df_CH = fun.clean_results_first(starbucks_CH, "Coffee")
```
Next, I created the base map in order to add the diferent layers on it for each city:

```ruby
SF_map = Map(location = San_Francisco, zoom_start = 12)
SE_map = Map(location = Seattle, zoom_start = 12)
LO_map = Map(location = London, zoom_start = 12)
CA_map = Map(location = Cambridge, zoom_start = 12)
CH_map = Map(location = Chicago, zoom_start = 12)

fun.mapping_results(df_SF, SF_map)
fun.mapping_results(df_SE, SE_map)
fun.mapping_results(df_LO, LO_map)
fun.mapping_results(df_CA, CA_map)
fun.mapping_results(df_CH, CH_map)
```

![Seattle](https://github.com/GuilleNes/project-III-geospatial-data/blob/main/images/Seattle.jpg)

[MAP](https://guillenes.github.io./)


<iframe id="inlineFrameExample"
    title="Inline Frame Example"
    width="600"
    height="400"
    src="https://guillenes.github.io./">
</iframe>

![giphy](https://user-images.githubusercontent.com/112824189/199121838-f8ecd2ac-9694-49da-b0aa-ac59b4a81428.gif)

Finally, in order to to get the final result for each city, we just apply a simple math formulation to the grouped data for each city. To this calculation we multiplied the value of the wheight of each category to get the final selected city.



...and it was......

![giphy (1)](https://user-images.githubusercontent.com/112824189/199121870-be39196d-d9ca-4a11-80c5-868cff17642f.gif)








  













