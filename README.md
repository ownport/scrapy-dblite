scrapy-dblite
=============

Simple library for storing [Scrapy Items](http://doc.scrapy.org/en/latest/topics/items.html) in sqlite 

According to Scrapy documentation Item objects are simple containers used to collect the scraped data. They provide a dictionary-like API with a convenient syntax for declaring their available fields.

```python
from scrapy.item import Item, Field

class Product(Item):
    name = Field()
    price = Field()
    stock = Field()
    last_updated = Field(serializer=str)
```

For more information about Scrapy Items please read [documentation](http://doc.scrapy.org/en/latest/topics/items.html)

## Working with storage

The simplest way to open sqlite database for storing Scrapy items is use `open()`

```python
import dblite
ds = dblite.open('sqlite://tests/db/test-db.sqlite:test_tbl', Product)
```


## Similar projects

- [https://github.com/noplay/scrapy-mongodb](Mongodb support for scrapy)

