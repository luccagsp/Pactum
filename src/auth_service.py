from models.user import User
from models.availability import Availability
from models.reservation import Reservation
from models.eventhall import Eventhall

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
      if not userFound:
        return [False, "User not found"]
      
      login_password = user.password
      hashed_password = userFound.password
    
      if not BcryptAdapter.compare(login_password, hashed_password):
          return [False, "Incorret password"]
      
      login_user(userFound, remember=True) 
      return ["successfully logged in"]
  def create_eventhall(eventhall):
    # Verifica si el parámetro eventhall es una instancia de la clase Eventhall
    if not isinstance(eventhall, Eventhall):
      raise TypeError(f"Se esperaba una instancia de Eventhall, pero se recibió {type(eventhall).__name__}")
    eventhall_exists = Eventhall.query.filter_by(name=eventhall.name).first()
    if eventhall_exists:
      return "Eventhall name already taken"
    db.session.add(eventhall)
    db.session.commit()
    return f"Event hall'{eventhall.name}' created successfully"