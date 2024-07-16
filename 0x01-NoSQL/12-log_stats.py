#!/usr/bin/env python3
"""log stats"""
from pymongo import MongoClient


def nginx_log_stats():
    """Provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient("mongodb://localhost:27017")
    db = client.logs
    collection = db.nginx
    total_logs = collection.cdocs({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    m = {method: collection.cdocs({'method': method}) for method in methods}
    status_check = collection.cdocs({'method': 'GET', 'path': '/status'})
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {m[method]}")
    print(f"{status_check} status check")


if __name__ == "__main__":
    log_stats()
