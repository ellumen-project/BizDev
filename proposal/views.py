from django.shortcuts import render,redirect
from .forms import DocumentForm
from django.http import JsonResponse
from django.views import View
from pathlib import Path
from pipelines.indexing_pipeline import IndexingPipeline
from pipelines.query_pipeline import QueryPipeline
from pipelines.extractive_qa_pipeline import ExtractiveQAPipeline
from pipelines.summarizer import SummarizerPipeline
import json,os
import logging
from unstructured.partition.auto import partition
from unstructured.documents.elements import Title
from unstructured_pytesseract import pytesseract
from django.conf import settings
from django.core.files.storage import default_storage


def home(request):
    return render(request, 'proposal/home.html', {})


def query(request):
    query_var = "LLM Response"
    return render(request, 'proposal/query.html', {'query_var': query_var})

def query(request):
    indexing_pipeline = IndexingPipeline()
    question = request.GET.get('question', None)
    if question:
        query_pipeline = QueryPipeline(indexing_pipeline.document_store)
        response = query_pipeline.run(question)
        return render(request, 'proposal/query.html', {'query_var': response})
    else:
        return render(request, 'proposal/query.html', {'query_var': "No question provided."})


class PipelineView(View):
    def get(self, request, *args, **kwargs):
        #questions =["Please output 5-10 sections covering the entire document.Sections should cover all input lines(from start to end).Section names should be short and brief(no more than 5 words)"]
        questions =["What are the objectives of this proposal?"]
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('debug.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        results={}
        try:
            uploaded_files = request.session.get('uploaded_files', [])
            if not uploaded_files:
                raise ValueError("No files to process")
            for question in questions:
                indexing_pipeline = IndexingPipeline()
                #output_dir = Path("/home/ec2-user/Haystack_RAG/Chat_with_your_data/data")
                output_dir = Path("/home/ec2-user/Projects/Django/BizDev/media/documents")
                indexing_pipeline.run([str(p) for p in output_dir.iterdir()])
                #indexing_pipeline.run(uploaded_files)
                query_pipeline = QueryPipeline(indexing_pipeline.document_store)
                result = query_pipeline.run(question)
                results[question]=result
                logger.debug(f"Question: {question}, Result: {result}")
            return render(request,'proposal/proposal.html',{'results':results})
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return render(request,'proposal/error.html',{"error": f"An error occurred: {e}"})


class ExtractiveQAView(View):
    def get(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('debug.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        try:
            indexing_pipeline = IndexingPipeline()
            output_dir = Path("/home/ec2-user/Haystack_RAG/Chat_with_your_data/data")
            indexing_pipeline.run([str(p) for p in output_dir.iterdir()])
            extractive_qa_pipeline = ExtractiveQAPipeline(indexing_pipeline.document_store)
            query = "What are the main objectives of this proposal?"
            result = extractive_qa_pipeline.run(query=query)
            max_result = max(result['reader']['answers'], key=lambda x: x.score)
            #print(result)
            logger.debug(f"Question: {query}, Result: {result}")
            return render(request,'proposal/extractiveqa.html',{'results':max_result})
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return render(request,'proposal/error.html',{"error": f"An error occurred: {e}"})

class DocumentOutlineView(View):
    def get(self, request, *args, **kwargs):
        questions =["Generate a comprehensive summary and outline of the entire document that includes overview, contract overview, description, background, objectives, Scope etc"]
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('debug.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        results={}
        try:
            uploaded_files = request.session.get('uploaded_files', [])
            if not uploaded_files:
                raise ValueError("No files to process")
            for question in questions:
                indexing_pipeline = IndexingPipeline()
                #output_dir = Path("/home/ec2-user/Haystack_RAG/Chat_with_your_data/data")
                output_dir = Path("/home/ec2-user/Projects/Django/BizDev/media/documents")
                indexing_pipeline.run([str(p) for p in output_dir.iterdir()])
                #indexing_pipeline.run(uploaded_files)
                summarizer_pipeline = SummarizerPipeline(indexing_pipeline.document_store)
                result = summarizer_pipeline.run(question)
                results[question]=result
                logger.debug(f"Question: {question}, Result: {result}")
            return render(request,'proposal/proposal.html',{'results':results})
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return render(request,'proposal/error.html',{"error": f"An error occurred: {e}"})
        
    
def upload_file(request):
    if request.method=='POST':
        form=DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            # Get the uploaded file paths
            print(request.FILES)
            #uploaded_files = [f.path for f in request.FILES.getlist('uploaded_file')]
            uploaded_files = []
            for f in request.FILES.getlist('uploaded_file'):
                file_path = os.path.join(settings.MEDIA_ROOT, f.name)
                with default_storage.open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                uploaded_files.append(file_path)
            logger = logging.getLogger(__name__)
            logger.debug(f"Uploaded files:{uploaded_files}")
            # Pass the file paths to the pipeline view
            request.session['uploaded_files'] = uploaded_files
            request.session.save()
            #return redirect('pipeline')
            return redirect('success')
    else:
        form =DocumentForm()
    return render(request,'proposal/upload.html',{'form':form})

def success_view(request):
    # Trigger the pipeline processing
    #return redirect('pipeline')
    return render(request, 'proposal/success.html')



