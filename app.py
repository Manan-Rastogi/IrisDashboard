from flask import Flask, render_template, request, redirect, session, Response, jsonify
import os
from plots import *

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'username' and password == 'password':
            session['logged_in'] = True
            return redirect('/index')
        return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect('/login')
    if request.method == 'POST':
        species = request.form['species']
        feature = request.form['feature']
        # Generate histogram and line chart (to be implemented)
    return render_template('index.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

@app.route('/get_histogram', methods=['GET'])
def get_histogram():
    species = request.args.get('species')
    feature = request.args.get('feature')
    histogram_data = generate_histogram()  # Function from plots.py
    return jsonify({"histogramData": histogram_data})

@app.route('/get_line_chart', methods=['GET'])
def get_line_chart():
    species = request.args.get('species')
    feature = request.args.get('feature')
    line_chart_data = generate_line_chart(species, feature)  # Function from plots.py
    return jsonify({"lineChartData": line_chart_data})


@app.route('/download_csv', methods=['GET'])
def download_csv():
    species = request.args.get('species')
    feature = request.args.get('feature')
    bin_start = float(request.args.get('bin_start'))
    bin_end = float(request.args.get('bin_end'))
    
    csv_data = generate_csv_data(species, feature, bin_start, bin_end)
    
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={species}_{feature}_{bin_start}_{bin_end}.csv"}
    )



if __name__ == '__main__':
    app.run(debug=True)
