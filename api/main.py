# OM GANGANPATAY NAMAH
# HAR HAR MAHADEV
# JAI SHRI RAM
from flask import Flask, render_template, request, session, redirect,url_for,flash,send_from_directory
import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import datetime
import os
from werkzeug.utils import secure_filename
import random
import time
# db setup
conn = sqlite3.connect('flask.db')
conn.execute('CREATE TABLE IF NOT EXISTS dotchainstaff (\
ID VARCHAR(6) PRIMARY KEY NOT NULL UNIQUE,\
USERNAME VARCHAR(20) NOT NULL UNIQUE, \
PASSWORD TEXT NOT NULL, \
EMAIL TEXT NOT NULL UNIQUE,\
PHONENUMBER  INT NOT NULL UNIQUE,\
ADDRESS TEXT NOT NULL)')

conn.execute('CREATE TABLE IF NOT EXISTS dotchainblogtable (\
BLOGID VARCHAR(6) PRIMARY KEY NOT NULL UNIQUE,\
TITLE TEXT NOT NULL, \
KEYWORD TEXT NOT NULL, \
CONTENT TEXT NOT NULL,\
CATEGORY TEXT NOT NULL,\
DESCRIPTION TEXT NOT NULL,\
USERNAME VARCHAR(20) NOT NULL,\
DATE TIMESTAMP NOT NULL,\
OBJECTIVE TEXT NOT NULL,\
IMAGE TEXT NOT NULL,\
CODE INT NOT NULL)')

conn.close()
# /db setup


app = Flask(__name__)

app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = './api/uploads'

def news_slider(query):
  news=[]
  url=f"https://news.google.com/search?q={query}&hl=en-IN&gl=IN&ceid=IN%3Aen"
  html_content = requests.get(url).text
  soup = BeautifulSoup(html_content, "html.parser")
  news_data=soup.findAll('div',{'class':'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'})
  for i in news_data:
    title=i.find('h3',{'class':'ipQwMb ekueJc RD0gLb'})
    link="https://news.google.com"+title.find('a')['href']
    time=i.find('div',{'class':'SVJrMe'}).text
    figure=i.find('figure')
    image=figure.find('img')['src'] if figure else " "
    news.append([title.text,link,time,image])
  new_news=[]
  for i in news:
    if "minutes" in str(i[2]) or "hours" in str(i[2]):
      new_news.append(i) 
  return new_news

def news():
  news=[]
  url="https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen"
  html_content = requests.get(url).text
  soup = BeautifulSoup(html_content, "html.parser")
  maindiv=soup.findAll('article',{'class':'IBr9hb'})
  for i in maindiv:
    title=i.find('h4',{'class':'gPFEn'}).text
    image=i.find('img',{'class':'Quavad'})
    image=image.get('src') if image else " "
    time=i.find('time',{'class':'hvbAAd'}).text
    link=i.find('a',{'class':'WwrzSb'})['href']
    link="https://news.google.com"+link
    if len(news)!=4:
      news.append([title,image,time,link]) 
    if len(news)==4:
      break
  return news

def searchblogdataforall(query,pageno):
  conn = sqlite3.connect('flask.db')
  cursor = conn.cursor()
  if query=="all":
    cursor.execute('SELECT BLOGID,TITLE,CATEGORY,DESCRIPTION,DATE,IMAGE FROM dotchainblogtable ORDER BY DATE DESC LIMIT (?),(?)',(10*pageno-10,10))
  else:
    query=tuple(query.split(' '))
    cursor.execute('SELECT BLOGID,TITLE,CATEGORY,DESCRIPTION,DATE,IMAGE FROM dotchainblogtable WHERE CATEGORY=(?) or TITLE LIKE (?) ORDER BY DATE DESC LIMIT (?),(?)',(query[0].lower(),f"%{query[0]}%",10*pageno-10,10))
  blogdata=cursor.fetchall()
  conn.close()
  return blogdata

