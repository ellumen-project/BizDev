from django.db import models
import json

# Define a model to store the metadata
class Metadata(models.Model):
    page_number = models.IntegerField()
    file_path = models.CharField(max_length=255)
    query = models.TextField()
    answer = models.TextField()
    score = models.FloatField()
    data = models.TextField()

# Define a function to store the metadata in the database
def store_metadata(metadata):
    data = json.loads(data)
    answer = max(data['reader']['answers'], key=lambda x:x['score'])
    for answer in metadata['reader']['answers']:
        # Extract the metadata
        page_number = answer['meta']['answer_page_number']
        file_path = answer['document']['meta']['file_path']
        query = answer['query']
        answer_text = answer['data']
        score = answer['score']
        data = answer['data']

        # Create a new Metadata object and save it to the database
        Metadata.objects.create(
            page_number=page_number,
            file_path=file_path,
            query=query,
            answer=answer_text,
            score=score,
            data=data
        )

class Document(models.Model):
    title = models.CharField(max_length=100)
    uploaded_file = models.FileField(upload_to='documents/')

class Solicitation(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

class File(models.Model):
    upload = models.FileField(upload_to='documents/')
    solicitation = models.ForeignKey(Solicitation, related_name='files', on_delete=models.CASCADE)