from models.user import User
from models.availability import Availability
from models.reservation import Reservation
from models.eventhall import EventHall

from db import db
from config.bcrypt_adapter import BcryptAdapter
from flask_login import login_user, login_required, logout_user, current_user

BcryptAdapter = BcryptAdapter()
class AuthService:
    
  def create_user(user):
    # Verifica si el parámetro user es una instancia de la clase User
    if not isinstance(user, User):
      raise TypeError(f"Se esperaba una instancia de User, pero se recibió {type(user).__name__}")
    user_exists = User.query.filter_by(email=user.email, phone=user.phone).first()
    if user_exists:
      return ["Email or phone already registered"]
  
    user.password = BcryptAdapter.hash(password=user.password)
    db.session.add(user)
    db.session.commit()
    return f"User '{user.name}' created successfully"
  def log_in_user(user):
    
      userFound = User.query.filter_by(email=user.email).first()
      if not userFound: return ["User not found"]
      
      login_password = user.password
      hashed_password = userFound.password
    
      if not BcryptAdapter.compare(login_password, hashed_password):
          return ["Incorret password"]
      
      login_user(userFound, remember=True) 
  def create_eventhall(eventhall):
    # Verifica si el parámetro eventhall es una instancia de la clase EventHall
    if not isinstance(eventhall, EventHall):
      raise TypeError(f"Se esperaba una instancia de EventHall, pero se recibió {type(eventhall).__name__}")
    eventhall_exists = EventHall.query.filter_by(name=eventhall.name).first()
    if eventhall_exists:
      return "EventHall name already taken"
    db.session.add(eventhall)
    db.session.commit()
    return f"Event hall'{eventhall.name}' created successfully"