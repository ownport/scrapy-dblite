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