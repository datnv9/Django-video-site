from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponseRedirect
import urllib2
import predictionio
import json
import csv
import os.path


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
    #print user

    mostpopular = 12
    lengthMostPopular = []
    for item in range(1,mostpopular+1):
        lengthMostPopular.append(item)

    length = 36

    engine_client = predictionio.EngineClient(url="http://localhost:8000")
    r = engine_client.send_query({"user": user, "num": length, "blackList": request.session['blacklist']})
    m = json.dumps(r)
    js = json.loads(m)
    loops = []
    #for index in range(0:3):
    movieIds = []
    movielensIds = []
    
    #Write file Watched
    user = request.session['user']
    print user
    # if request.session['mid'] is not None:
    #     watchedFilm = request.session['mid']
    #     print watchedFilm
    #     watchedFile = open(user+'watched.txt','a')
    #     print "da ghi"
    #     watchedFile.write(watchedFilm)
    #     watchedFile.write('\n')
    #     watchedFile.close()

    movies = []
    movies.append('0')
    #Read file Watched

    #Read file csv
    check = 1    
    for item in js['itemScores']:
        #print item
        with open('links.csv') as file:
            reader = csv.reader(file) 
            for row in reader:
                if row[0] == item['item']:
                    movieIds.append(row[2])
                    movielensIds.append(row[0])
    print movieIds
    #Remove duplicate of moviewIds                       
    # newlistMoviewIds = []                        
    # for i in movieIds:
    #     if i not in movies:
    #         newlistMoviewIds.append(i)
    # print newlistMoviewIds
    #Remove duplicate of movielensIds
    # newlistMovieLensIds = []                        
    # for i in movieIds:
    #     if i not in newlistMovieLensIds:
    #         newlistMovieLensIds.append(i)
            
    for item in range(1,13):
        loops.append(item)
    return render(request, 'index.html', {'movieIds':json.dumps(movieIds), 'movielensIds': json.dumps(movielensIds), 'length':loops, 'lengthMostPopular':lengthMostPopular})
    if search in "1::Toy Story (1995)::Animation|Children's|Comedy":
        print "co roi ne"
    return render(request, 'index.html')

def signin(request):
    if 'user' in request.session:
        return HttpResponseRedirect('/polls/')
    if request.method == 'POST':
        userName = request.POST['username']
        request.session['user'] = userName
        #handle = open(userName,"r+")
        #Write file users
        fileName = ""+ userName + ".txt"
        blacklist = []
        if os.path.isfile(fileName):
            with open(fileName, "r") as myfile:
                for line in myfile:
                    blacklist.append(line)
        request.session['blacklist'] = blacklist
        return HttpResponseRedirect('/polls/')
    else:
        return render(request, 'signin.html')
    
    #return HttpResponse(json.dumps(movieIds))
    
def recommend(request):
    if 'user' in request.session:
        user = request.session['user']
        length = 38
        engine_client = predictionio.EngineClient(url="http://localhost:8000")
        r = engine_client.send_query({"user": user, "num": length, "blackList": request.session['blacklist']})
        m = json.dumps(r)
        js = json.loads(m)
        movieIds = []
        movielensIds = []
        #Read file csv
        for item in js['itemScores']:
            #print "item:" + item
            with open('links.csv') as file:
                reader = csv.reader(file) 
                for row in reader:
                    if row[0] == item['item']:
                        # with open("backlist.dat") as fileb:
                        #     bls = file.readlines()
                        #     for bl in bls:
                        #         if bl != row[0]:
                                    movieIds.append(row[2])
                                    movielensIds.append(row[0])
        loops =[]
        for item in range(1,len(movieIds)+1):
            loops.append(item)
        return render(request, 'recommend.html',{'movieIds':json.dumps(movieIds), 'length': loops, 'movielensIds': json.dumps(movielensIds)})

def search(request):
    search = ""
    m = []
    movieIds = []
    movielensIds = []
    loops = []
    if request.method == 'GET':
        search = request.GET['search']
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
                            movielensIds.append(row[0])
                #print movieIds
        for item in range(1,len(movieIds)+1):
            print item
            print len(movieIds)
            loops.append(item)
    return render(request, 'search.html', {'movieIds':json.dumps(movieIds), 'length':loops, 'movielensIds': json.dumps(movielensIds)})

def signout(request):
    print "signout"
    if request.method == 'GET':
        if 'user' in request.session:
            del request.session['user']
        return HttpResponseRedirect('/polls/signin')

def single(request):
    if request.method == 'GET':
        mid = request.GET['mid']
        request.session['mid'] = mid
        print "mid: " + mid
            
        request.session['mid'] = mid

        item = 0

        with open('links.csv') as file:
            reader = csv.reader(file) 
            for row in reader:
                if row[2] == mid:
                    item = row[0]
        
        user = request.session['user']
        print "mid:" + mid + "\n"
        print "item:" + item
        client = predictionio.EventClient(
            access_key="9AGBBsMkyqSCHsbLsm1XL6I9ppt0WqNXW_O-fuY0yKoWw5j-_r7uiWA56LADGi9O",
            url="http://localhost:7070",
            threads=5,
            qsize=500
        )
        client.create_event(
            event="buy",
            entity_type="user",
            entity_id=user,
            target_entity_type="item",
            target_entity_id=item
        )

    return render(request, "single.html", {'movieId':mid})


def rate(request):
    print 'rate'
    print request.session['mid']
    if request.method == 'POST':
        user = request.session['user']
        print "da nhan request"
        rate = request.POST['rate']
        mid = request.session['mid']
        #blackListFile = open("blacklist.dat","a")
        
        #lines = blackListFile.readlines()
        #for it in lines:

        item = 0

        with open('links.csv') as file:
            reader = csv.reader(file) 
            for row in reader:
                if row[2] == mid:
                    item = row[0]
                    blacklist = request.session['blacklist']
                    blacklist.append(item)
                    request.session['blacklist']=blacklist
                    with open(user+".txt", 'a') as file:
                        file.write(item + '\n')
                    break

        client = predictionio.EventClient(
            access_key="9AGBBsMkyqSCHsbLsm1XL6I9ppt0WqNXW_O-fuY0yKoWw5j-_r7uiWA56LADGi9O",
            url="http://localhost:7070",
            threads=5,
            qsize=500
        )
        client.create_event(
            event="rate",
            entity_type="user",
            entity_id=user,
            target_entity_type="item",
            target_entity_id=item,
            properties= { "rating" : float(rate) }
        )
    #rate = filter(None,rate)
    #print rate    
    return render(request, "single.html", {'movieId':request.session['mid']})
