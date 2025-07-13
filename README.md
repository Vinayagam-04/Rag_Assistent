# AI Legal Assistant

A Django-based AI legal assistant that uses RAG (Retrieval-Augmented Generation) to provide legal advice and document analysis.

## Features

- 🤖 AI-powered legal question answering
- 📄 Document upload and analysis
- 💬 Real-time chat interface
- 📱 Responsive design
- 🔍 Document search and retrieval
- 📚 Chat history (coming soon)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Lawyer
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```bash
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key-here
```

**Important**: You need a Google Gemini API key to use the AI features:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`

## Usage

### Basic Usage
1. Open the application in your browser
2. Type your legal question in the chat input
3. Press Enter or click the send button
4. The AI will provide a response based on available documents or general legal knowledge

### Document Upload
1. Click the "Upload Document" button in the chat header
2. Select a text file (.txt, .pdf, .doc, .docx)
3. The document will be processed and stored
4. You can then ask questions about the uploaded document

### Chat History
- Click the history button (📜) to view chat history
- The sidebar will show your previous conversations

## Troubleshooting

### Common Issues

**1. "AI service is not properly configured"**
- Make sure you have set the `GEMINI_API_KEY` in your `.env` file
- Verify the API key is valid and has sufficient credits

**2. "No documents found for query"**
- Upload some legal documents first
- The AI can still answer general legal questions without documents

**3. Database errors**
- Run `python manage.py migrate` to ensure database is up to date
- Check that the `db.sqlite3` file is writable

**4. Static files not loading**
- Run `python manage.py collectstatic`
- Ensure `DEBUG=True` in settings for development

**5. ChromaDB errors**
- Delete the `chroma_db` folder and restart the application
- ChromaDB will recreate the database automatically

### Logs
Check the `debug.log` file in the root directory for detailed error messages.

## Technical Details

### Architecture
- **Backend**: Django 5.1.1
- **AI**: Google Gemini 1.5 Flash
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Frontend**: HTML, CSS, JavaScript

### Key Components
- `rag_app/views.py`: Main application logic
- `rag_app/rag_pipeline.py`: AI and document processing
- `rag_app/models.py`: Database models
- `templates/`: HTML templates
- `static/`: CSS and JavaScript files

### API Endpoints
- `GET /`: Main chat interface
- `POST /upload/`: Document upload (AJAX)
- `POST /query/`: Process queries (AJAX)
- `GET /history/`: Get chat history (AJAX)

## Development

### Adding New Features
1. Create new views in `rag_app/views.py`
2. Add URL patterns in `rag_app/urls.py`
3. Create templates in `templates/`
4. Add styles in `static/css/style.css`

### Testing
```bash
python manage.py test
```

### Production Deployment
1. Set `DEBUG=False` in settings
2. Configure proper `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up proper static file serving
5. Configure HTTPS

## License

This project is for educational purposes. Please ensure compliance with local laws and regulations when using AI for legal advice.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the logs in `debug.log`
3. Ensure all dependencies are properly installed
4. Verify your API keys are correctly configured 