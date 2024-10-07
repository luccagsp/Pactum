import base64

def objToStr(object):
    # Filtrar y solo imprimir los atributos que no son metadatos
    object_filtered = {}
    for key, value in object.__dict__.items():
        if not key.startswith('_'):
            if isinstance(value, bytes): value = value.decode('utf-8')

            object_filtered[key] = value
    print(object_filtered)
    return object_filtered