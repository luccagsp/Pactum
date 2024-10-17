import json
import re

# Patrón para validar el formato de tiempo HH:MM en 24 horas
time_pattern = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')

def checkHour(hour):
    if hour == "":
        return "Not specified"
    else:
        return hour

def parseToJson(data):
    
    availability = {
        'mon': {
            'startTime': checkHour(data.get('start-time-mon')),
            'endTime': checkHour(data.get('end-time-mon'))
        },
        'tue': {
            'startTime': checkHour(data.get('start-time-tue')),
            'endTime': checkHour(data.get('end-time-tue'))
        },
        'wed': {
            'startTime': checkHour(data.get('start-time-wed')),
            'endTime': checkHour(data.get('end-time-wed'))
        },
        'thu': {
            'startTime': checkHour(data.get('start-time-thu')),
            'endTime': checkHour(data.get('end-time-thu'))
        },
        'fri': {
            'startTime': checkHour(data.get('start-time-fri')),
            'endTime': checkHour(data.get('end-time-fri'))
        },
        'sat': {
            'startTime': checkHour(data.get('start-time-sat')),
            'endTime': checkHour(data.get('end-time-sat'))
        },
        'sun': {
            'startTime': checkHour(data.get('start-time-sun')),
            'endTime': checkHour(data.get('end-time-sun'))
        }
    }
    return availability

def validate_json_hours_structure(data):
    # Días de la semana esperados
    expected_days = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}
    data = parseToJson(data)
    print(data)
    # Asegúrate de que data sea un diccionario
    if not isinstance(data, dict):
        return [False, "Invalid data: Expected a dictionary"]
    
    # Verificar que todos los días de la semana estén presentes
    missing_days = expected_days - set(data.keys())
    if missing_days:
        return [False, f"Missing days in data: {', '.join(missing_days)}"]

    for day in expected_days:
        times = data[day]
        print(times)
        if not isinstance(times, dict):
            return [False, f"Invalid structure for {day}: Expected a dictionary"]
        
        # Validar que cada día tenga 'startTime' y 'endTime'
        if "startTime" not in times or "endTime" not in times:
            return [False, f"Missing 'startTime' or 'endTime' in {day}"]
        if 'Not specified' in times["startTime"] and 'Not specified' not in times["endTime"]:
            return [False, f"Missing hour in '{day}'"]
        if 'Not specified' not in times["startTime"] and 'Not specified' in times["endTime"]:
            return [False, f"Missing hour in {day}"]
        if not isinstance(times.get("startTime"), str) or not isinstance(times.get("endTime"), str):
            return [False, f"Invalid time format in {day}: 'startTime' and 'endTime' must be strings"]
        
        # Validar formato de tiempo
        if times["startTime"] != "Not specified" and not time_pattern.match(times["startTime"]):
            return [False, f"Invalid startTime format in {day}: Expected 'HH:MM' (24-hour)"]
        if times["endTime"] != "Not specified" and not time_pattern.match(times["endTime"]):
            return [False, f"Invalid endTime format in {day}: Expected 'HH:MM' (24-hour)"]
    
    return True, "Valid JSON structure"

#EXPECTED SYNTAX:
# {
#     "mon": {
#         "startTime": "Not specified",
#         "endTime": "Not specified"
#     },
#     "tue": {
#         "startTime": "Not specified",
#         "endTime": "Not specified"
#     },
#     "wed": {
#         "startTime": "Not specified",
#         "endTime": "Not specified"
#     },
#     "thu": {
#         "startTime": "Not specified",
#         "endTime": "Not specified"
#     },
#     "fri": {
#         "startTime": "Not specified",
#         "endTime": "Not specified"
#     },
#     "sat": {
#         "startTime": "Not specified",
#         "endTime": "Not specified"
#     },
#     "sun": {
#         "startTime": "12:40",
#         "endTime": "15:36"
#     }
# }