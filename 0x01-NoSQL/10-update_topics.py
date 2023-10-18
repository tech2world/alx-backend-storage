#!/usr/bin/env python3
"""
Write a Python function that changes all topics of a school
document based on the name:

Prototype: def update_topics(mongo_collection, name, topics):
mongo_collection will be the pymongo collection object
name (string) will be the school name to update
topics (list of strings) will be the list of topics approached in the school
"""

import pymongo


def update_topics(mongo_collection, name, topics):
    """
    change all topics of a school document based on the name
    """
    doc_name = {"name": name}
    updated_values = {"$set": {"topics": topics}}
    mongo_collection.update_many(doc_name, updated_values)
    