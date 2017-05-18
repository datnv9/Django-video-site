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
    for item in lines:
        #print item.decode('iso-8859-1').encode('utf8')
        with open('links.csv') as fileCsv:
            reader = csv.reader(fileCsv) 
            if (search.lower() in item.lower()):
                #print "item: " + item
                index = item.index("::")
                item = item[0:index]
                #print "item slit: " + item
                for row in reader:
                    if row[0] == item:
                       #print row[0]
                       #print "movies Id: " + row[2]
                       movieIds.append(row[2])                 
    return  movieIds
    

def index(request):
    if 'user' not in request.session:
        return HttpResponseRedirect('/polls/signin');
    user = request.session['user']
    search = ""
    m = []
    if request.method == 'POST':
        search = request.POST['search']
        print "search:" + search
    # if search in "1::Toy Story (1995)::Animation|Children's|Comedy":
    #     print "co roi ne"
    else:
         return render(request, 'index.html')  

    movieIds = []
    fileDat = open("movies.dat","r")
    lines = fileDat.readlines()
    for item in lines:
        #print item.decode('iso-8859-1').encode('utf8')
        with open('links.csv') as fileCsv:
            reader = csv.reader(fileCsv) 
            if (search.lower() in item.lower()):
                #print "item: " + item
                index = item.index("::")
                item = item[0:index]
                #print "item slit: " + item
                for row in reader:
                    if row[0] == item:
                       #print row[0]
                       #print "movies Id: " + row[2]
                       movieIds.append(row[2]) 
            #print movieIds
           
    loops = []
    for item in range(1,len(movieIds)+1):
        print item
        print len(movieIds)
        loops.append(item)
    return render(request, 'search.html', {'movieIds':json.dumps(movieIds), 'length':loops})
    

def signin(request):
    
    mostpopular = 6
    lengthMostPopular = []
    for item in range(1,mostpopular+1):
        lengthMostPopular.append(item)

    length = 36
    if request.method == 'POST':
        userName = request.POST['username']
        request.session['user'] = userName
    handle = open(userName,"r+")
    
    
    
    engine_client = predictionio.EngineClient(url="http://localhost:8000")
    r = engine_client.send_query({"user": userName, "num": length})
    m = json.dumps(r)
    js = json.loads(m)
    loops = []
    for item in range(1,length+1):
        loops.append(item)
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
    return render(request, 'index.html', {'movieIds':json.dumps(movieIds), 'length':loops, 'lengthMostPopular':lengthMostPopular})
    #return HttpResponse(json.dumps(movieIds))
    
def recommend(request):
    if request.method == 'GET':
        return render(request, 'index.html')

def search(request):
    return true

def signout(request):
    print "signout"
    if request.method == 'GET':
        return render(request, 'signin.html')

def single(request):
    if request.method == 'POST':
        newuser = request.POST['newuser']
        print "newuser:" + newuser + "\n"

    return render(request, "single.html")
