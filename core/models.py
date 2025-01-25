from django.db import models
from django.utils import timezone
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class WasteImage(models.Model):
    WASTE_TYPES = [
        ('organic', 'Organic'),
        ('recyclable', 'Recyclable'),
        ('hazardous', 'Hazardous'),
        ('other', 'Other'),
        ('unclassified', 'Unclassified')
    ]

    image = models.ImageField(upload_to='waste_images/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    classification_result = models.CharField(
        max_length=20,
        choices=WASTE_TYPES,
        default='unclassified'
    )
    confidence_score = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Waste Image {self.id} - {self.classification_result}"

    class Meta:
        ordering = ['-uploaded_at']
        
# new code
Base = declarative_base()

class WasteReport(Base):
    __tablename__ = 'waste_reports'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    waste_type = Column(String, nullable=False)
    file_path = Column(String, nullable=True)  # Path to the uploaded file

# Database setup
engine = create_engine('sqlite:///db.sqlite3')  # Replace with your DB URI
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
