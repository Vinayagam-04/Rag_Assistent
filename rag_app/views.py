import logging
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import OperationalError
from django.http import HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Document
from .rag_pipeline import RAGPipeline

# Configure logging
logger = logging.getLogger(__name__)

def index(request):
    logger.debug(f"Request method: {request.method}")
    try:
        if request.method == 'POST':
            logger.debug("Processing POST request")
            if 'document' in request.FILES:
                try:
                    doc_file = request.FILES['document']
                    title = doc_file.name[:255]
                    content = doc_file.read().decode('utf-8', errors='ignore')
                    document = Document.objects.create(title=title, content=content)
                    rag = RAGPipeline()
                    rag.store_document(content, str(document.id))
                    messages.success(request, 'Document uploaded and processed successfully!')
                    logger.debug("Document uploaded successfully")
                    return redirect('index')
                except OperationalError as e:
                    logger.error(f"Database error during document upload: {str(e)}")
                    messages.error(request, 'Database error: Unable to save document.')
                    return redirect('index')
                except Exception as e:
                    logger.error(f"Error during document upload: {str(e)}")
                    messages.error(request, f'Error uploading document: {str(e)}')
                    return redirect('index')
            elif 'query' in request.POST:
                query = request.POST.get('query', '').strip()
                logger.debug(f"Query received: {query}")
                if not query:
                    messages.error(request, 'Please enter a valid query.')
                    return redirect('index')
                try:
                    rag = RAGPipeline()
                    response = rag.query(query)
                    logger.debug(f"Query response: {response}")
                    return render(request, 'results.html', {'query': query, 'response': response})
                except Exception as e:
                    logger.error(f"Error processing query: {str(e)}")
                    messages.error(request, f'Error processing query: {str(e)}')
                    return redirect('index')
            else:
                logger.warning("Invalid POST request: No document or query provided")
                messages.error(request, 'Invalid request: Please upload a document or submit a query.')
                return redirect('index')
        else:
            logger.debug("Rendering index.html for GET request")
            return render(request, 'index.html')
    except Exception as e:
        logger.error(f"Unexpected error in index view: {str(e)}")
        return HttpResponseServerError(f"Server error: {str(e)}")

@csrf_exempt
def upload_document(request):
    """Handle document upload via AJAX"""
    if request.method == 'POST':
        try:
            if 'document' in request.FILES:
                doc_file = request.FILES['document']
                title = doc_file.name[:255]
                content = doc_file.read().decode('utf-8', errors='ignore')
                document = Document.objects.create(title=title, content=content)
                rag = RAGPipeline()
                rag.store_document(content, str(document.id))
                return JsonResponse({
                    'success': True,
                    'message': f'Document "{title}" uploaded successfully!',
                    'document_id': document.id
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'No document file provided.'
                })
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error uploading document: {str(e)}'
            })
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def process_query(request):
    """Handle query processing via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '').strip()
            
            if not query:
                return JsonResponse({
                    'success': False,
                    'message': 'Please enter a valid query.'
                })
            
            rag = RAGPipeline()
            response = rag.query(query)
            
            return JsonResponse({
                'success': True,
                'response': response,
                'query': query
            })
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error processing query: {str(e)}'
            })
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def get_chat_history(request):
    """Get chat history for the sidebar"""
    try:
        # For now, return empty history - you can implement this based on your needs
        history = []
        return JsonResponse({'success': True, 'history': history})
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Error loading chat history.'})