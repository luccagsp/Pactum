from sqlalchemy.sql import func
from db import db
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventhall_id = db.Column(db.Integer, db.ForeignKey('eventhall.id'), nullable=False)
    file_url = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)
    type_image = db.Column(db.String(50), nullable=False, default="image") 
    created_at = db.Column(db.DateTime, default=func.now())
    deleted_at = db.Column(db.DateTime)