# Oja E-commerce Platform

A modern e-commerce platform built with Django, featuring PayPal integration, cart functionality, and a responsive design.

## Features

- 🛍️ Product catalog with categories
- 🛒 Shopping cart functionality
- 💳 Secure PayPal payment integration
- 👤 User authentication and profiles
- 📦 Order management system
- 🚚 Shipping address management
- 📱 Responsive design for all devices
- 🔒 SSL/TLS security
- 🎨 Modern UI with WhiteNoise for static files

## Tech Stack

- **Backend**: Django 5.1.3
- **Database**: PostgreSQL
- **Payment Processing**: PayPal
- **Static Files**: WhiteNoise
- **Styling**: CSS/Bootstrap
- **Deployment**: Render.com

## Prerequisites

- Python 3.11+
- PostgreSQL
- PayPal Business Account (for payment processing)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd ecom
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```

## Environment Variables

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: PostgreSQL database URL
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `PAYPAL_RECEIVER_EMAIL`: PayPal business email for payments

## Project Structure

```
ecom/
├── cart/               # Shopping cart functionality
├── payment/            # Payment processing and orders
├── store/              # Main store application
├── static/             # Static files (CSS, JS, images)
├── media/              # User-uploaded content
├── templates/          # HTML templates
└── ecom/               # Project settings
```

## Database Configuration

The project uses PostgreSQL with the following configuration:

- Connection pooling enabled
- SSL required for security
- Keepalive connections
- Statement timeout: 5 seconds
- Connection timeout: 5 seconds

## Deployment

The application is configured for deployment on Render.com with the following features:

- WhiteNoise for static file serving
- PostgreSQL database
- SSL/TLS encryption
- Environment variable management

### Deployment Steps

1. Create a new Web Service on Render.com
2. Connect your repository
3. Set environment variables in Render dashboard
4. Deploy the application

## Security Features

- CSRF protection enabled
- SSL/TLS encryption required
- Secure password validation
- Session security
- Protected media files
- Sanitized user inputs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the development team.

## Acknowledgments

- Django framework and community
- PayPal for payment processing
- Bootstrap for UI components
- WhiteNoise for static file serving
- Render.com for hosting services
