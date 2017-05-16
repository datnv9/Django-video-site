from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
import urllib2
import predictionio
import json
import csv

def index(request):
    # data = '{ "user": "1", "num": 4 }'
    # url = 'http://localhost:8000/queries.json'
    # req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    # f = urllib2.urlopen(req)
    userName = 123
    
    # print userName
    engine_client = predictionio.EngineClient(url="http://localhost:8000")
    r = engine_client.send_query({"user": "1", "num": 4})
    return render(request, 'index.html',{'username':json.dumps(r)})

def signin(request):
    if request.method == 'POST':
        userName = request.POST['username']
    engine_client = predictionio.EngineClient(url="http://localhost:8000")
    r = engine_client.send_query({"user": userName, "num": 8})
    m = json.dumps(r)
    js = json.loads(m)
    
    #for index in range(0:3):
    movieIds = []
    #Read file csv
        
    for item in js['itemScores']:
        print item
        with open('links.csv') as file:
            reader = csv.reader(file) 
            for row in reader:
                if row[0] == item['item']:
                    movieIds.append(row[2])
    
    
    return render(request, 't.html', {'movieIds':json.dumps(movieIds)})
    #return HttpResponse(json.dumps(movieIds))
def t(request, hello):
    text = helo
    return HttpResponse(text)
