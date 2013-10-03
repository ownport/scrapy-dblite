scrapy-dblite
=============

Simple library for storing [Scrapy Items](http://doc.scrapy.org/en/latest/topics/items.html) in sqlite 

According to Scrapy documentation Item objects are simple containers used to collect the scraped data. They provide a dictionary-like API with a convenient syntax for declaring their available fields.

```python
from scrapy.item import Item, Field

class Product(Item):
    name = Field()
    price = Field()
```

For more information about Scrapy Items please read [documentation](http://doc.scrapy.org/en/latest/topics/items.html)

## Working with storage

The simplest way to open sqlite database for storing Scrapy items is use `open()`

```python
>>> import dblite
>>> ds = dblite.open(Product, 'sqlite://tests/db/test-db.sqlite:test_tbl')
>>> ds
<dblite.Storage object at 0x17e1f10>
>>> ds.fieldnames
set(['price', 'name'])
```

All manipulations with Items are performed via 3 methods: get(), put(), delete()

```python
>>> p1 = Product(name='Laptop', price=1000)
>>> p1
{'name': 'Laptop', 'price': 1000}
>>> ds.put(p1)
>>> [i for i in ds.get()]
[(1, {'name': u'Laptop', 'price': 1000})]
>>> ds.delete({'rowid':1})
>>> [i for i in ds.get()]
[]
>>>
```

## Similar projects

- [https://github.com/noplay/scrapy-mongodb](Mongodb support for scrapy)

