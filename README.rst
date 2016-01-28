scrapy-dblite
=============

**The component is not supported anymore**. As alternative, you can use `ownport/scrapy-rethinkdb <https://github.com/ownport/scrapy-rethinkdb>`_, forked from `sprij/scrapy-rethinkdb <https://github.com/sprij/scrapy-rethinkdb>`_


Simple library for storing `Scrapy Items <http://doc.scrapy.org/en/latest/topics/items.html>`_ in sqlite. There's no special requirements or dependencies for using this library but main goal of dblite is working together with `Scrapy <http://scrapy.org/>`_ - a fast high-level screen scraping and web crawling framework, used to crawl websites and extract structured data from their pages.

According to `Scrapy documentation <http://doc.scrapy.org/en/latest/>`_ Item objects are simple containers used to collect the scraped data. They provide a dictionary-like API with a convenient syntax for declaring their available fields.::

    from scrapy.item import Item, Field

    class Product(Item):
        _id     = Field()
        name    = Field()
        price   = Field()

For more information about Scrapy Items please read `documentation <http://doc.scrapy.org/en/latest/topics/items.html>`_. Item and Field classes also included in dblite library but there's no need to use them. It's just simplifed version of Scrapy's classes. 

The *_id* field is required to be defined for Item(). Most probably you will never use this directly but dblite is used for own logic: *_id* equals *rowid* in sqlite database.

Item & Field classes defintions in dblite described in `Items specification <https://github.com/ownport/scrapy-dblite/blob/master/docs/items.md>`_ 

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

More detail information about dblite can be founded in `docs/dblite-api <https://github.com/ownport/scrapy-dblite/blob/master/docs/dblite-api.md>`_ document

Installation
------------

To install scrapy-dblite directly from github::
    
    pip install git+https://github.com/ownport/scrapy-dblite.git

or install from `PyPI - the Python Package Index <https://pypi.python.org/pypi>`_::

    pip install scrapy-dblite

Change log
----------
Change log for dblite is based on `GitHub Milestones <https://github.com/ownport/scrapy-dblite/issues/milestones>`_

How to use scrapy-dblite with Scrapy
------------------------------------
Using dblite in Item Pipeline::
    
    from scrapy.exceptions import DropItem
    from myproject.items import Product
    import dblite

    class StoreItemsPipeline(object):
        def __init__(self):
            self.ds = None
        
        def open_spider(self, spider):
            self.ds = dblite.open(Product, 'sqlite://db/products.sqlite:items', autocommit=True)

        def close_spider(self, spider):
            self.ds.close()

        def process_item(self, item, spider):           
            if isinstance(item, Product):
                try:
                    self.ds.put(item)
                except dblite.DuplicateItem:
                    raise DropItem("Duplicate item found: %s" % item)
            else:
                raise DropItem("Unknown item type, %s" % type(item))
            return item

For developers
--------------

Creation of development environment::

    $ git clone https://github.com/ownport/scrapy-dblite.git
    $ cd scrapy-dblite
    $ docker build -t 'scrapy-dblite:dev' .
    $ docker run -ti --rm --name 'scrapy-dblite' -v $(pwd):/data/scrapy-dblite scrapy-dblite:dev /data/bin/run-as.sh dev 1000 /bin/sh

    $ cd /data/scrapy-dblite/

Perform unit tests::

    $ make test-all              
    ........................................................
    ----------------------------------------------------------------------
    Ran 56 tests in 7.407s

    OK
    $
    $ make test-all-with-coverage
    .........................................................
    Name                 Stmts   Miss  Cover   Missing
    --------------------------------------------------
    dblite                 207      3    99%   285, 344-345
    dblite.item             46      2    96%   84, 89
    dblite.query            80      0   100%   
    dblite.serializers      27      0   100%   
    dblite.settings          2      0   100%   
    --------------------------------------------------
    TOTAL                  362      5    99%   
    ----------------------------------------------------------------------
    Ran 57 tests in 7.923s

    OK

