# Nano Stories - AI Brand Storytelling Platform

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.13+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastAPI-0.104.1-green.svg" alt="FastAPI Version">
  <img src="https://img.shields.io/badge/Google%20Gemini-2.0--flash--exp-orange.svg" alt="Gemini Version">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
</div>

## 🌟 Overview

**Nano Stories** is a cutting-edge AI-powered brand storytelling platform that combines character creation, product visualization, background design, and narrative generation to create compelling brand stories. Using Google's Gemini AI and advanced image fusion technology, it transforms your brand elements into cohesive visual narratives.

### ✨ Key Features

- 🤖 **AI-Powered Content Generation**: Leverages Google Gemini 2.0 Flash for intelligent content creation
- 🎨 **Multi-Modal Image Fusion**: Combines characters, products, and backgrounds into unified scenes
- 📱 **Modern Web Interface**: Responsive, accessible frontend with intuitive workflow
- 🔄 **Real-time Processing**: FastAPI backend with async processing capabilities
- 💾 **Local Storage**: Secure local file management with organized directory structure
- 🎯 **Brand Storytelling**: Purpose-built for marketing and brand communication

## 🏗️ Architecture

```
nano-stories/
├── backend/                 # FastAPI Backend
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # SQLAlchemy models
│   │   ├── services/       # Business logic (Gemini AI)
│   │   ├── database.py     # Database configuration
│   │   └── main.py         # FastAPI application
│   └── uploads/            # Generated images storage
├── frontend/               # Vanilla JavaScript Frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   └── api.js          # API client
│   ├── styles.css          # Modern CSS styling
│   └── index.html          # Main application
└── tests/                  # Test suites
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

#### Linux/macOS
```bash
chmod +x setup.sh
./setup.sh
```

#### Windows
```cmd
setup.bat
```

### Option 2: Manual Setup

#### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13+** - [Download from python.org](https://python.org)
- **Node.js 16+** - [Download from nodejs.org](https://nodejs.org)
- **Git** - [Download from git-scm.com](https://git-scm.com)

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/nano-stories.git
cd nano-stories
```

#### 2. Backend Setup

##### Install Python Dependencies

```bash
# Using pip (recommended)
pip install -r backend/requirements.txt

# Or using uv (faster)
pip install uv
uv pip install -r backend/requirements.txt
```

##### Environment Configuration

1. **Get Google Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the API key

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` file:
   ```env
   # Nano Stories Environment Configuration
   GOOGLE_API_KEY=your_actual_google_api_key_here
   DATABASE_URL=sqlite:///./nano_stories.db
   ```

   > ⚠️ **Security Note**: Never commit your `.env` file to version control!

##### Initialize Database

```bash
cd backend
python -c "from src.database import init_database; init_database()"
```

#### 3. Frontend Setup

```bash
cd frontend

# Install ESLint for code quality (optional)
npm install

# The frontend is pure HTML/CSS/JS, no build process required
```

### Option 3: Docker Setup

#### Prerequisites
- **Docker** - [Download from docker.com](https://docker.com)
- **Docker Compose** - Usually included with Docker Desktop

#### Quick Start with Docker

```bash
# Clone repository
git clone https://github.com/your-username/nano-stories.git
cd nano-stories

# Create environment file
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Start services
docker-compose up --build
```

#### Access the Application
- 🌐 **Frontend**: http://localhost:3000
- 📡 **Backend API**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs

### 4. Run the Application (Manual Setup)

#### Start Backend Server

```bash
cd backend
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Start Frontend Server

```bash
cd frontend
python -m http.server 3000
```

#### Access the Application

- 🌐 **Frontend**: http://localhost:3000
- 📡 **Backend API**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs

## 📋 Workflow

1. **📋 Project Setup**: Create a new brand storytelling project
2. **👤 Character Creation**: Generate or describe your brand character
3. **📦 Product Upload**: Upload product images for integration
4. **🎨 Background Design**: Create scene backgrounds
5. **📖 Story Writing**: Craft your brand narrative
6. **⚡ Generate Images**: AI fuses all elements into final images
7. **🖼️ Gallery**: Review and download generated images

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API Key | Required |
| `DATABASE_URL` | SQLite database path | `sqlite:///./nano_stories.db` |

### File Structure

```
uploads/
├── characters/     # Generated character images
├── products/       # Uploaded product images
├── backgrounds/    # Generated background images
├── final/         # Final fused images
└── mock-images/   # Placeholder images
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm run lint
```

### Manual Testing

```bash
# Test API endpoints
curl http://localhost:8000/api/v1/projects

# Test image generation
curl -X POST http://localhost:8000/api/v1/projects/{project_id}/generate
```

## 📜 Available Scripts

### Setup Scripts
- `setup.sh` - Linux/macOS automated setup
- `setup.bat` - Windows automated setup

### Development Scripts
- `backend/test_image_saving.py` - Test image generation
- `backend/create_components.py` - Create test components
- `frontend/test_final_generation.py` - Test final image generation

### Docker Scripts
- `docker-compose.yml` - Full stack deployment
- `backend/Dockerfile` - Backend container
- `frontend/Dockerfile` - Frontend container

## 🔄 Development Workflow

