#!/usr/bin/env python3
"""
Write a Python function that inserts a new document in a collection based on kwargs:

Prototype: def insert_school(mongo_collection, **kwargs):
mongo_collection will be the pymongo collection object
Returns the new _id
"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    insert a new document into the collection
    """
    new_doc = mongo_collection.insert(kwargs)
    return new_doc
