#!/usr/bin/env python3
"""Inserts a document in python"""

def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection based on kwargs"""
    return mongo_collection.insert_one(kwargs).inserted_id
