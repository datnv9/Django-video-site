from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
import urllib2
import predictionio
import json
import csv

def ReadFileDat(fileName, search):
    movieIds = []
    fileDat = open(fileName,"r")
    lines = fileDat.readlines()
    # with open('links.csv') as file:
    #     for item in lines:
    #         if search.lower() in search.lower():
    #             print "item:" + item[0][0]
    #             movieIdsInMoviesLensss.append(item[0][0])

    for item in lines:
        #print item.decode('iso-8859-1').encode('utf8')
        with open('links.csv') as fileCsv:
            reader = csv.reader(fileCsv) 
            if (search.lower() in item.lower()):
                print "item: " + item
                index = item.index("::")
                item = item[0:index]
                print "item slit: " + item
                for row in reader:
                    if row[0] == item:
                       #print row[0]
                       print "movies Id: " + row[2]
                       movieIds.append(row[2])                 
    return  movieIds
    

def index(request):
    #search = ""
    if request.method == 'POST':
        search = request.POST['search']
    # if search in "1::Toy Story (1995)::Animation|Children's|Comedy":
    #     print "co roi ne"
        ReadFileDat("movies.dat",search)
    return render(request, 'search.html')

def signin(request):
    # length = 8
    # if request.method == 'POST':
    #     userName = request.POST['username']
    # engine_client = predictionio.EngineClient(url="http://192.168.99.100:8000")
    # r = engine_client.send_query({"user": 1, "num": length})
    # m = json.dumps(r)
    # js = json.loads(m)

    # loops = []
    # for item in range(1,length+1):
    #     loops.append(item)
    # #for index in range(0:3):
    # movieIds = []
    # #Read file csv
        
    # for item in js['itemScores']:
    #     print item
    #     with open('links.csv') as file:
    #         reader = csv.reader(file) 
    #         for row in reader:
    #             if row[0] == item['item']:
    #                 movieIds.append(row[2])
    
    return render(request, 't.html')
    #return render(request, 't.html', {'movieIds':json.dumps(movieIds), 'length':loops})
    #return HttpResponse(json.dumps(movieIds))
def t(request):
    if request.method == 'GET':
        return render(request, 'index.html')

def search(request):
    return true

def signout(request):
    print "signout"
    if request.method == 'GET':
        return render(request, 'index.html')