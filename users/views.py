
from django.shortcuts import render
import mysql.connector
from operator import itemgetter
import pymongo
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import math
def rank_machine(ip):
    # if(ip<=47):
    #     return -1
    if(ip>=175):
         return 1
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mongoproject"]
    table = mydb["mark_rank"]
    mark = list()
    rank = list()
    for x in table.find():
      mark.append(x["mark"])
      rank.append(x["rank"])
    plt.plot(rank,mark)
    print(len(mark))
    print(rank)
    xnew = np.linspace(0, 180, num=400, endpoint=True)#gives range of numbers
    f2 = interp1d(mark, rank , kind='quadratic') # gives quadratic relation between rank and marks
    print(math.ceil(f2(ip)))
    return math.ceil(f2(ip))
# Create your views here.

def getcolleges():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )
    query = "select * from college"
    cursor = db.cursor()

    cursor.execute(query)
    records = cursor.fetchall()
    list1 = []
    for i in records:
        list1.append((i[0].replace("\xa0", " "), i[1]))
    return list1


def getcategory():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )
    query = "select * from cat"
    cursor = db.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    list = []
    for i in records:
        list.append(i[0])
    return list


def getcourse():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )
    query = "select * from course"
    cursor = db.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    list = []
    for i in records:
        list.append((i[0].replace("\n", " "), i[1]))
    return list


def tuple_to_string(t):
    str = ''
    for i in t:
        str = str + i
    return str


def calculatecutoff(college, course, category):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )
    query = "select cutoff_rank from cutoff WHERE cat_id=%s and college_id=%s and course_id=%s"
    tupple = (category, college, course)
    cursor = db.cursor()
    cursor.execute(query, tupple)
    records = cursor.fetchall()
    try:
        #print( "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        (x ,a , b) = predict_extrapolate(college, course, category)
        print(x,a,b,"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        x = int(x)    #predicted rank
        a = int(a)      #interceptt
        b = int(b)    #Slope
        if(b<0):return ("The predicted Cutoff for course specified is: "+str(x),"\n   College or Course Trend is increasing")
        else:
            if (b > 0 and b<800): return ("The predicted Cutoff is: "+ str(x),"\n     College or Course Trend is Steady")
            else:
                if(b > 800):
                    return ("The predicted Cutoff for course specified is: "+ str(x),"\n       College or Course Trend is decreasing")
    except:
        return ("THE GIVEN COURSE IS NOT AVAILABLE AT THIS COLLEGE","")

def pred_coll(college,course,cat,rank):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )
    cursor = db.cursor()
    if (course == "NIL"):
        query = "select course_id from cutoff WHERE cat_id=%s and college_id=%s and year =2020"
        tupple = (cat, college)
        cursor.execute(query, tupple)
        result = list(cursor.fetchall())
        IDS = list()
        print(result, "Reeee")
        for x in range(len(result)):
            course = str(result[x])
            print(course)
            # print(predict_extrapolate(x, course, cat),"aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # print(str(x[0]))
            shr = predict_extra1(college, course, cat)
            if (type(shr) is not None):
                if (int(rank) < (shr + (shr / 20))): IDS.append(course)
            list2=list()
            list1=getcourse()
            for j in IDS:
                print("THIS IS J:", j[2:5])
                for i in list1:
                    print("This id i", i[1])
                    if (i[1] == j[2:5]):        #i[0] has course names
                        list2.append(i[0])

    if (college == "NIL"):
        query = "select college_id from cutoff WHERE cat_id=%s and course_id=%s and year =2020"
        tupple = (cat, course)
        cursor.execute(query, tupple)
        result = list(cursor.fetchall())
        IDS = list()
        for x in range(len(result)):
            college = str(result[x])
            #print(college)
            # print(predict_extrapolate(x, course, cat),"aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # print(str(x[0]))
            shr = predict_extra2(college, course, cat)
            print(college,"              ",int(shr))
            if (type(shr) is not None):
                if (int(rank) < (int(shr) + (int(shr) / 20))):
                    IDS.append(college)
                    # print("In iffff and sucessss",college)

        list1 = getcolleges()
        list2 = list()
        for j in IDS:
            for i in list1:
                if (i[1] == j[2:6]):
                    list2.append(i[0])
    if (len(IDS) < 1):
        return "Course/ College NOT FOUND"
    else:
        return list2
