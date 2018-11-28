from igbot.instadp import *
import csv

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messengerbot.settings')
django.setup()

from igbot.models import Instagrammer

Instagrammer.objects.all().delete()
# image_url, bio = getImageUrl("changchaishi")
  
# csv file name 
filename = "igid.csv"
  
# initializing the titles and rows list 
fields = [] 
rows = [] 
  
# reading csv file 
with open(filename, 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile) 
      
    # extracting field names through first row 
    fields = next(csvreader) 
  
    # extracting each data row one by one 
    for row in csvreader: 
        rows.append(row) 
  
    # get total number of rows 
    print("Total no. of rows: %d"%(csvreader.line_num)) 

# printing the field names 
print('Field names are:' + ', '.join(field for field in fields)) 

#  printing first 5 rows 
print('\nRows are:\n') 
for row in rows: 
    # parsing each column of a row 
    id = row[0]
    genre = row[1]
    country = row[2]
    # print(id+genre+country)
    
    image_url, bio = getImageUrl(id)
    if image_url == "":
        print("Id not found")
    else:
        print("processing %s"%id)
        Instagrammer.objects.create(
            id = id,
            genre = genre,
            country = country,
            content = bio,
            url = "https://www.instagram.com/%s" % id,
            image_url = image_url
        )