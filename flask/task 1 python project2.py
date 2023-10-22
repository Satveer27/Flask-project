# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 00:54:04 2022

@author: dabis
"""
#Importing all the modules to access the features
from time import strftime
from flask import Flask, render_template, url_for, redirect, flash,request
from wtforms import Form, StringField, TextAreaField, validators, SubmitField, BooleanField,RadioField, EmailField
from wtforms.validators import InputRequired, Length, DataRequired, Email
from wtforms.widgets import TextArea



app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'JDaodfhiuowefndsfnsfnsdnfsidofnsdUHIfdhsdf' #Secret key for safety purposes

#first part of flask
class The_first_form(Form):#This part gets the name, email and GIC number given by the user. It validates each entrybox to see weather any data has been submitted. If none has an error will pop up.
    name = StringField('Name:', validators=[validators.DataRequired()])#This is all possible by the work of Forms
    GIC = StringField('GIC', validators=[validators.DataRequired(),Length(min=7, max=7, message="At least 7 characters")])#This part checks if the P number length is correct, and provides a error if the P number is wrong in terms of length
    email = EmailField('email:', validators=[validators.DataRequired(),Email(message="Please enter a valid email addresss")])#This parrt validates if the email is correctly written using validation specifically for email
def current_time():#This part gets the time when the user submits the data.
    time_get = strftime("%Y-%m-%dT%H:%M")
    return time_get
def write_to_file(name, GIC, email):#This  part writes to file the name, time, GIC number and email in a certain format.
    store_data = open('GIC_details.txt', 'a')#This part opens the file to write
    time_store = current_time()
    store_data.write('DateStamp={}, Name={}, GIC number={}, Email={} \n'.format(time_store, name, GIC, email))#format is over here
    store_data.close()#This part closes the file



#second part of flask
class Second_form(Form):#This part validates that the user has ticked the checkbox, if the user doesnt a error will pop up. This is done by boolean validators.
    accept = BooleanField('accept', validators=[validators.DataRequired()])



#third part of flask
class Third_form(Form):#Radio fields are added here to have multiple choice questions. In total there are 4 questions with the choices of yes or no. As well as each yes data is connected to a yes data that will be written to the file.
    question =  RadioField('Label',validators=[InputRequired()],choices=[("yes", 'yes'), ("no", 'no')], validate_choice=True)#Each choice will have to validate true, the following four lines of code was taken from https://stackoverflow.com/questions/53101631/wtforms-radiofield-preventing-form-validation
    question1 =  RadioField('Label',validators=[InputRequired()],choices=[("yes", 'yes'), ("no", 'no')], validate_choice=True)
    question2 =  RadioField('Label',validators=[InputRequired()],choices=[("yes", 'yes'), ("no", 'no')], validate_choice=True)
    question3 =  RadioField('Label',validators=[InputRequired()],choices=[("yes", 'yes'), ("no", 'no')], validate_choice=True)
def  write_to_file1(question, question1, question2, question3):#This part takes the answer from the radiofields(4 answers) and stores them in a file, formatted way just like the file above.
    store_data1 = open('ans1.txt', 'a')#This part opens the file
    store_data1.write('question={}, Q1={}, Q2={}, Q3={} \n'.format(question, question1, question2, question3))#This is the format
    store_data1.close()#This part closes the file


#final part of flask
class Fourth_form(Form):#This area of the flask uses Textareafield. such a field enables us to write alot of words in a box. The box can be configurated by rows and columns. The maximum character and minimum will be set. If the user doesnt meet the max and min values, there will be a error.
    question4 = TextAreaField('question4', validators=[DataRequired(), Length(min=15, max=250, message="At least 15 characters, maximum 250")], render_kw={"rows": 10, "cols": 80}) #The following 2 lines of code was taken from https://stackoverflow.com/questions/7979548/how-to-render-my-textarea-with-wtforms
    question5 = TextAreaField('question5', validators=[DataRequired(), Length(min=15, max=250, message="At least 15 characters, maximum 250")], render_kw={"rows": 10, "cols": 80})
def  write_to_disk2(question4, question5):#The answers again are stored in another file. Seperately just like above.
    store_data1 = open('ans2.txt', 'a')
    store_data1.write('Q4={}, Q5={} \n'.format(question4, question5))
    store_data1.close()

    

    

@app.route('/home', methods =['GET','POST']) #Set the route of the app and the method to access it is POST, this is to be safer.
def start1():
    form = The_first_form(request.form) #the form here is assigned to the first form to help request form in shorter way
    
    if request.method == 'POST': #if method is post then we would request a form for name, email and Gic in html.
        name = request.form['name']
        GIC = request.form['GIC']
        email = request.form['email']
        
        if form.validate(): #If the form validates using the validators we will write the information in the file and go to a different url
           write_to_file(name, GIC, email)
           return redirect(url_for('check'))

           
        else: #if the form doesnt validate there will be a error popping up
            flash('Error: please enter a valid email adress')

    return render_template('index.html', form=form) #render template will take the html form from the template folder and use it for website building.





@app.route('/check', methods =['GET','POST']) #Set the route of the app and the method to access it is POST, this is to be safer.
def check():
       form = Second_form(request.form)
       
       if request.method == 'POST':#if method is post then we would instantly go to the validation process. We dont need to store data for accepting terms and conditions.
           if form.validate():#This would validate if the box has been ticked, if it has we would go to url question1
              return redirect(url_for('questions1'))

              
           else: #or else a error will pop up
               flash('Error: please tick the box')
               
       return render_template('index1.html', form=form)#This is another html form in the same template





@app.route('/questions1', methods =['GET','POST']) #Set the route of the app and the method to access it is POST, this is to be safer.
def questions1():
    form = Third_form()    
    if request.method == 'POST': #if method is post then we would request a form for the 4 questions assigned here.
        question = request.form['question']
        question1 = request.form['question1']
        question2 = request.form['question2']
        question3 = request.form['question3']
        
        if form.validate(): #same thing as above, if one of the radiofields isnt ticked then an error will be flashed
          flash('Error: A box must be ticked')

           
        else: #or else the answers will be stored and the user will move forward to the next file
           write_to_file1(question, question1, question2, question3)
           return redirect(url_for('questions2'))
           
            
    return render_template('index2.html', form=form) #This is a different html file in the same folder template





@app.route('/questions2', methods =['GET','POST'])  #Set the route of the app and the method to access it is POST, this is to be safer.
def questions2():
    form = Fourth_form()
     
    if request.method == 'POST':#if method is post then we would request a form for the 2 questions assigned here.
        question4 = request.form['question4']
        question5 = request.form['question5']
        
        if form.validate(): # if the textfield has input but doesnt meet the validation requirement a error will be supplied
            flash('Error: a input must be filled')
            

           
        else:#or else answer will be stored and the user will go to the final page
            write_to_disk2(question4, question5)
            return redirect(url_for('end'))
            
    return render_template('index3.html', form=form)#its a different html form but in the same template
    
   

@app.route('/end', methods =['GET','POST'])  #Set the route of the app and the method to access it is POST, this is to be safer.
def end():#This is the final route where its a thank you page.
    return render_template('index4.html')#its a different html form but the same template







if __name__ == '__main__':
    app.run() #This is for the flask to run.