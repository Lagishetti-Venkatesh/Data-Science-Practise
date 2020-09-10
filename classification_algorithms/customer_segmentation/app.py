import numpy as np
from flask_mysqldb import MySQL
from flask import Flask, request, jsonify, render_template
import pickle
import yaml

app = Flask(__name__)
model = pickle.load(open('model_kmeans.pkl', 'rb'))

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    print(int_features)
    if int_features[-1] == 'female':
        int_features[-1] = 0
    elif int_features[-1] =='male':
        int_features[-1] = 1
    else:
        int_features[-1] = 2
    int_features = [int(x) for x in int_features]

    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0]+1)
    classes = [1, 2, 3, 4, 5]
    #Annual income is in multiple of 1000$.
    int_features[2] *=1000;

    if output in classes:
        #storing the Data in the Database.
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Data(gender, age, annual_income, spending_score) "\

        "VALUES(%s, %s, %s, %s)", (int_features[0], int_features[1], int_features[2], int_features[3]))
        mysql.connection.commit()
        cur.close()
        print(int_features)
        if output == 1:
            text = 'Class {}: customer will have low annual income as well as low yearly spend of income.'.format(output)
            return render_template('index.html', prediction_text = text)

        elif output == 2:
            text = 'Class {}: customer will have high annual income and low yearly spend.'.format(output)
            return render_template('index.html', prediction_text = text)

        elif output == 3:
            text = 'Class {}: customer will have the medium income salary as well as the medium annual spend of salary.'.format(output)
            return render_template('index.html', prediction_text = text)

        elif output == 4:
            text = 'Class {}: customer will have a high annual income as well as a high annual spend.'.format(output)
            return render_template('index.html', prediction_text = text)

        elif output == 5:
            text = 'Class {}: customer will have a low annual income but its high yearly expenditure.'.format(output)
            return render_template('index.html', prediction_text = text)

    else:
          return render_template('index.html', prediction_text = 'Class: {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
