https://weather-dashboard-wewn.onrender.com/

This is a full-stack Django web application that provides real-time weather data and interactive visualizations for cities worldwide.

Stack & Skills 
* Backend Development
- Django 5.2.7 
- RESTful API Integration (OpenWeatherMap API consumption)
- Database Modeling (SQLite with Django ORM)
- URL Routing (Clean URL patterns and reverse URL lookups)
- View Functions (Class-based and function-based views)
- Middleware Configuration (Security and static files handling)

Frontend Development
- HTML5/CSS3 (Semantic markup and modern styling)
- JavaScript ES6+ (Dynamic content and API calls)
- Chart.js (Interactive data visualizations)
- Bootstrap 4 (Responsive grid system and components)
- AJAX/Fetch API (Asynchronous data loading)

DevOps & Deployment
- Render (Cloud platform deployment)
- Gunicorn (Production WSGI server)
- Whitenoise (Static file serving in production)
- Environment Configuration (Secure management of API keys)
- Build Automation (Custom build scripts and dependency management)

API Integration
- OpenWeatherMap API (Real-time weather data integration)

Key Achievements
- Successfully deployed a full-stack Django application to production
- Integrated third-party API with proper error handling and data validation
- Implemented responsive design that works across all device sizes
- Built interactive data visualizations using Chart.js
- Configured production environment with security best practices
- Automated deployment pipeline with Render and GitHub integration

Project Structure
weather_dashboard/
├── weather/ # Main app
│ ├── models.py # Database models
│ ├── views.py # Application logic
│ ├── urls.py # URL routing
│ └── templates/ # HTML templates
├── weatherdb/ # Project configuration
│ ├── settings.py # Django settings
│ └── urls.py # Project URLs
├── requirements.txt # Python dependencies
├── render.yaml # Deployment configuration
└── build.sh # Build script
- **REST API Design** - Clean endpoint structure
- **Error Handling** - Robust API error management
- **Data Parsing** - JSON response processing
