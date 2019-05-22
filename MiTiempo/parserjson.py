import json
import sys

pueblos = {}

with open("municipios.json", 'r', encoding = "ISO-8859-1") as json_file:
    munis = json.load(json_file)


for muni in munis:
    pueblos[muni['nombre']] = muni


def main():
    return pueblos

if __name__ == "__main__":
    main()


## Ejemplo de funcionamiento
#try:
#    print(pueblos['p']['id_old'])
#except KeyError:
#    print("Pueblo buscado no existente")