### 1. Feature Development
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes following TDD
# Write tests first, then implementation

# Run tests
cd backend && pytest tests/ -v

# Commit changes
git add .
git commit -m "feat: add your feature description"
```

### 2. Code Quality
- Follow PEP 8 for Python code
- Use type hints in Python functions
- Write comprehensive docstrings
- Keep functions small and focused
- Use async/await for FastAPI endpoints

### 3. Testing Strategy
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and database operations
- **Contract Tests**: Test API request/response contracts
- **Performance Tests**: Test image generation performance

### 4. Database Migrations
```bash
# When models change, recreate database
cd backend
rm nano_stories.db
python -m src.main
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the development workflow
4. Write tests for new features
5. Ensure all tests pass
6. Submit a pull request

## 📋 Project Structure

```
nano_stories/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # SQLAlchemy models
│   │   ├── services/       # Business logic
│   │   └── main.py         # Application entry point
│   └── tests/              # Test suites
├── frontend/                # Vanilla JS frontend
│   ├── src/
│   │   ├── api.js          # API client
│   │   ├── app.js          # Main application
│   │   └── components/     # UI components
│   └── styles.css          # Application styles
├── docs/                   # Documentation
├── scripts/                # Utility scripts
└── specs/                  # Feature specifications
```

## 🔧 Troubleshooting

### Common Issues

**1. Gemini API Errors**
```
Error: API_KEY not found
```
- Ensure `.env` file exists with `GEMINI_API_KEY`
- Check API key is valid and has proper permissions

**2. Database Connection Issues**
```
sqlite3.OperationalError: unable to open database file
```
- Ensure write permissions in backend directory
- Check if database file is corrupted

**3. Image Generation Fails**
```
Error: Image generation failed
```
- Verify Gemini API key has image generation permissions
- Check network connectivity
- Ensure uploads directory has write permissions

**4. Frontend Not Loading**
```
Failed to fetch API endpoints
```
- Verify backend is running on port 8000
- Check CORS settings in middleware
- Ensure API endpoints are accessible

### Debug Mode

Enable debug logging:
```bash
# Backend
cd backend
uvicorn src.main:app --reload --log-level debug

# Frontend
cd frontend
python -m http.server 3000
```

### Reset Database

```bash
cd backend
rm nano_stories.db
python -m src.main
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [SQLAlchemy Documentation](https://sqlalchemy.org/)
- [Vanilla JS Best Practices](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini for AI image generation
- FastAPI for the robust API framework
- The open source community for amazing tools

---

**Happy coding! 🚀**

## 📚 API Documentation

### Core Endpoints

#### Projects
- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create new project
- `GET /api/v1/projects/{id}` - Get project details

#### Characters
- `POST /api/v1/projects/{id}/character` - Generate character

#### Products
- `POST /api/v1/projects/{id}/product/generate` - Generate product image
- `POST /api/v1/projects/{id}/product/upload` - Upload product image

#### Backgrounds
- `POST /api/v1/projects/{id}/background` - Generate background

#### Stories
- `POST /api/v1/projects/{id}/story` - Create story

#### Generation
- `POST /api/v1/projects/{id}/generate` - Generate final images

### Response Format

```json
{
  "images": [
    {
      "id": "fused_img_1",
      "prompt": "Generated prompt...",
      "image_url": "/uploads/final/final_mock_uuid.png",
      "fusion_style": "seamlessly integrated composition"
    }
  ]
}
```

## � Docker Deployment

### Using Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Services

#### Backend Only
```bash
cd backend
docker build -t nano-stories-backend .
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key_here nano-stories-backend
```

#### Frontend Only
```bash
cd frontend
docker build -t nano-stories-frontend .
docker run -p 3000:80 nano-stories-frontend
```

### Environment Variables in Docker

Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_actual_api_key
```

Docker Compose will automatically load these variables.

### Common Issues

#### 1. API Key Issues
```
Error: GOOGLE_API_KEY not configured
```
**Solution**: Ensure your `.env` file contains a valid Google Gemini API key.

#### 2. Port Already in Use
```
Error: [Errno 48] Address already in use
```
**Solution**:
```bash
# Find process using port
lsof -i :8000
# Kill process
kill -9 <PID>
```

#### 3. Database Issues
```
Error: sqlite3.OperationalError
```
**Solution**:
```bash
cd backend
rm nano_stories.db
python -c "from src.database import init_database; init_database()"
```

#### 4. CORS Issues
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution**: Ensure both servers are running on correct ports and CORS is configured.

### Debug Mode

Enable debug logging:
```bash
cd backend
DEBUG=1 python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Write tests for new features
- Update documentation
- Use conventional commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** - For advanced AI image generation
- **FastAPI** - For the robust backend framework
- **SQLite** - For lightweight database storage
- **Pillow** - For image processing capabilities

## 📞 Support

- 📧 **Email**: support@nano-stories.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/nano-stories/issues)
- 📖 **Documentation**: [Wiki](https://github.com/your-username/nano-stories/wiki)

---

<div align="center">
  <p>Built with ❤️ using AI for better brand storytelling</p>
  <p>
    <a href="#nano-stories---ai-brand-storytelling-platform">Back to Top</a>
  </p>
</div>