def showsearchdataemp(searchemp):
  conn = sqlite3.connect('flask.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM dotchainstaff WHERE ID =? OR USERNAME=?',(searchemp.strip(),searchemp.strip()))
  userdata=cursor.fetchall()
  conn.close()
  return userdata

def searchblogdata(query):
  conn = sqlite3.connect('flask.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM dotchainblogtable WHERE BLOGID=? OR USERNAME=? OR CATEGORY=? OR OBJECTIVE=? or TITLE LIKE ?',(query.strip(),query.strip(),query.lower(),query.lower(),f"%{query}%"))
  blogdata=cursor.fetchall()
  conn.close()
  return blogdata

def showdata():
  conn = sqlite3.connect('flask.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM dotchainstaff')
  userdata=cursor.fetchall()
  conn.close()
  return userdata

def isphonevalid(phone):
  if len(str(phone))==10 and str(phone).isdigit():
    return True;
  else:
    return False;

def isemailvalid(email):
  pattern=r"^[a-z]+\w+[\.]?[a-z 0-9]+[\w]?@+\w+\.+\w+."
  return re.search(pattern,email)


@app.route('/',methods=['GET','POST'])
def index():
  index_news=news_slider("ai")
  newsi=news()
  if request.method=="POST":
    dotchainsearch=request.form.get('dotchainsearch')
    return redirect(url_for('dotchainsearch',dotchainsearch=dotchainsearch,pageno=1))
  conn = sqlite3.connect('flask.db')
  cursor = conn.cursor()
  cursor.execute('SELECT BLOGID,TITLE,CATEGORY,DESCRIPTION,DATE,IMAGE FROM dotchainblogtable WHERE OBJECTIVE=(?) ORDER BY DATE DESC LIMIT (?)',('commercial',6))
  commercial=cursor.fetchall()
  cursor.execute('SELECT BLOGID,TITLE,CATEGORY,DESCRIPTION,DATE,IMAGE FROM dotchainblogtable WHERE OBJECTIVE=(?) ORDER BY DATE DESC LIMIT (?)',('homescreen',12))
  homescreen=cursor.fetchall()
  cursor.execute('SELECT BLOGID,TITLE,CATEGORY,DATE,IMAGE FROM dotchainblogtable ORDER BY DATE DESC LIMIT (?)',(10,))
  latest=cursor.fetchall()
  cursor.execute('SELECT BLOGID,TITLE,CATEGORY,DATE,IMAGE FROM dotchainblogtable WHERE OBJECTIVE=(?) ORDER BY DATE DESC LIMIT (?)',('homescreen',10))
  editors_pick=cursor.fetchall()
  conn.close()
  return render_template('index.html',index_news=index_news,commercial=commercial,homescreen=homescreen,newsi=newsi,latest=latest,editors_pick=editors_pick)

@app.route('/search/<dotchainsearch>/<int:pageno>')
def dotchainsearch(dotchainsearch,pageno):
  if pageno!=0:
    index_news=news_slider(dotchainsearch)
    blogdata=searchblogdataforall(dotchainsearch,pageno)
    if pageno==1:
      prev="#"
      next=f"/search/{dotchainsearch}/{pageno+1}"
    elif len(blogdata)<10:
      prev=f"/search/{dotchainsearch}/{pageno-1}"
      next="#"
    else:
      prev=f"/search/{dotchainsearch}/{pageno-1}"
      next=f"/search/{dotchainsearch}/{pageno+1}"
    return render_template('allblog.html',dotchainsearch=dotchainsearch,blogdata=blogdata,prev=prev,next=next,pageno=pageno,index_news=index_news)
  return render_template('error.html')
  
@app.route('/articles/page/<int:pageno>')
def articles(pageno):
  query="all"
  if pageno!=0:
    blogdata=searchblogdataforall(query,pageno)
    if pageno==1:
      prev="#"
      next=f"/articles/page/{pageno+1}"
    elif len(blogdata)<10:
      prev=f"/articles/page/{pageno-1}"
      next="#"
    else:
      prev=f"/articles/page/{pageno-1}"
      next=f"/articles/page/{pageno+1}"
    index_news=news_slider('top')
    return render_template('allblog.html',blogdata=blogdata,prev=prev,next=next,pageno=pageno,index_news=index_news)
  return render_template('error.html')

