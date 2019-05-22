#!/usr/bin/python
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib.request


class CounterHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inTemp = False
        self.inContent = False
        self.theContent = ""
        self.atributo = ""

        self.cont_prec = 0
        self.cont_tmaxima = 0
        self.cont_tmin = 0
        self.cont_cielo = 0
        self.precipitacion = ""
        self.tmaxima = ""
        self.tmin = ""
        self.estadocielo = ""

    def startElement (self, name, attrs):
        if name == 'dia':
            self.inItem = True
        elif self.inItem:
            if name == 'prob_precipitacion':
                 self.atributo = attrs.get('periodo')
                 if self.atributo == "00-24":
                     self.inContent = True
            elif name == 'estado_cielo':
                self.atributo = attrs.get('descripcion')
                self.inContent = True

        if name == 'temperatura':
            self.inTemp = True
        elif self.inTemp:
            if name == 'maxima':
                 self.inContent = True
            elif name == 'minima':
                self.inContent = True


    def endElement (self, name):
        if name == 'dia':
            self.inItem = False
        elif self.inItem:
            if name == 'prob_precipitacion':
                if self.cont_prec == 7:
                    self.precipitacion = self.theContent
                self.cont_prec = self.cont_prec + 1
                self.inContent = False
                self.theContent = ""
            elif name == 'estado_cielo':
                if self.cont_cielo == 7:
                    self.estadocielo = self.atributo
                self.cont_cielo = self.cont_cielo + 1
                self.inContent = False
                self.theContent = ""

        if name == 'temperatura':
            self.inTemp = False
        elif self.inTemp:
            if name == 'maxima':
                if self.cont_tmaxima == 1:
                    self.tmaxima = self.theContent
                self.cont_tmaxima = self.cont_tmaxima + 1
                self.inContent = False
                self.theContent = ""
            elif name == 'minima':
                if self.cont_tmin == 1:
                    self.tmin = self.theContent
                self.cont_tmin = self.cont_tmin + 1
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


# --- Main prog
def main(xml):

    xmlFile= urllib.request.urlopen(xml)

    Parser = make_parser()
    Handler = CounterHandler()
    Parser.setContentHandler(Handler)

    Parser.parse(xmlFile)
    
    return [Handler.precipitacion, Handler.estadocielo, Handler.tmaxima, Handler.tmin]

if __name__ == "__main__":
    main(xml)
