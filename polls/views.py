from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponseRedirect
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
        return HttpResponseRedirect('/polls/signout')
       #return HttpResponseRedirect('/polls')
    user = request.session['user']
    print user

    mostpopular = 12
    lengthMostPopular = []
    for item in range(1,mostpopular+1):
        lengthMostPopular.append(item)

    length = 12

    engine_client = predictionio.EngineClient(url="http://localhost:8000")
    r = engine_client.send_query({"user": user, "num": length})
    m = json.dumps(r)
    js = json.loads(m)
    loops = []
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
    for item in range(1,len(movieIds)+1):
        loops.append(item)
    return render(request, 'index.html', {'movieIds':json.dumps(movieIds), 'length':loops, 'lengthMostPopular':lengthMostPopular})
    # if search in "1::Toy Story (1995)::Animation|Children's|Comedy":
    #     print "co roi ne"
    

def signin(request):
    if 'user' in request.session:
        return HttpResponseRedirect('/polls/')
    if request.method == 'POST':
        userName = request.POST['username']
        request.session['user'] = userName
        #handle = open(userName,"r+")
        #Write file users
        with open("users.txt", "a") as myfile:
            myfile.write(userName + '\n')
        return HttpResponseRedirect('/polls/')
    else:
        return render(request, 'signin.html')
    
    #return HttpResponse(json.dumps(movieIds))
    
def recommend(request):
    if 'user' in request.session:
        user = request.session['user']
        length = 12
        engine_client = predictionio.EngineClient(url="http://localhost:8000")
        r = engine_client.send_query({"user": user, "num": length})
        m = json.dumps(r)
        js = json.loads(m)
        movieIds = []
        #Read file csv
        for item in js['itemScores']:
            print item
            with open('links.csv') as file:
                reader = csv.reader(file) 
                for row in reader:
                    if row[0] == item['item']:
                        movieIds.append(row[2])
        loops =[]
        for item in range(1,len(movieIds)+1):
            loops.append(item)
        return render(request, 'recommend.html',{'movieIds':json.dumps(movieIds), 'length': loops})

def search(request):
    search = ""
    m = []
    movieIds = []
    loops = []
    if request.method == 'POST':
        search = request.POST['search']
        print "search:" + search
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
        for item in range(1,len(movieIds)+1):
            print item
            print len(movieIds)
            loops.append(item)
    return render(request, 'search.html', {'movieIds':json.dumps(movieIds), 'length':loops})

def signout(request):
    print "signout"
    if request.method == 'GET':
        if 'user' in request.session:
            del request.session['user']
        return HttpResponseRedirect('/polls/signin')

def single(request):
    if request.method == 'POST':
        mid = request.POST['mid']
        request.session['mid'] = mid
        print "mid:" + mid + "\n"

    return render(request, "single.html", {'movieId':mid})


def rate(request):
    print 'rate'

    print request.session['mid']
    if request.method == 'POST':
        print "da nhan request"
        rate = request.POST['rate']
        print rate
    #rate = filter(None,rate)
    #print rate    
    return render(request, "single.html", {'movieId':request.session['mid']})