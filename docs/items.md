Declaring Items
---------------
Items are declared using a simple class definition syntax and Field objects::

```python
from scrapy.item import Item, Field

class Product(Item):
    _id = Field()
    name = Field()
    price = Field()
```

Item Fields
-----------
Field objects are used to specify metadata for each field. [Scrapy](http://scrapy.org/) allows you to specify any kind of metadata for each field. There is no restriction on the values accepted by Field objects. For this same reason, there isn’t a reference list of all available metadata keys. Each key defined in Field objects could be used by a different components, and only those components know about it. 

Item Field definitions in dblite
---------------------------------
Let's review how Items and Fields classes mapped to sqlite scheme. For above example with Product class, dblite will create the next table:

```sql
CREATE TABLE IF NOT EXISTS <table name> (name, price);
```
The value of `table name` will be taken from uri parameter.

Unlike most SQL databases, SQLite does not restrict the type of data that may be inserted into a column based on the columns declared type. Instead, SQLite uses dynamic typing. That's a reason why there's no need to define type of the fields.

