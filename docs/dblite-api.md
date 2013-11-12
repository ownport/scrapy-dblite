### Storing Items in sqlite
```python
>>> p1 = Product(name='Laptop', price=1000)
>>> p2 = Product(name='Nettop', price=100)
>>> p3 = Product(name='Desktop PC', price=500)
>>> ds.put(p1)
>>> ds.put([p2,p3])
>>> [p for p in ds.get()]
[{'_id': 1, 'name': u'Laptop', 'price': 1000}, 
{'_id': 2, 'name': u'Nettop', 'price': 100}, 
{'_id': 3, 'name': u'Desktop PC', 'price': 500}]
```

### Update items 

dblite supports updating items but for that you need to know `_id` of item
```python
>>> p1 = Product(name='Leptop', price=1000)
>>> ds.put(p1)
>>> [p for p in ds.get()]
[{'_id': 1, 'name': u'Leptop', 'price': 1000}]
>>> for p in ds.get({'name': 'Leptop'}):
...		p['name'] = 'Laptop'
...     ds.put(p)
...
>>> [p for p in ds.get()]
[{'_id': 1, 'name': u'Laptop', 'price': 1000}]
>>> 
```

### Select Items
Select all items from sqlite
```python
>>> [p for p in ds.get()]
[{'_id': 1, 'name': u'Laptop', 'price': 1000}, 
{'_id': 2, 'name': u'Nettop', 'price': 100}, 
{'_id': 3, 'name': u'Desktop PC', 'price': 500}]
```

Selecting items by equality conditions
```python
>>> [p for p in ds.get({'name': u'Laptop'})]
[{'_id': 1, 'name': u'Laptop', 'price': 1000}]
```

To specify condition, use `{<field>: <value>}` to select all items that contain the `<field>` with the specified `<value>`

You can also specify more than one field with logical AND conjunction
```python
>>> [p for p in ds.get({'name': u'Laptop', 'price': 1000})]
[{'_id': 1, 'name': u'Laptop', 'price': 1000}]
```

There's another way how to use AND conjunction
```python
>>> [p for p in ds.get({'$and': {'name': u'Nettop', 'price': 100}})]
[{'_id': 2, 'name': u'Nettop', 'price': 100}]
```

By using `$or` operator, you can select items with logical OR conjunction
```python
>>> [p for p in ds.get({'$or': [{'price': 100}, {'price': 1000}]})]
[{'_id': 1, 'name': u'Laptop', 'price': 1000},
{'_id': 2, 'name': u'Nettop', 'price': 100}] 
>>> [p for p in ds.get({'$or': [{'name': 'Laptop'}, {'name': 'Desktop PC'}]})]
[{'_id': 1, 'name': u'Laptop', 'price': 1000}, 
{'_id': 3, 'name': u'Desktop PC', 'price': 500}]
```

Time to time there's no need to get all results. You can limit the amount of items returned by get() with `limit` parameter:
```python
>>> for product in products.get(limit=5):
...		print product
...
[{'_id': 1, 'name': u'Laptop', 'price': 1000}, 
{'_id': 2, 'name': u'Nettop', 'price': 100}, 
{'_id': 3, 'name': u'Desktop PC', 'price': 500},
{'_id': 4, 'name': u'Tablet', 'price': 300},
{'_id': 5, 'name': u'Smartphone', 'price': 200}]
```

In case when you need to get details just for one item, get(limit=1) returns Item object but not the list
```python
>>> ds.get(limit=1)
{'_id': 1, 'name': u'Laptop', 'price': 1000}
```

#### ORDER BY

The `$orderby` operator sorts the results of a query in ascending or descending order. Specify 
a value to $orderby of negative one (e.g. -1, as above) to sort in descending order or a positive 
value (e.g. 1) to sort in ascending order.
```python
ds.get({'$orderby': {'product_name': -1}})
```
is equivalent for SQL 
```sql
SELECT rowid, * FROM products ORDER BY product_name DESC; 
```


dblite support LIKE and REGEXP syntax for selection items

#### LIKE
```python
ds.get( 'product_name': '/%book%/' )
```
is equivalent for SQL 
```sql
SELECT rowid, * FROM products WHERE product_name LIKE '%book%'; 
```

#### REGEXP
```python
ds.get( 'product_id': 'r/code-\d+/' )
```
is equivalent for SQL 
```sql
SELECT rowid, * FROM products WHERE product_id REGEXP 'code-\d+'; 
```

The REGEXP operator is a special syntax for the _regexp() user function. 

#### None values
```python
ds.get( 'product_id': None )
```
is equivalent for SQL 
```sql
SELECT rowid, * FROM products WHERE product_id ISNULL; 
```

### Delete items
For deleting items you can specify as argument Item object 
```python
>>> [p for p in ds.get({'name': u'Laptop'})]
[{'_id': 1, 'name': u'Laptop', 'price': 1000}]
>>> for p in ds.get({'name': 'Laptop'}):
...		ds.delete(p)
...
>>> [p for p in ds.get({'name': u'Laptop'})]
[]
>>>
```

or conditions the same as for selecting items
```python
>>> [p for p in ds.get({'$or': [{'price': 100}, {'price': 500}]})]
[{'_id': 2, 'name': u'Nettop', 'price': 100},
{'_id': 3, 'name': u'Desktop PC', 'price': 500}]
>>> ds.delete({'$or': [{'price': 100}, {'price': 500}]}) 
>>> [p for p in ds.get({'$or': [{'price': 100}, {'price': 500}]})]
[]
>>>
```

or you can delete all items by
```python
>>> ds.delete(_all=True)
>>>
```

### Direct SQL requests

Many of operations with data is not supported via dblite API at this moment but you can use `sql()` method for direct SQL requests to database. For all SELECT requests dblite will try to rerurn the result as list of Item objects

```python
>>> ds.sql('INSERT INTO product (name, price, catalog_url) VALUES (?,?,?)', ('Laptop', 1000, 'http://catalog/1'))
>>> [p for p in ds.sql('SELECT rowid, * FROM product;')]
[{'_id':1, 
  'name': 'Laptop', 
  'price': 1000, 
  'catalog_url': 'http://catalog/1'}]
```

### copy() function

copy items one database to another one (when source and target items are the same)
```python
source = (SourceItem, 'sqlite://data/source.sqlite:data')
target = (TargetItem, 'sqlite://data/target.sqlite:data')
dblite.copy(source, target)
```

copy items with transformation
```python
source = (SourceItem, 'sqlite://data/source.sqlite:data')
target = (TargetItem, 'sqlite://data/target.sqlite:data')

def transform(item):
    # code for item fields transformation ... 
    return item
dblite.copy(source, target, transform=transform)
```

