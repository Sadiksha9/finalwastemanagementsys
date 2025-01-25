from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///users.db'  # Replace with your database URL
echo = True  # Logs SQL queries
engine = create_engine(DATABASE_URL, echo=echo)
Base = declarative_base()

# SQLAlchemy setup
DATABASE_URL = 'sqlite:///users.db'  # Replace with your database URL
echo = True  # Logs SQL queries
engine = create_engine(DATABASE_URL, echo=echo)
Base = declarative_base()

# SQLAlchemy User model
class SQLAlchemyUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
sqlalchemy_session = Session()

# Django views
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if user already exists (SQLAlchemy)
        existing_user = sqlalchemy_session.query(SQLAlchemyUser).filter_by(username=username).first()
        existing_email = sqlalchemy_session.query(SQLAlchemyUser).filter_by(email=email).first()
        if existing_user:
            messages.error(request, "Username already exists.")
            return redirect('signup')
        if existing_email:
            messages.error(request, "Email already exists.")
            return redirect('signup')

        # Create a new SQLAlchemy user
        new_user = SQLAlchemyUser(username=username, email=email, password=password)
        sqlalchemy_session.add(new_user)
        sqlalchemy_session.commit()

        # Optional: Sync to Django's auth model
        if not User.objects.filter(username=username).exists():
            django_user = User.objects.create_user(username=username, email=email, password=password)
            django_user.save()

        messages.success(request, "Signup successful. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate with SQLAlchemy
        user = sqlalchemy_session.query(SQLAlchemyUser).filter_by(username=username, password=password).first()
        if user:
            # Optional: Sync with Django's authentication system
            django_user = authenticate(username=username, password=password)
            if django_user:
                login(request, django_user)
                messages.success(request, "Login successful.")
                return redirect('home')

            messages.success(request, "Login successful (SQLAlchemy).")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')