def displaycutoff(request):
    col = request.POST.get('college')
    cat = request.POST.get('category')
    cou = request.POST.get('course')
    rank = request.POST.get('rank')
    option = request.POST.get('option')
    cou = cou + ' '
    cutoff = calculatecutoff(col, cou, cat)
    if (option == 'COLLEGE'):
        col='NIL'
    else:
        cou='NIL'
    cutoff1 = pred_coll(col,cou,cat,rank)
    return render(request, 'cutoff.html', {'result': cutoff,'result1':cutoff1})

def clgtrend(college, course):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )
    query = "select year,cutoff_rank from cutoff WHERE college_id=%s and course_id=%s and cat_id=%s"
    category = "GM"
    tupple = (college, course, category)
    cursor = db.cursor()
    cursor.execute(query, tupple)
    records = cursor.fetchall()
    query = "SELECT year, cutoff_rank from cutoff where college_id"
    print(records)


def home(request):
    #list1 = getcolleges()
    #list_cou = getcourse()
    #list_cat = getcategory()
    #return render(request, "home.html", {'lists': list1, 'lists_category': list_cat, 'lists_course': list_cou})
    return render(request,"base.html")


def func(x, a, b):
    return a + b * x

def funcexp(x, a, b):
    return a + (x**b)


def predict_extrapolate(college, course, cat):
    # college = str(input())
    # course = str(input())
    # cat = str(input())

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )

    mycursor = db.cursor()

    query = "SELECT * FROM cutoff where (college_id={col_id} and course_id = {cor_id} and cat_id = {c_id})".format(
        col_id='"' + college + '"', cor_id='"' + course + '"', c_id='"' + cat + '"')
    mycursor.execute(query)
    result = list(mycursor.fetchall())
    print(result,course,college[2:6],cat)
    # print(result)
    x_data = list()
    y_data = list()
    i = 2020
    data = list()
    if (len(result) > 2):
        for x in result:
            data.append((int(x[0]), int(x[1])))             #x[0] is year and x[1] is rank
    else:
        print("No Data")
        return 99999999
    flag = True
    data.sort()                                     #data=[(2009,1234),....]
    print("XXXXXXXXXXXXXX_DAAAAAATAAAAAAAAAA ",x_data,data)
    for i in range(0, len(x_data) - 1):
        print("XXXXXXXXXXXXXX_DAAAAAATAAAAAAAAAA ", x_data, data)
        if (len(data) < 2):
            flag = False
        if (data[i][0] - x_data[i + 1][0] != 1):
            flag = False
    if (flag == False):
        print("No data")
        return 9999999
    print(data)
    for i in range(0, len(data)):                       #i gives 0 for 2009,1 for 2010,.... and data[i][1] gives rank corresponding
        x_data.append(i)
        y_data.append(data[i][1])
    x_data = np.array(x_data)
    x1=list()
    y_data = np.array(y_data)
    plt.plot(x_data, y_data, 'bo', label=college + "  " + course + "  " + cat)#'bo' blue circle markers
    print("Points.......",y_data)
    if(y_data[0]/y_data[-1]<=10):
        popt, pcov = curve_fit(func, x_data, y_data, p0=[sum(y_data) / len(y_data), 6]) # function takes func() defined above, x and y data, p0 as initial estimated values of intercept and slope)
    else:
        popt, pcov = curve_fit(funcexp, x_data, y_data, p0=[sum(y_data) / len(y_data), 6])
    print(popt)#intercept, slope (type ndarray)
    print(pcov)#covariaance matrix
    print(sum(y_data) / len(y_data))
    xFit = np.arange(0.0, 12.0, 0.01) #gives an array of number spaced by 0.01 between 0 to 5
    plt.plot(xFit, func(xFit, *popt), 'r', label="data")# plots the straight line showing the trend
    plt.xlabel("Year")
    plt.ylabel("Rank")
    plt.legend() # shows the data on top left of graph
    plt.xlim(-1, 13)
    plt.ylim(min(y_data) - max(y_data)*0.1, max(y_data) + max(y_data)*0.1)
    plt.show()
    # plt.savefig("output.jpg")
    j = 0
    if (y_data[-1] > y_data[-2] and popt[1] > 0):
        print(func(len(y_data) - j, *popt),"xxx",y_data[-1],y_data[-2])
        while (func(len(y_data) - j, *popt) < y_data[-1]):      #len(y_data)=12
            j -= 1
            print(func(len(y_data) - j, *popt))
            print(1)
    else:
        print(func(len(y_data) - j, *popt),"xxx",y_data[-1],y_data[-2])
        if (y_data[-1] > y_data[-2] and popt[1] < 0):
            while (func(len(y_data) - j, *popt) < y_data[-1]):
                j += 1
                print(2)
        else:
            if (y_data[-1] < y_data[-2] and popt[1] > 0):
                print(func(len(y_data) - j, *popt), "xxx", y_data[-1], y_data[-2])
                while (func(len(y_data) - j, *popt) < y_data[-1]):
                    j -= 1
                    print(3)
            else:
                if (y_data[-1] < y_data[-2] and popt[1] < 0):
                    while (func(len(y_data) - j, *popt) < y_data[-1]):
                        j += 1
                        print(func(len(y_data) - j, *popt))
                        print(4)
    return (func(len(y_data) - j, *popt),*popt)


