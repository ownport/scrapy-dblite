scrapy-dblite
=============

Simple library for storing `Scrapy Items <http://doc.scrapy.org/en/latest/topics/items.html>`_ in sqlite. There's no special requirements or dependencies for using this library but main goal of dblite is working together with `Scrapy <http://scrapy.org/>`_ - a fast high-level screen scraping and web crawling framework, used to crawl websites and extract structured data from their pages.

According to `Scrapy documentation <http://doc.scrapy.org/en/latest/>`_ Item objects are simple containers used to collect the scraped data. They provide a dictionary-like API with a convenient syntax for declaring their available fields.::

	from scrapy.item import Item, Field

	class Product(Item):
	    _id 	= Field()
	    name 	= Field()
	    price 	= Field()

For more information about Scrapy Items please read `documentation <http://doc.scrapy.org/en/latest/topics/items.html>`_. Item and Field classes also included in dblite library but there's no need to use them. It's just simplifed version of Scrapy's classes. 

The *_id* field is required to be defined for Item(). Most probably you will never use this directly but dblite is used for own logic: *_id* equals *rowid* in sqlite database.

Working with storage
--------------------
The simplest way to open sqlite database for storing Scrapy items is use *open()*::

	>>> import dblite
	>>> ds = dblite.open(Product, 'sqlite://tests/db/test-db.sqlite:test_tbl')
	>>> ds
	<dblite.Storage object at 0x17e1f10>
	>>> ds.fieldnames
	set(['price', '_id', 'name'])

All manipulations with Items are performed via 3 methods: get(), put(), delete()::

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

More detail information about dblite can be founded in [docs/dblite-api](https://github.com/ownport/scrapy-dblite/blob/master/docs/dblite-api.md) document

How to use scrapy-dblite with Scrapy
------------------------------------
::
	>>>

