# Ecommerce API

A modern FastAPI-based ecommerce application skeleton for building scalable online stores.

## Features

- ✨ Built with FastAPI for high performance
- 🚀 Async/await support for concurrent operations
- 📚 Interactive API documentation (Swagger UI)
- 🔒 CORS middleware for cross-origin requests
- 🗄️ SQLAlchemy ORM ready
- 🔧 Environment configuration support

## Project Structure

```
ecommerce/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Project dependencies
├── README.md              # This file
└── .github/
    └── copilot-instructions.md  # Development instructions
```

## Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone or navigate to the project directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the development server:
```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health & Status
- `GET /` - Welcome message and API status
- `GET /health` - Health check endpoint

## Development

### Adding New Routes

Edit `main.py` and add new routes:

```python
@app.get("/products")
async def get_products():
    return {"products": []}
```

### Adding Dependencies

Add packages to `requirements.txt` and reinstall:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root for environment variables:
```
DATABASE_URL=sqlite:///./ecommerce.db
DEBUG=True
```

## Next Steps

- [ ] Set up database models
- [ ] Create product endpoints
- [ ] Add user authentication
- [ ] Implement shopping cart
- [ ] Add payment processing
- [ ] Create order management

## License

MIT

## Support

For questions or issues, please create an issue in the project repository.