def predict_extra1(college, course, cat):       #called to redict course
    # college = str(input())
    # course = str(input())
    # cat = str(input())

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )

    mycursor = db.cursor()
    query = "SELECT * FROM cutoff where (college_id={col_id} and course_id = {cor_id} and cat_id = {c_id})".format(
        col_id='"' + college + '"', cor_id='"' + course[2:5] + '"', c_id='"' + cat + '"')
    mycursor.execute(query)
    result = list(mycursor.fetchall())
    print(result,course,college[2:6],cat)
    # print(result)
    x_data = list()
    y_data = list()
    i = 2020
    data = list()
    if (len(result) > 2):
        for x in result:
            data.append((int(x[0]), int(x[1])))         #x[0] has year and x[1] cutoff_rank
    else:
        print("No Data")
        return 99999999
    flag = True
    data.sort()
    for i in range(0, len(x_data) - 1):
        if (len(data) < 2):
            flag = False
        if (data[i][0] - x_data[i + 1][0] != 1):
            flag = False
    if (flag == False):
        print("No data")
        return 9999999
    print(data)
    for i in range(0, len(data)):
        x_data.append(i)
        y_data.append(data[i][1])
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    plt.plot(x_data, y_data, 'bo', label=college + "  " + course + "  " + cat)
    popt, pcov = curve_fit(func, x_data, y_data, p0=[sum(y_data) / len(y_data), 6])
    print(popt)
    print(sum(y_data) / len(y_data))
    xFit = np.arange(0.0, 5.0, 0.01)
    plt.plot(xFit, func(xFit, *popt), 'r', label="data")
    plt.xlabel("Year")
    plt.ylabel("Rank")
    plt.legend()
    plt.xlim(-3, 15)
    plt.ylim(min(y_data) - 50, max(y_data) + 50)
    # plt.show()
    # plt.savefig("output.jpg")
    j = 0
    if (y_data[-1] > y_data[-2] and popt[1] > 0):
        while (func(len(y_data) - j, *popt) < y_data[-1]):
            j -= 1
            print(func(len(y_data) - j, *popt))
            print(1)
    else:
        if (y_data[-1] > y_data[-2] and popt[1] < 0):
            while (func(len(y_data) - j, *popt) < y_data[-1]):
                j += 1
                print(2)
        else:
            if (y_data[-1] < y_data[-2] and popt[1] > 0):
                while (func(len(y_data) - j, *popt) < y_data[-1]):
                    j -= 1
                    print(3)
            else:
                if (y_data[-1] < y_data[-2] and popt[1] < 0):
                    while (func(len(y_data) - j, *popt) < y_data[-1]):
                        j += 1
                        print(func(len(y_data) - j, *popt))
                        print(4)
    return (func(len(y_data) - j, *popt))           #called to
