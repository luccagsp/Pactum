import re 
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
email_pattern =  re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_data(nombre, apellido, email, phone) -> list:
    if len(nombre) > 20 or len(apellido) > 20 or " " in nombre or " " in apellido:
        return ["Nombre o apellido invalidos"]
    if email_pattern.match(email) == None:
        return ["Email invalido"]
    try:
        if carrier._is_mobile(number_type(phonenumbers.parse(phone))):
            return ["Numero de telefono invalido"]
    except:
            return ["Numero de telefono invalido"]

    return[None, {'nombre':nombre, 'apellido':apellido, 'email':email, 'phone':phone}]