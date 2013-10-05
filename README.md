scrapy-dblite
=============

Simple library for storing [Scrapy Items](http://doc.scrapy.org/en/latest/topics/items.html) in sqlite 

According to Scrapy documentation Item objects are simple containers used to collect the scraped data. They provide a dictionary-like API with a convenient syntax for declaring their available fields.

```python
from scrapy.item import Item, Field

class Product(Item):
    _id 	= Field()
    name 	= Field()
    price 	= Field()
```

For more information about Scrapy Items please read [documentation](http://doc.scrapy.org/en/latest/topics/items.html). There's no need to use Item and Field classes provided by dblite library. It's just simplifed version of Scrapy's classes. The `_id` field is required to be defined for Item(). Most probably you will never use this directly but dblite is used for own logic: `_id` equals `rowid` in sqlite database.

## Working with storage

The simplest way to open sqlite database for storing Scrapy items is use `open()`

```python
>>> import dblite
>>> ds = dblite.open(Product, 'sqlite://tests/db/test-db.sqlite:test_tbl')
>>> ds
<dblite.Storage object at 0x17e1f10>
>>> ds.fieldnames
set(['price', '_id', 'name'])
```

All manipulations with Items are performed via 3 methods: get(), put(), delete()

```python
>>> p1 = Product(name='Laptop', price=1000)
>>> p1
{'name': 'Laptop', 'price': 1000}
>>> ds.put(p1)
>>> [product for product in ds.get()]
[{'_id': 1, 'name': u'Laptop', 'price': 1000}]
>>> ds.delete(p1)
>>> [i for i in ds.get()]
[]
>>>
```
## Storing Items in sqlite

```python
>>> p1 = Product(name='Laptop', price=1000)
>>> p2 = Product(name='Nettop', price=100)
>>> p3 = Product(name='Desktop PC', price=500)
>>> ds.put(p1)
>>> ds.put([p2,p3])
>>> [p for p in ds.get()]
[{'_id': 1, 'name': u'Laptop', 'price': 1000}, {'_id': 2, 'name': u'Nettop', 'price': 100}, {'_id': 3, 'name': u'Desktop PC', 'price': 500}]
```

## Similar projects

- [https://github.com/noplay/scrapy-mongodb](Mongodb support for scrapy)

