import boto3
import wolframalpha
import os
import sys
from dotenv import load_dotenv



bucket = "equation-solver1"



load_dotenv()
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
app_id = os.getenv('APP_ID')

client1 = wolframalpha.Client(app_id)



client = boto3.client('textract',region_name='us-east-1',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
s3 = boto3.resource('s3',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

documentName = input("Please Enter your file name: ")
data = open(documentName, 'rb')
s3.Bucket('equation-solver1').put_object(Key=documentName, Body=data)

your_bucket = s3.Bucket(bucket)


#extracted_data = []



#for s3_file in your_bucket.objects.all():
response = client.detect_document_text(
    Document={'S3Object': {
        'Bucket': bucket,
        'Name': documentName
    }})

blocks = response['Blocks']
equation = ""
print(equation)
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        equation += item["Text"] + "\n"

res = client1.query(equation)
answer = next(res.results).text
print(answer)
