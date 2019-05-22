#!/usr/bin/python
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib.request
from . import parserjson
from . import parserxml

pueblos = {}
pueblos = parserjson.main()

def datos_municipio(municipio):
    try:
        id = pueblos[municipio]['id']
        id = id.split('d')[1]
        xmlFile = "http://www.aemet.es/xml/municipios/localidad_" + id + ".xml"
        return parserxml.main(xmlFile)

    except KeyError:
        print("Pueblo buscado no existente")


if __name__ == "__main__":

    datos_municipio(municipio)
