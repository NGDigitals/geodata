#!/usr/bin/env python
# coding: utf-8
import os
import overpy
import uvicorn
from fastapi import FastAPI
        
class GeoData:

    def __init__(self):
        self.api = overpy.Overpass()
    
    def loadByBounds(self, bounds=""):
        self.api = overpy.Overpass()
        result = self.api.query(f"""
                                way(poly:"{bounds}");
                                way._[building];
                                (._;>;);
                                out body; 
                                """)
        # result = self.api.query(f"""
        #                         node(poly:"{bounds}");
        #                         out body;
        #                         """)
        data = []
        latlng = bounds.split(" ", 2)
        for way in result.ways:
            # location = dict(name = node.tags.get("name", "n/a"), lat = "%f" % (node.lat), lng = "%f" % (node.lon))
            location = dict(name = way.tags.get("name", "n/a"), lat = "%f" % float(latlng[0]), lng = "%f" % float(latlng[1]))
            data.append(location)
        return data


app = FastAPI()

@app.get("/")
def test():
    return {"Welcome to GeoData"}

@app.get("/data/")
def fetchDataByBounds(bounds: str):
    geodata = GeoData();
    result = geodata.loadByBounds(bounds)
    return result


if __name__ == "__main__":
    port = os.getenv("PORT")
    if not port:
        port = 8080
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=False, log_level="debug")