@app.route('/admin/<username>', methods=['GET','POST'])
def admin(username):
  if ('user' in session and session['user'] == "jaishriram"):
    if request.method=='POST':
      conn = sqlite3.connect('flask.db')
      cursor=conn.cursor()
      try:
        if (isphonevalid(request.form.get('staff_phone'))) and (isemailvalid(request.form.get('staff_email'))):
          cursor.execute('''INSERT INTO dotchainstaff ('ID','USERNAME','PASSWORD','EMAIL','PHONENUMBER','ADDRESS') VALUES 
        (?,?,?,?,?,?)''',(request.form.get('staff_id'),request.form.get('staff_username'),request.form.get('staff_pass'),request.form.get('staff_email'),request.form.get('staff_phone'),request.form.get('staff_address')))
          conn.commit()
          flash('added')   
        else :
            flash('wrong email or phone number format')
        
      except:
        conn.rollback()
        flash('add emp failed')
      conn.close()
      userdata=showdata()
      totalemp=len(userdata)
      return render_template('admindashboard.html',username=username,userdata=userdata,totalemp=totalemp)
    userdata=showdata()
    totalemp=len(userdata)
    conn = sqlite3.connect('flask.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dotchainblogtable')
    blogdata=cursor.fetchall()
    blogdatalen=len(blogdata)
    conn.close()
    return render_template('admindashboard.html',username=username,userdata=userdata,totalemp=totalemp,blogdata=blogdata,blogdatalen=blogdatalen)
  if('user' not in session):
    return render_template('adminlogin.html')
  else:
    return redirect(url_for('staffpanel',username=session['user']))
  
@app.route('/admin/search', methods=['GET','POST'])
def adminsearch():
  if ('user' in session and session['user'] == "jaishriram"):
    if request.method=='POST':
      query=request.form.get('search_emp')
      return redirect(url_for("searchemp",query=query))
  return redirect(url_for('staffdashboard'))

@app.route('/searchemp/<query>')
def searchemp(query):
  if ('user' in session and session['user'] == "jaishriram"):
    if query.lower()!="all":
      userdata=showsearchdataemp(query)
      totalemp=len(userdata)
      return render_template('admindashboard.html',username=session['user'],userdata=userdata,totalemp=totalemp)
  return redirect(url_for('staffdashboard'))

@app.route('/admin/search/blog', methods=['GET','POST'])
def adminsearchblog():
  if ('user' in session and session['user'] == "jaishriram"):
    if request.method=='POST':
      query=request.form.get('search_blog')
      return redirect(url_for("searchblog",query=query))
  return redirect(url_for('staffdashboard'))

@app.route('/searchblog/<query>')
def searchblog(query):
  if ('user' in session and session['user'] == "jaishriram"):
    if query.lower()!="all":
      conn = sqlite3.connect('flask.db')
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM dotchainblogtable WHERE BLOGID=? OR USERNAME=? OR CATEGORY=? OR OBJECTIVE=? or TITLE LIKE ?',(query,query,query.lower(),query.lower(),f"%{query}%"))
      blogdata=cursor.fetchall()
      blogdatalen=len(blogdata)
      conn.close()
      return render_template('admindashboard.html',username=session['user'],blogdata=blogdata,blogdatalen=blogdatalen)
  return redirect(url_for('staffdashboard'))

@app.route('/staff/search/blog', methods=['GET','POST'])
def staffsearchblog():
  if('user'in session and  session['user'] == "jaishriram"):
    return redirect(url_for('admin',username=session['user']))
  elif('user' in session):
    if request.method=='POST':
      query=request.form.get('search_blog_staff')
      return redirect(url_for("searchblogstaff",query=query))
  return render_template('adminlogin.html')

