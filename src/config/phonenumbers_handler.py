import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type, NumberParseException

def verify_phone(phone):
  try:
    parsed_number = phonenumbers.parse(phone, "AR")  # "AR" para Argentina
    valid_phone = phonenumbers.is_valid_number(parsed_number)
    return valid_phone
  except:
    print("Numero de telefono invalido")
    return False
  
  # except NumberParseException as exc :
  #   print("Numero de telefono invalido")
  #   return False

# print(verify_phone("+5493564609680"))