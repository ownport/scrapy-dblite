Declaring Items
---------------
Items are declared using a simple class definition syntax and Field objects::

    from scrapy.item import Item, Field

    class Product(Item):
        name = Field()
        price = Field()

Item Fields
-----------
Field objects are used to specify metadata for each field. [Scrapy](http://scrapy.org/) allows you to specify any kind of metadata for each field. There is no restriction on the values accepted by Field objects. For this same reason, there isn’t a reference list of all available metadata keys. Each key defined in Field objects could be used by a different components, and only those components know about it. 