@app.route('/searchblog/staff/<query>')
def searchblogstaff(query):
  if('user'in session and  session['user'] == "jaishriram"):
    return redirect(url_for('admin',username=session['user']))
  elif('user' in session): 
    if query.lower()!="all":
      conn = sqlite3.connect('flask.db')
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM (SELECT * FROM dotchainblogtable WHERE USERNAME=?) WHERE BLOGID=? OR CATEGORY=? OR OBJECTIVE=? or TITLE LIKE ?',(session['user'],query,query.lower(),query.lower(),f"%{query}%"))
      blogdata=cursor.fetchall()
      blogdatalen=len(blogdata)
      conn.close()
      return render_template('allblogstaff.html',username=session['user'],blogdata=blogdata,blogdatalen=blogdatalen)
  return render_template('adminlogin.html')

@app.route("/staffdashboard", methods=['GET', 'POST'])
def staffdashboard():
  if ('user' in session and session['user'] == "jaishriram"):
    username="jaishriram"
    return redirect(url_for('admin',username=username))
  elif('user' in session):
    return redirect(url_for('staffpanel',username=session['user']))
    
  if request.method=='POST':
    username = request.form.get('staff_username')
    userpass = request.form.get('staff_pass')
    if (username == "jaishriram" and userpass == "jaishriram@4871"):
      #set the session variable
      session['user'] = username
      return redirect(url_for('admin',username=username))
    conn = sqlite3.connect('flask.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dotchainstaff WHERE USERNAME=? AND PASSWORD=?", (username, userpass))
    if cursor.fetchone() is not None:
      session['user']=username
      return redirect(url_for('staffpanel',username=username)) 
    conn.close()
  return render_template('adminlogin.html')

@app.route('/staffpanel/<username>',methods=['GET','POST'])
def staffpanel(username):
  if('user'in session and  session['user'] == "jaishriram"):
    return redirect(url_for('admin',username=session['user']))
  elif('user' in session):
    return render_template('staff.html',username=session['user'])
  return render_template('adminlogin.html')

@app.route('/staffpanel/<username>/add',methods=['GET','POST'])
def staffpanel_add(username):
  if('user'in session and  session['user'] == "jaishriram"):
    return redirect(url_for('admin',username=session['user']))
  elif('user' in session):
    if request.method=='POST':
      conn = sqlite3.connect('flask.db')
      cursor=conn.cursor()
      try:
        image = request.files['image']
        # Validate the uploaded image
        if not allowed_file(image.filename):
          flash('Invalid file format. Only JPG GIF files are allowed.')
          return redirect(url_for('allblogs_staff',username=session['user']))
        if image:
            filename = secure_filename(image.filename)
            filename,extension=os.path.splitext(filename)
            filename=f"{str(time.time()).replace('.','_')}{extension}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            cursor.execute('''INSERT INTO dotchainblogtable ('BLOGID','TITLE','KEYWORD','CONTENT','CATEGORY','DESCRIPTION','USERNAME','DATE','OBJECTIVE','IMAGE','CODE') VALUES (?,?,?,?,?,?,?,?,?,?,?)''',(request.form.get("article_id")+f"{str(time.time()).replace('.','_')}",request.form.get("title").lower(),request.form.get("keywords"),request.form.get("main_content"),request.form.get('category').lower(),request.form.get('description'),username,datetime.datetime.now().strftime("%-m/%-d/%y"),request.form.get('objective').lower(),filename,random.randint(1000,9999)))  
            conn.commit()
            flash('added and published')
      except:
        conn.rollback()
        flash('failed')
      conn.close()
      return redirect(url_for('allblogs_staff',username=session['user']))
    return render_template('addblog.html',username=session['user'])
  return render_template('adminlogin.html')

def allowed_file(filename):
  allowed_extensions = {'jpg', 'gif'}
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# to send the folder details of uploaded image
@app.route('/uploads/<filename>')
def serve_uploaded_image(filename):
    uploads_folder = os.path.join(app.root_path, 'uploads')
    return send_from_directory(uploads_folder, filename)

@app.route('/staffpanel/<username>/allblogs')
def allblogs_staff(username):
  if('user'in session and  session['user'] == "jaishriram"):
    return redirect(url_for('admin',username=session['user']))
  elif('user' in session):
    query=session['user']
    blogdata=searchblogdata(query)
    blogdatalen=len(blogdata)
    return render_template('allblogstaff.html',username=session['user'],blogdata=blogdata,blogdatalen=blogdatalen)
  return render_template('adminlogin.html')

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/staffdashboard')

@app.route("/deletestaff/<string:id>", methods = ['GET', 'POST'])
def deletestaff(id):
  if ('user' in session and session['user'] == "jaishriram"):
    conn = sqlite3.connect('flask.db')
    cursor = conn.cursor()
    try:
      cursor.execute('DELETE FROM dotchainstaff WHERE ID=(?)',(id,))
      conn.commit()
      flash(f"deleted id {id}")
    except:
      conn.rollback()
      flash(f'not deleted emp {id}')
    conn.close()
    return redirect(url_for('admin',username=session['user']))
  return redirect(url_for('staffdashboard'))

@app.route("/deleteblog/<string:id>", methods = ['GET', 'POST'])
def deleteblog(id):
  if ('user' in session and session['user'] == "jaishriram"):
    conn = sqlite3.connect('flask.db')
    cursor = conn.cursor()
    try:
      cursor.execute('DELETE FROM dotchainblogtable WHERE BLOGID=(?)',(id,))
      conn.commit()
      flash(f"deleteD BLOG id {id}")
    except:
      conn.rollback()
      flash(f'not deleted BLOG {id}')
    conn.close()
    return redirect(url_for('admin',username=session['user']))
  return redirect(url_for('staffdashboard'))

@app.route("/updatestaff/<string:id>",methods=['GET','POST'])
def adminupdate(id):
  if ('user' in session and session['user'] == "jaishriram"):
    conn = sqlite3.connect('flask.db')
    cursor = conn.cursor()
    try:
      if request.method=='POST':
        if (isphonevalid(request.form.get('staff_update_phone'))) and (isemailvalid(request.form.get('staff_update_email'))):
          cursor.execute('''UPDATE dotchainstaff SET ID=?,USERNAME=?,PASSWORD=?,EMAIL=?,PHONENUMBER=?,ADDRESS=? WHERE ID=?''',(request.form.get('staff_update_id'),request.form.get('staff_update_username'),request.form.get('staff_update_pass'),request.form.get('staff_update_email'),request.form.get('staff_update_phone'),request.form.get('staff_update_address'),id))
          conn.commit()
          flash(f'updated emp {id}')
        else:
          flash('wrong email or phone number format')
      else:
        flash('no data to update')
    except:
      conn.rollback()
      flash('not updated --failed')
    conn.close()
    return redirect(url_for('admin',username=session['user']))
  return redirect(url_for('staffdashboard'))

@app.route("/staffpanel/<username>/info")
def info(username):
  if('user' in session):
    return render_template("staffinfo.html",username=session['user'])
  return render_template("adminlogin.html")

@app.route("/staffpanel/<username>/setting",methods=['GET','POST'])
def setting(username):
  if('user'in session and  session['user'] == "jaishriram"):
    return redirect(url_for('admin',username=session['user']))
  elif('user' in session):
    if request.method=='POST':
      conn=sqlite3.connect('flask.db')
      cursor=conn.cursor()
      try:
        cursor.execute('UPDATE dotchainstaff SET PASSWORD=? WHERE USERNAME=? AND PASSWORD=?',(request.form.get("newpw"),username,request.form.get("oldpw")))
        conn.commit()
        flash("password changed")
      except:
        conn.rollback()
        flash("wrong password")
      conn.close()
      return redirect(url_for('allblogs_staff',username=session['user']))
    return render_template("staffsetting.html",username=session['user'])
  return render_template("adminlogin.html")
    
@app.route("/blogupdate/<username>/<string:blogid>",methods=['GET','POST'])
def blogupdate(blogid,username):
  if('user'in session and  session['user'] == "jaishriram"):
    conn = sqlite3.connect('flask.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dotchainblogtable WHERE BLOGID=(?)',(blogid,))
    blogdata=cursor.fetchone()
    categories = ['gaming', 'technology', 'gen-z','anime']  # Add more categories as needed in lower
    objectives = ['commercial', 'main', 'homescreen','other']  # Add more objectives as needed in lower
    try:
      if request.method=='POST':
        image=request.files['image']
        if image.filename!="":
          if not allowed_file(image.filename):
            flash('Invalid file format. Only JPG GIF files are allowed.')
            return redirect(url_for('admin',username=session['user']))
          if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            cursor.execute('''UPDATE dotchainblogtable SET TITLE=?,KEYWORD=?,CONTENT=?,CATEGORY=?,DESCRIPTION=?,DATE=?,OBJECTIVE=?,IMAGE=?,CODE=? WHERE BLOGID=?''',(request.form.get("title").lower(),request.form.get("keywords"),request.form.get("main_content"),request.form.get('category').lower(),request.form.get('description'),datetime.datetime.now().strftime("%-m/%-d/%y"),request.form.get('objective').lower(),filename,random.randint(1000,9999),blogid))  
            conn.commit()
            flash('updated and published with image')
            return redirect(url_for('admin',username=session['user']))
        else:
          cursor.execute('''UPDATE dotchainblogtable SET TITLE=?,KEYWORD=?,CONTENT=?,CATEGORY=?,DESCRIPTION=?,DATE=?,OBJECTIVE=?,CODE=? WHERE BLOGID=?''',(request.form.get("title").lower(),request.form.get("keywords"),request.form.get("main_content"),request.form.get('category').lower(),request.form.get('description'),datetime.datetime.now().strftime("%-m/%-d/%y"),request.form.get('objective').lower(),random.randint(1000,9999),blogid))
          conn.commit()
          flash('updated and published without image')
          return redirect(url_for('admin',username=session['user']))
    except:
      conn.rollback()
      flash('not updated --failed')
      return redirect(url_for('admin',username=session['user']))
    conn.close()
    return render_template('adminblogupdate.html',username=session['user'],blogdata=blogdata,categories=categories,objectives=objectives)
    
  elif ('user' in session):
    if username==session['user']:
      conn = sqlite3.connect('flask.db')
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM dotchainblogtable WHERE BLOGID=(?)',(blogid,))
      blogdata=cursor.fetchone()
      categories = ['gaming', 'technology', 'gen-z','anime']  # Add more categories as needed in lower
      objectives = ['commercial', 'main', 'homescreen','other']  # Add more objectives as needed in lower
      try:
        if request.method=='POST':
          if request.form.get('code')==str(blogdata[10]):
            image=request.files['image']
            if image.filename!="":
              if not allowed_file(image.filename):
                flash('Invalid file format. Only JPG GIF files are allowed.')
                return redirect(url_for('allblogs_staff',username=session['user']))
              if image:
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                cursor.execute('''UPDATE dotchainblogtable SET TITLE=?,KEYWORD=?,CONTENT=?,CATEGORY=?,DESCRIPTION=?,DATE=?,OBJECTIVE=?,IMAGE=?,CODE=? WHERE BLOGID=?''',(request.form.get("title").lower(),request.form.get("keywords"),request.form.get("main_content"),request.form.get('category').lower(),request.form.get('description'),datetime.datetime.now().strftime("%-m/%-d/%y"),request.form.get('objective').lower(),filename,random.randint(1000,9999),blogid))  
                conn.commit()
                flash('updated and published with image')
                return redirect(url_for('allblogs_staff',username=session['user']))
            else:
              cursor.execute('''UPDATE dotchainblogtable SET TITLE=?,KEYWORD=?,CONTENT=?,CATEGORY=?,DESCRIPTION=?,DATE=?,OBJECTIVE=?,CODE=? WHERE BLOGID=?''',(request.form.get("title").lower(),request.form.get("keywords"),request.form.get("main_content"),request.form.get('category').lower(),request.form.get('description'),datetime.datetime.now().strftime("%-m/%-d/%y"),request.form.get('objective').lower(),random.randint(1000,9999),blogid))
              conn.commit()
              flash('updated and published without image')
              return redirect(url_for('allblogs_staff',username=session['user']))
          else:
            flash("type correct update code")
            query=session['user']
            blogdata=searchblogdata(query)
            blogdatalen=len(blogdata)
            return render_template('allblogstaff.html',username=session['user'],blogdata=blogdata,blogdatalen=blogdatalen)
      except:
        conn.rollback()
        flash('not updated --failed')
      conn.close()
      return render_template('blogupdate.html',username=session['user'],blogdata=blogdata,categories=categories,objectives=objectives)
    else:
      flash("don't you try to update others work WARNING-------")
  return redirect(url_for('staffdashboard'))

@app.route('/article/<string:blogid>',methods=['GET','POST'])
def article(blogid):
  if request.method=="POST":
      dotchainsearch=request.form.get('dotchainsearch')
      return redirect(url_for('dotchainsearch',dotchainsearch=dotchainsearch,pageno=1))
  conn=sqlite3.connect('flask.db')
  cursor=conn.cursor()
  cursor.execute('SELECT * FROM dotchainblogtable WHERE BLOGID=(?)',(blogid,))
  blogdata=cursor.fetchone()
  cursor.execute('SELECT BLOGID,TITLE,CATEGORY,IMAGE,DATE FROM dotchainblogtable WHERE CATEGORY=(?) ORDER BY DATE DESC LIMIT (?),(?)',(blogdata[4],random.randint(1,5),6))
  rec_blogdata=cursor.fetchall()
  conn.close()
  return render_template('article.html',blogdata=blogdata,rec_blogdata=rec_blogdata)

@app.route('/terms_and_conditions')
def terms_and_conditions():
  index_news=news_slider("tech")
  return render_template('terms.html',index_news=index_news)

@app.route('/policy')
def policy():
  index_news=news_slider("tech")
  return render_template('policy.html',index_news=index_news)

def layout2blog(query):
  conn = sqlite3.connect('flask.db')
  cursor = conn.cursor()
  cursor.execute('SELECT BLOGID,TITLE,CATEGORY,DATE,IMAGE FROM dotchainblogtable WHERE CATEGORY=(?) ORDER BY DATE DESC LIMIT (?)',(query.lower(),11))
  blog=cursor.fetchall()
  conn.close
  return blog
  
@app.route('/anime')
def anime():
  index_news=news_slider("anime")
  newsl=news()
  blog=layout2blog('anime')
  return render_template('layout2.html',index_news=index_news,heading="Anime",newsl=newsl,headimage=['img/anime1.jpg','img/anime2.jpg'],blog=blog)
  
@app.route('/gaming')
def gaming():
  index_news=news_slider("gaming")
  newsl=news()
  blog=layout2blog('gaming')
  return render_template('layout2.html',index_news=index_news,heading="Gaming",newsl=newsl,headimage=['img/gaming1.jpg','img/gaming2.jpg'],blog=blog)

@app.route('/genz')
def genz():
  index_news=news_slider("Gen-z")
  newsl=news()
  blog=layout2blog('gen-z')
  return render_template('layout2.html',index_news=index_news,heading="Genz",newsl=newsl,headimage=['img/genz1.jpg','img/genz2.jpg'],blog=blog)

@app.route('/tech')
def tech():
  index_news=news_slider("technology")
  newsl=news()
  blog=layout2blog('technology')
  return render_template('layout2.html',index_news=index_news,heading="Tech",newsl=newsl,headimage=['img/tech1.jpg','img/tech2.jpg'],blog=blog)

app.run(host='0.0.0.0', port=81,debug=False)
