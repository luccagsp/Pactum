from models.user import User, validate_data
from models.availability import Availability
from models.reservation import Reservation
from models.eventhall import EventHall


def create_eventhall(user):
      # Verifica si el parámetro user es una instancia de la clase User
    if not isinstance(user, User):
      raise TypeError(f"Se esperaba una instancia de User, pero se recibió {type(user).__name__}")
    
    # Si pasa la verificación, continúa con el proceso
    print("Usuario válido:", user)
    # Aquí continuarías con la lógica para crear el EventHall