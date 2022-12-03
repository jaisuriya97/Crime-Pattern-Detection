import re
import json
from flask import Flask,render_template,request,Response,flash,jsonify,make_response, url_for,redirect
import pymongo
from bson.objectid import ObjectId
app=Flask(__name__)
app.secret_key="iuwbdcishdb"
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017
    )
    db = mongo.company
    mongo.server_info()
except:
    print("************ Error Cant connnect *************** ")



@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=="POST":
        name = request.form['Name']
        passw = request.form['password']
        data = list(db.Users.find())
        for user in data:
            user["name"]=str(user["name"])
            user["password"]=str(user["password"])
            if user["name"]==name and user["password"]==passw:
                return redirect(url_for("dashboard"))
            else:
                flash(" Login Incorrecct")    
             
    return render_template("login.html") 
        
@app.route('/')
def Home():
    return render_template("Home.html")
@app.route('/Signup',methods=["POST","GET"])    
def Signup():
    if request.method == "POST":
        try:
            name = request.form['Name']
            passw = request.form['password']
            cpass = request.form['cpassword']
            
            if passw == cpass:
                user = {
                "name" : f"{request.form['Name']}",
                "password":f"{request.form['password']}",
                "cpass":f"{request.form['cpassword']}",
                "email":f"{request.form['email']}"
                }
                dbresponse = db.Users.insert_one(user)
                return redirect(url_for("dashboard"))
            else:
                flash("Confirm password not match!")    
        except Exception as ex:
            print("*************",ex,"****************")

    return render_template("Signup.html")    

@app.route('/Dashboard',methods=["POST","GET"])
def dashboard():
    if request.method=="POST":
        current_form = request.form['form-method']
        if current_form == "Insert":
            name = request.form['Name']
            Country = request.form['Country']
            Years_active = request.form['Years active']
            Notes = request.form['Notes']
            update(name,Country,Years_active,Notes)
        elif current_form == "Delete":
            name = request.form['Name']
            Country = request.form['Country']
            Years_active = request.form['Years active']
            Notes = request.form['Notes']
            dela(name)

    return render_template("dashboard.html")    
def update(name,country,year_active,notes):
    name = name
    data = list(db.Data.find())
    for user in data:
        if name in user["Name"]:
            flash("Already data exist!")
            break
        if name not in user["Name"]:     
            user = {
                    "Name" :name,
                    "Country":country,
                    "Years active":year_active,
                    "Notes":notes
                    }
            dbresponse = db.Data.insert_one(user)
            flash("inserted successfully")
            break  
def dela(name):
    data = list(db.Data.find())
    for user in data:
        if name in user["Name"]:
            flash("Already data exist!")
            break
        if name not in user["Name"]:     
            sample = db.Data.delete_one( { "Name": name } )
            flash("Deleted successfully")
            break  
@app.route('/Finding',methods=["POST","GET"])
def find():
    if request.method=="POST":
        string = request.form['Name']
        split= string.split()
        women = {}
        young_women={}
        elder_women={}
        men={}
        young_men={}
        elder_men={}
        child={}
        data = list(db.Data.find())
        for user in data:
            sample = user["Notes"]
            saplme_x= sample.split()
            for i in saplme_x:
                if i.lower() == "girl" or i.lower() == "women" or i.lower() == "ladies" or i.lower() == "female" or i.lower() == "females" or i.lower() == "girls" or i.lower() == "womens":
                    women.update({user["Name"]:user["Notes"]})
                    women_y_list = list(women.values())
                    for i in women_y_list:
                        i = i.split()
                        for i in i:
                            if i.lower() == "young":
                                young_women.update({user["Name"]:user["Notes"]}) 
                            if i.lower() == "":
                                elder_women.update({user["Name"]:user["Notes"]})
                if i.lower() == "men" or i.lower() == "boy" or i.lower() == "boys":
                    men.update({user["Name"]:user["Notes"]})
                    men_y_list = list(men.values())
                    for i in men_y_list:
                        i = i.split()
                        for i in i:
                            if i.lower() == "young":
                                young_men.update({user["Name"]:user["Notes"]}) 
                            if i.lower() == "":
                                elder_men.update({user["Name"]:user["Notes"]})
                if i.lower() == "children":
                    child.update({user["Name"]:user["Notes"]}) 
            else:
                if string.lower() in user["Notes"]:
                    flash("Name : "+user["Name"]) 
                    flash("Country : "+user["Country"])                                                                             
                    flash("Notes : "+user["Notes"])
        for i in split:
            if i.lower() == "women" or i.lower() == "girl" or i.lower() == "ladies" or i.lower()=="female":
                sample_key_list=list(women.keys())
                sample_value_list=list(women.values())
                for i in range(0,len(sample_key_list)):
                    flash("name :"+sample_key_list[i])
                    flash("Notes :"+sample_value_list[i])
                    flash("****")
            elif i.lower() == "men" or i.lower() =="gay" or i.lower() =="boy":
                sample_key_list=list(men.keys())
                sample_value_list=list(men.values())
                for i in range(0,len(sample_key_list)):
                    flash("name :"+sample_key_list[i])
                    flash("Notes :"+sample_value_list[i])
                    flash("****")
            elif i.lower() == "child" or i.lower() =="children":
                sample_key_list=list(child.keys())
                sample_value_list=list(child.values())
                for i in range(0,len(sample_key_list)):
                    flash("name :"+sample_key_list[i])
                    flash("Notes :"+sample_value_list[i])
                    flash("****")                                                     
            elif i.lower() == "young":
                sample_key_list=list(young_women.keys())
                sample_value_list=list(young_women.values())
                for i in range(0,len(sample_key_list)):
                    flash("name :"+sample_key_list[i])
                    flash("Notes :"+sample_value_list[i])
                    flash("****")
        

           


                                     
    return render_template("find.html")
@app.route('/search',methods=["POST","GET"])
def search():
    if request.method=="POST":
        crime = request.form['crime']
        location = request.form['location']
        if crime == "1":
            data = list(db.RapeData.find())
            for i in range(0,1051):
                sample  = list(data[i].values())
                sample.pop(0)
                for i in sample:
                    if  i==location:
                        flash("****")
                        for j in range(0,1051): 
                                    
                                    if  i == location:
                                        if j==0:
                                            flash("Location:"+str(sample[0]))
                                        if j==1:
                                            flash("Year:"+str(sample[1]))
                                        if j==2:
                                            flash("Subgroup:"+str(sample[2]))
                                        if j==3:
                                            flash("Rape Cases Reported:"+str(sample[3]))
                                        if j==4:
                                            flash("Victims Above 50 Yrs:"+str(sample[4]))
                                        if j==5:
                                            flash("Victims Between 10-14 Yrs:"+str(sample[5]))
                                        if j==6:
                                            flash("Victims Between 14-18 Yrs:"+str(sample[6]))
                                        if j==7:
                                            flash("Victims Between 18-30 Yrs:"+str(sample[7]))
                                        if j==8:
                                            flash("Victims Between 30-50 Yrs:"+str(sample[8]))
                                        if j==9:
                                            flash("Victims of Rape Total:"+str(sample[9]))
                                        if j==10:
                                            flash("Victims Upto 10 Yrs:"+str(sample[10]))                 
             
    return render_template("search.html") 
if __name__=="__main__":
    app.run(debug=True)