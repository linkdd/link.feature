Tutorial
--------

This package is used to make classes providing features.
A feature is a class, providing an API using the class' instance.

For example:

.. code-block:: python

   from link.feature import Feature
   import json


   class JSONFeature(Feature):
       name = 'json'

       def to_json(self):
           return json.dumps(self.obj.data)

Then, we just have to add the feature to the class, using the decorator:

.. code-block:: python

   from link.feature import addfeatures


   @addfeatures([JSONFeature])
   class MyClass(object):
       def __init__(self, *args, **kwargs):
           super(MyClass, self).__init__(*args, **kwargs)

           self.data = {'foo': 'bar'}

You can now get a list of all features provided by an instance:

.. code-block:: python

   from link.feature import getfeatures

   obj = MyClass()
   result = getfeatures(obj)

   # result == [(obj, JSONFeature)]

**NB:** ``getfeatures()`` also look for instance members recursively:

.. code-block:: python

   class Dummy(object):
       def __init__(self, *args, **kwargs):
           super(Dummy, self).__init__(*args, **kwargs)

           self.inner = MyClass()

   obj2 = Dummy()
   result = getfeatures(obj2)

   # result == [(obj2.inner, JSONFeature)]

Now, you can check if an object provides a feature, and instantiate it:

.. code-block:: python

   from link.feature import hasfeature, getfeature

   assert hasfeature(obj, 'json')

   try:
       f = getfeature(obj, 'json')

   except AttributeError:
       print('obj has no feature json')

   result = f.to_json()
