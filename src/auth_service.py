from models.user import User, validate_data
from models.availability import Availability
from models.reservation import Reservation
from models.eventhall import EventHall
from db import db

def create_user(user):
  # Verifica si el parámetro user es una instancia de la clase User
  if not isinstance(user, User):
    raise TypeError(f"Se esperaba una instancia de User, pero se recibió {type(user).__name__}")
  user_exists = User.query.filter_by(email=user.email, phone=user.phone).first()
  if user_exists:
    return ["Email or phone already registered"]
  db.session.add(user)
  db.session.commit()
  return f"User '{user.name}' created successfully"
def create_eventhall(eventhall):
  # Verifica si el parámetro eventhall es una instancia de la clase EventHall
  if not isinstance(eventhall, EventHall):
    raise TypeError(f"Se esperaba una instancia de User, pero se recibió {type(eventhall).__name__}")
  eventhall_exists = EventHall.query.filter_by(name=eventhall.name).first()
  if eventhall_exists:
    return "EventHall name already taken"
  
  db.session.add(eventhall)
  db.session.commit()
  return f"Event hall'{eventhall.name}' created successfully"