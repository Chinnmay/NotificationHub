# NotificationHub

A modern notification hub built with FastAPI and Kafka for scalable, real-time notification delivery.

## 🚀 Features

- **FastAPI Framework**: High-performance async API
- **Kafka Integration**: Event-driven notification processing with aiokafka
- **Health Monitoring**: Built-in health check endpoints
- **Auto Documentation**: Interactive API docs with Swagger UI
- **Scalable Architecture**: Async-first design for high throughput

## 📋 Prerequisites

- Python 3.10+
- Kafka server (for production)
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NotificationHub
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔗 Available Endpoints

### Core Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## 🏗️ Project Structure

```
NotificationHub/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── venv/               # Virtual environment (not tracked)
```

## 🔧 Dependencies

- **FastAPI** (0.118.2): Modern web framework for building APIs
- **Uvicorn** (0.37.0): ASGI server for FastAPI
- **aiokafka** (0.12.0): Async Kafka client for Python

## 🌐 Environment Setup

### Local Development
The application runs on `http://localhost:8000` by default.

### Environment Variables
Create a `.env` file for configuration:
```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
API_HOST=0.0.0.0
API_PORT=8000
```

## 🐳 Docker Support (Coming Soon)

Docker configuration will be added for easy deployment and scaling.

## 🧪 Testing

```bash
# Run the application
uvicorn main:app --reload

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
```

## 📈 Monitoring

- Health check endpoint: `/health`
- Built-in FastAPI metrics
- Kafka connection monitoring (when implemented)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔮 Roadmap

- [ ] Kafka producer/consumer implementation
- [ ] Notification templates
- [ ] Multi-channel delivery (email, SMS, push)
- [ ] User management
- [ ] Analytics and reporting
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Monitoring and alerting

## 📞 Support

For questions or support, please open an issue in the repository.

---

**Built with ❤️ using FastAPI and Kafka**
