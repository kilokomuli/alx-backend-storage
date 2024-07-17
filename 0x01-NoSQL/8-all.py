#!/usr/bin/env python3
"""LIsts al documents in a collection"""


def list_all(mongo_collection):
    """lists all documents"""
    return mongo_collection.find()