def predict_extra2(college, course, cat):       #called to redict college
    # college = str(input())
    # course = str(input())
    # cat = str(input())

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )

    mycursor = db.cursor()
    query = "SELECT * FROM cutoff where (college_id={col_id} and course_id = {cor_id} and cat_id = {c_id})".format(
        col_id='"' + college[2:6] + '"', cor_id='"' + course + '"', c_id='"' + cat + '"')
    mycursor.execute(query)
    result = list(mycursor.fetchall())
    print(result,course,college[2:6],cat)
    # print(result)
    x_data = list()
    y_data = list()
    i = 2020
    data = list()
    if (len(result) > 2):
        for x in result:
            data.append((int(x[0]), int(x[1])))
    else:
        print("No Data")
        return 99999999
    flag = True
    data.sort()
    for i in range(0, len(x_data) - 1):
        if (len(data) < 2):
            flag = False
        if (data[i][0] - x_data[i + 1][0] != 1):
            flag = False
    if (flag == False):
        print("No data")
        return 9999999
    print(data)
    for i in range(0, len(data)):
        x_data.append(i)
        y_data.append(data[i][1])
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    plt.plot(x_data, y_data, 'bo', label=college + "  " + course + "  " + cat)
    popt, pcov = curve_fit(func, x_data, y_data, p0=[sum(y_data) / len(y_data), 6])
    print(popt)
    print(sum(y_data) / len(y_data))
    xFit = np.arange(0.0, 5.0, 0.01)
    plt.plot(xFit, func(xFit, *popt), 'r', label="data")
    plt.xlabel("Year")
    plt.ylabel("Rank")
    plt.legend()
    plt.xlim(-3, 15)
    plt.ylim(min(y_data) - 50, max(y_data) + 50)
    # plt.show()
    # plt.savefig("output.jpg")
    j = 0
    if (y_data[-1] > y_data[-2] and popt[1] > 0):
        while (func(len(y_data) - j, *popt) < y_data[-1]):
            j -= 1
            print(func(len(y_data) - j, *popt))
            print(1)
    else:
        if (y_data[-1] > y_data[-2] and popt[1] < 0):
            while (func(len(y_data) - j, *popt) < y_data[-1]):
                j += 1
                print(2)
        else:
            if (y_data[-1] < y_data[-2] and popt[1] > 0):
                while (func(len(y_data) - j, *popt) < y_data[-1]):
                    j -= 1
                    print(3)
            else:
                if (y_data[-1] < y_data[-2] and popt[1] < 0):
                    while (func(len(y_data) - j, *popt) < y_data[-1]):
                        j += 1
                        print(func(len(y_data) - j, *popt))
                        print(4)
    return (func(len(y_data) - j, *popt))



#----------------------------------------------------------------------------------------------------------------------
def finalcutoff(request):
    list1 = getcolleges()
    list_cou = getcourse()
    list_cat = getcategory()
    print(list1)
    return render(request, "getcutoff.html", {'lists': list1, 'lists_category': list_cat, 'lists_course': list_cou})

def finaldisplaycutoff(request):
    col = request.POST.get('college') #In html <select> cannot be referenced
    print(col)
    cat = request.POST.get('category')
    cou = request.POST.get('course')
    cou = cou + ' '
    if(cat=="Select a Category"):
        return render(request,"error.html")
    cutoff = finalcalculatecutoff(col, cou, cat)
    if(len(cutoff)==0):
        return render(request,"error1.html")
    return render(request,"cutoff.html",{'lists':cutoff})


def finalcalculatecutoff(college, course, category):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )
    query = "select year,cutoff_rank from cutoff WHERE cat_id=%s and college_id=%s and course_id=%s"
    tupple = (category, college, course)
    cursor = db.cursor()
    cursor.execute(query, tupple)
    records = cursor.fetchall()
    list1=list()
    for i in records:
        list1.append(i)
    list1.sort(key=itemgetter(0),reverse=True)
    return list1
#-----------------------------------------------------------------------------------------------------------------------
def finalpredcollege(request):
    list1 = getcolleges()
    list_cou = getcourse()
    list_cat = getcategory()
    return render(request,"predcollege.html", {'lists': list1, 'lists_category': list_cat, 'lists_course': list_cou})

def disfinalpredcollege(request):
    rank = request.POST.get('rank')
    cat = request.POST.get('category')
    cou = request.POST.get('course')
    cou = cou + ' '
    try:
        x = int(rank) + 1
    except:
        l = list()
        l.append("Rank input incompatible")
        return render(request, "dispredcourse.html", {'lists': l})

    if (str(cat) == "Select a Category"):
        l = list()
        l.append("Select valid category")
        return render(request, "dispredcourse.html", {'lists': l})

    cutoff =pred_coll('NIL',cou,cat,rank)
    if(cutoff=="Course/ College NOT FOUND"):
        l=list()
        l.append("Course/ College not found")
        return render(request, "dispredcollege.html", {'lists': l})
    return render(request, "dispredcollege.html", {'lists': cutoff})
