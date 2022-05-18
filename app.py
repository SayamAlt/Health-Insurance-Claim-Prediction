#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, request
import joblib


# In[2]:


model = joblib.load('model.pkl')
model


# In[3]:


app = Flask(__name__)


# In[4]:


city_names = ['NewYork', 'Boston', 'Phildelphia', 'Pittsburg', 'Buffalo',
       'AtlanticCity', 'Portland', 'Cambridge', 'Hartford', 'Springfield',
       'Syracuse', 'Baltimore', 'York', 'Trenton', 'Warwick',
       'WashingtonDC', 'Providence', 'Harrisburg', 'Newport', 'Stamford',
       'Worcester', 'Atlanta', 'Brimingham', 'Charleston', 'Charlotte',
       'Louisville', 'Memphis', 'Nashville', 'NewOrleans', 'Raleigh',
       'Houston', 'Georgia', 'Oklahoma', 'Orlando', 'Macon', 'Huntsville',
       'Knoxville', 'Florence', 'Miami', 'Tampa', 'PanamaCity',
       'Kingsport', 'Marshall', 'Mandan', 'Waterloo', 'IowaCity',
       'Columbia', 'Indianapolis', 'Cincinnati', 'Bloomington', 'Salina',
       'KanasCity', 'Brookings', 'Minot', 'Chicago', 'Lincoln',
       'FallsCity', 'GrandForks', 'Fargo', 'Cleveland', 'Canton',
       'Columbus', 'Rochester', 'Minneapolis', 'JeffersonCity',
       'Escabana', 'Youngstown', 'SantaRosa', 'Eureka', 'SanFrancisco',
       'SanJose', 'LosAngeles', 'Oxnard', 'SanDeigo', 'Oceanside',
       'Carlsbad', 'Montrose', 'Prescott', 'Fresno', 'Reno', 'LasVegas',
       'Tucson', 'SanLuis', 'Denver', 'Kingman', 'Bakersfield',
       'Mexicali', 'SilverCity', 'Pheonix', 'SantaFe', 'Lovelock']
cities = dict(zip(city_names,[55,  5, 63, 64,  8,  1, 65,  9, 29, 79, 81,  3, 89, 83, 85, 86, 67,
       28, 56, 80, 88,  0,  6, 12, 13, 42, 47, 53, 54, 68, 30, 26, 58, 59,
       44, 31, 38, 24, 49, 82, 61, 37, 46, 45, 87, 33, 17, 32, 15,  4, 71,
       35,  7, 51, 14, 40, 22, 27, 23, 16, 10, 18, 70, 50, 34, 20, 90, 77,
       21, 73, 74, 41, 60, 72, 57, 11, 52, 66, 25, 69, 39, 84, 75, 19, 36,
        2, 48, 78, 62, 76, 43]))
job_names = ['Actor', 'Engineer', 'Academician', 'Chef', 'HomeMakers', 'Dancer',
       'Singer', 'DataScientist', 'Police', 'Student', 'Doctor',
       'Manager', 'Photographer', 'Beautician', 'CA', 'Blogger', 'CEO',
       'Labourer', 'Accountant', 'FilmDirector', 'Technician',
       'FashionDesigner', 'Architect', 'HouseKeeper', 'FilmMaker',
       'Buisnessman', 'Politician', 'DefencePersonnels', 'Analyst',
       'Clerks', 'ITProfessional', 'Farmer', 'Journalist', 'Lawyer',
       'GovEmployee']
job_titles = dict(zip(job_names,[ 2, 16,  0, 10, 22, 12, 32, 13, 30, 33, 15, 28, 29,  5,  8,  6,  9,
       26,  1, 19, 34, 18,  4, 23, 20,  7, 31, 14,  3, 11, 24, 17, 25, 27,
       21]))
disease_names = ['NoDisease', 'Epilepsy', 'EyeDisease', 'Alzheimer', 'Arthritis',
       'HeartDisease', 'Diabetes', 'Cancer', 'High BP', 'Obesity']
diseases = dict(zip(disease_names,[8, 4, 5, 0, 1, 6, 3, 2, 7, 9]))


# In[5]:


@app.route("/")
def home():
    return render_template('home.html',cities=city_names,jobs=job_names,hereditary_diseases=disease_names)


# In[6]:


@app.route("/predict", methods = ['GET','POST'])
def predict():
    if request.method == 'POST':
        age = request.form['age'] #age range: (18,64)
        sex_select = request.form['sex'] #male: 1 female: 0
        sex = 0
        if sex_select == 'MALE':
            sex = 1
        elif sex_select == 'FEMALE':
            sex = 0
        weight = request.form['weight'] #weight range: (34.0,95.0) (float)
        bmi = request.form['bmi'] #bmi range: (16.0,53.1) (float)
        dis_selected = request.form['disease'] 
        hereditary_disease = diseases[dis_selected]
        no_of_dependents = request.form['no_dependents'] # nod range: (0,5)
        smoke_select = request.form['smoke']
        smoker = 0
        if smoke_select == 'YES':
            smoker = 1
        elif smoke_select == 'NO':
            smoker = 0
        city_select = request.form['city']
        city = cities[city_select]
        bp = request.form['blood_pressure'] # BP range: (0,122) Integer
        diab_select = request.form['diabetes']
        diabetes = 0
        if diab_select == 'YES':
            diabetes = 1
        elif diab_select == 'NO':
            diabetes = 0
        reg_ex_select = request.form['regular_exercise']
        regular_exercise = 0
        if reg_ex_select == 'YES':
            regular_exercise = 1
        elif reg_ex_select == 'NO':
            regular_exercise = 0
        job_title_selected = request.form['job_title']
        job_title = job_titles[job_title_selected]
        
        predictions = model.predict([[
            age,
            sex,
            weight,
            bmi,
            hereditary_disease,
            no_of_dependents,
            smoker,
            city,
            bp,
            diabetes,
            regular_exercise,
            job_title
        ]])
        
        output = predictions[0]
        output = output * 12147.834670761482
        output = "%.3f" % output
        output = float(output)
        output = format(output, ',')
        return render_template('home.html',cities=city_names,jobs=job_names,hereditary_diseases=disease_names,prediction_text="Your estimated health insurance claim is ${}.".format(output))


# In[ ]:


if __name__ == '__main__':
    app.run(port=8080)

