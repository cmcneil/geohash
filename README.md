# geohash
![pytest](https://github.com/cmcneil/geohash/actions/workflows/python-app.yml/badge.svg)

GeoFire adds spatial querying to Firestore. This is a Python mathematically-equivalent replication.

[Firebase](https://firebase.google.com/docs/firestore) does not have native geospatial querying. However, they provide the [GeoFireUtils](https://github.com/firebase/geofire-android) library to do Geohashing, which they have open-sourced. That's great for the Kotlin libraries on app, but one use case is to use the official Python `geofire_admin` libraries to load a dataset into the store for use by your app.

This snippet just closes that gap. We can use this to generate geo hashes in python that match Firebase's implementation, so we can load our data in Python. 

As this is a community library, there is no guarantee on the function staying syncced to geofire. (though I copied their current test cases, and hash functions should never change their input/output mapping as a matter of principle)
