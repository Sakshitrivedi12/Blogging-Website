from django.shortcuts import render,redirect
from.models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from datetime import date


# Create your views here.
def All_category():
    all_cat = Category.objects.all()
    return all_cat

def Recent_and_popular():
    allpost = Post.objects.all()
    recent_three = allpost[::-1][:3]
    like = []
    le = len(allpost)
    newpost = []
    for i in allpost:
        l = LikeComment.objects.filter( post_data=i,like=True).count()
        like.append(l)

        for i in range (le):
            if max(like) > 0:
                m = max(like)
                p = like.index(m)
                po = allpost[p]
                like.pop(p)
                like.insert(p,0)
                newpost.append(po)
        top_three = newpost[:3]
        return top_three,recent_three



def Home(request):
    all_post = Post.objects.all()
    li = []
    for i in all_post:
        like = LikeComment.objects.filter(post_data=i,like = True).count()
        li.append(like)

    z = zip(all_post,li)
    top3,recent3 = Recent_and_popular()
    d= {"allcat":All_category(),"all_post":z,"top3":top3,"recent3":recent3}
    return render(request,'index.html',d)

def about(request):
    d = {"allcat": All_category()}
    return render(request,'about.html',d)

def Login(request):
    error = False
    if request.method == 'POST':
        x = request.POST
        us = x['usr']
        pa =x['pas']
        user = authenticate(username = us, password = pa)

        if user:
            login(request,user)
            return redirect('home')
        else:
            error = True

    d = {"allcat": All_category(),"error":error}
    return render(request,'login.html',d)

def contact(request):
    d = {"allcat": All_category()}
    return render(request,'contact.html',d)

def signup(request):
    error = False

    if request.method == "POST":
        dd = request.POST
        n = dd['name']
        u = dd['usrn']
        e = dd['em']
        p = dd['pwd']
        i = request.FILES['img']
        udata = User.objects.filter(username=u)
        if udata:
            error = True
        else:
            user = User.objects.create_user(username = u,password = p,email = e,first_name = n)
            user_detail.objects.create(user_d=user,image = i)
            return redirect('login')
    d = {"allcat": All_category(),"error":error}
    return render(request,'signup.html',d)


def Blog_detail(request,bid):
    detail = Post.objects.get(id=bid)
    d = {"allcat": All_category(),"detail":detail}
    return render(request,'singlepage.html',d)

def Like_post(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    data = Post.objects.get(id = pid)
    data2 = LikeComment.objects.filter(usr = request.user,like = True,post_data = data)

    if not data2:
        data3 = LikeComment.objects.filter(post_data = data,usr=request.user).first()
        if data3:
            data3.like = True
            data3.save()
        else:
            LikeComment.objects.create(post_data = data,usr = request.user,like = True)
        return redirect('home')
    else:
        return redirect('home')

def Logout(request):
    logout(request)
    return redirect('login')

def Post_comment(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    pdata = Post.objects.get(id=pid)
    user = request.user
    td = date.today()
    if request.method == "POST":
        d = request.POST
        c = d['Message']
        data = LikeComment.objects.filter(usr = request.user,post_data=pdata).first()
        if data:
            data.comment = c
            data.save()
        else:
            LikeComment.objects.create(usr=user, post_data=pdata,comment=c,date=td)
        return redirect('blog_d',pid)


def Myblogs(request):
    data = Post.objects.filter(usr=request.user)
    d = {"allcat": All_category(),"mdata":data}

    return render(request,'fashion.html',d)

def blog_delete(request,bid):
    data=Post.objects.get(id=bid)
    data.delete()
    return redirect('myblog')


def category_detail(request,cid):
    cdata=Category.objects.get(id=cid)
    d = {"allcat": All_category(),"cdata":cdata}

    return render(request,'detail.html',d)


from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def add_blog(request):
    if request.method == "POST":
        dd = request.POST
        t = dd['title']
        s = dd['short']
        l = dd['long']
        c = dd['cat']
        i = request.FILES['img']
        cdata = Category.objects.get(id=c)
        User = request.user
        td = date.today()
        Post.objects.create(cat=cdata,title=t,usr=User,date=td,short_des=s,Long_des=l,image=i)
        from_email = setting.EMAIL_HOST_USER
        to_email = user.email
        sub = "Blog Added"
        msg = EmailMultiAlternatives(sub,'',from_email,[to_email])
        dic = {"title":t,"short":s}
        html = get_template('mail.html').render(dic)
        return redirect('myblog')

    d = {"allcat": All_category()}
    return render(request,'add_blog.html',d)


def Change_Image(request):
    udata = user_detail.objects.filter(user_d=request.user).first()
    if request.method == "POST":
        i=request.FILES['img']
        udata.image=i
        udata.save()
        return redirect('myblog')
    d = {"allcat": All_category(),"udata":udata}
    return render(request,'change_pro.html',d)

def change_pas(request):
    error = False
    if request.method == "POST":
        o = request.POST['old']
        n = request.POST['new']
        data = authenticate(username=request.user.username,password=o)
        if data:
            data.set_password(n)
            data.save()
            logout(request)
            login(request,data)
            return redirect('myblog')
        else:
            error = True

    d = {"allcat": All_category(),"error":error}

    return render(request,'changepass.html',d)