#----------------------------------------------------------------------------------------------------------------------
def finalpredcourse(request):
    list1 = getcolleges()
    list_cou = getcourse()
    list_cat = getcategory()
    return render(request, "predcourse.html", {'lists': list1, 'lists_category': list_cat, 'lists_course': list_cou})

def disfinalpredcourse(request):
    rank = request.POST.get('rank')
    cat = request.POST.get('category')
    col = request.POST.get('college')
    try:
        x=int(rank)+1
    except:
        l = list()
        l.append("Rank input incompatible")
        return render(request, "dispredcourse.html", {'lists': l})

    if (str(cat)=="Select a Category"):
        l = list()
        l.append("Select valid category")
        return render(request, "dispredcourse.html", {'lists': l})

    cutoff =pred_coll(col,"NIL",cat,rank)
    if (cutoff == "Course/ College NOT FOUND"):
        l = list()
        l.append("Course/ College NOT FOUND")
        return render(request, "dispredcourse.html", {'lists': l})
    return render(request, "dispredcourse.html", {'lists': cutoff})

#--------------------------------------------------------------------------------------------------------College trends
def kct(request):
    list1 = getcolleges()
    list_cou = getcourse()
    list_cat = getcategory()
    return render(request, "kct.html", {'lists': list1, 'lists_category': list_cat, 'lists_course': list_cou})

def diskct(request):
    cou=request.POST.get('course')
    cou=cou+' '
    cat = request.POST.get('category')
    col = request.POST.get('college')
    print("VAIBHAVVVVVVVVVVVVVVVVVVVVVVVV ",cat)
    if (cat == "" or cat == "Select a Category" or cat==None):
        return render(request, "error.html")
    (cutoff,cutoff1) =calculatecutoff(col,cou,cat)
    return render(request, "diskct.html", {'lists': cutoff,'lists1':cutoff1})
#--------------------------------------------------------------------------------------------------------Rank predict

def rank_form(request):
    return render(request,"rank_form.html")
def disrank(request):
    m = request.POST.get('maths')
    c = request.POST.get('physics')
    p = request.POST.get('chemistry')
    res=int(m)+int(c)+int(p)
    print("totallll",res)
    if(int(m)>60 or int(c)>60 or int(p)>60):
        l="Invalid input and marks out of bound"
        print("Hello")
        return render(request, "disrank.html", {'lists': l})
    if(res==-1):
        l="Greater than or Equal to 55000 "
        return render(request, "disrank.html", {'lists': l})

    res=int(rank_machine(res))
    #print(res)
    return render(request,"disrank.html",{'lists': res})
#
#----------------------------------------------------------------------------------------------------Create account
def authenticate(request):
    return render(request, "homepage.html")
def createaccount(request):
    return render(request,"accountcreate.html")
def accountcreated(request):
    name= request.POST.get('name')
    password = request.POST.get('password')
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )
    query1 = "select number from weblogin where (%s,%s) NOT IN (select name,password from weblogin)"
    tupple = (name, password)
    cursor = db.cursor()
    cursor.execute(query1, tupple)
    records = cursor.fetchall()
    if(len(records)==0):
        print("yesssssssssssss")
        return render(request,"loginerror.html")
    query2 = "select MAX(number) from weblogin"
    cursor = db.cursor()
    cursor.execute(query2)
    records = cursor.fetchall()
    print("PRINARYYYYYYYYYYYYYYYY KEYYYYYYYYYYYYYYYY ",records[0][0],name,password)
    num=int(records[0][0])+1
    num1=str(num)
    query = "INSERT INTO weblogin (number,name,password) VALUES (%s,%s,%s) "
    tupple = (num1,name,password)
    cursor = db.cursor()
    cursor.execute(query, tupple)
    db.commit()
    return render(request, "accountcreated.html")
#------------------------------------------------------------------------------Login
def login(request):
    return render(request,"logincheck.html")

def loginsuccess(request):
    name = request.POST.get('name')
    password = request.POST.get('password')
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="project"
    )
    query1 = "select number from weblogin where (%s,%s) IN (select name,password from weblogin)"
    tupple = (name, password)
    cursor = db.cursor()
    cursor.execute(query1, tupple)
    records = cursor.fetchall()
    if (len(records) >0):
        return render(request, "loginsuccess.html")
    else:
        return render(request,"loginerror.html")
# predict_extrapolate("E005","CE ","GM")