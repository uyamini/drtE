from flask import Flask, render_template
from src import CLEAN_XL, CLEAN_XL_PATH, DATA_PATH, data_file_path, allowed_file, ROOT_PATH, config_file_path, CLEAN_PATH, CLEAN_NAME, PIE_PATH
import os
from flask import flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
from .integration import get_preds
import webbrowser
from threading import Timer, Thread
from src import Driver
from time import sleep
from PIL import Image
import base64
import io

UPLOAD_FOLDER = DATA_PATH

app = Flask('main ui',
            template_folder = ROOT_PATH + '/templates',
            static_folder = ROOT_PATH + '/static')
driver = None

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['SECRET_KEY'] = '0000'

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods =['GET', 'POST'] )
def upload_file():
    for pth in [CLEAN_PATH, CLEAN_XL_PATH, PIE_PATH]:
        if os.path.exists(pth): os.remove(pth)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # t = Thread(target = start_processing)
            # t.start()
            # while driver is None or driver.progress < 150:
            #     sleep(1)
            #     # update progress
            # t.join()
            start_processing()
            return redirect(url_for('download_page')) 
    return render_template('home.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        configs = request.form.getlist('source')
        with open(config_file_path(), 'w') as config:
            config.write('\n'.join(configs))
        return redirect(url_for('upload_file'))
    return render_template('config.html')

@app.route('/download', methods=['GET', 'POST'])
def download_page():
    if request.method == 'POST':
        if request.form['submit_button'] == "Download as CSV" :
            return redirect(url_for('download_file', name=CLEAN_NAME))
        else:
            return redirect(url_for('download_file', name=CLEAN_XL))
    else:
        return render_template('download.html')
    
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name, as_attachment=True)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/summary")
def summary():
    f_path = PIE_PATH
    if (os.path.exists(f_path)):
        im = Image.open(f_path)
        data = io.BytesIO()
        im.save(data,"PNG")
        encoded_img_data = base64.b64encode(data.getvalue())
        global driver
        sizes, labels, dupes, missing = driver.summary_stats()
        table  = [[0 for i in range(2)] for j in range(len(labels))]
        for x in range(len(labels)):
            table[x][0] = labels[x]
            table[x][1] = sizes[x]
        dirty = driver.dirty_inds.shape[0]
        total = driver.clean_mat.shape[0] * driver.clean_mat.shape[1]
        return render_template('summary.html', img_data=encoded_img_data.decode('utf-8'), 
                                table=table, dirty = dirty, total = total, dupes = dupes, missing = missing)
    else:
        return render_template('summary.html')

def start_processing():
    """Starts the backend code to process the data after it is saved by Flask."""
    global driver
    pth = data_file_path()
    if pth == '':
        flash('No selected file')
        return redirect(request.url)
    print(f'Reading {pth}')
    preds, dupes = get_preds()
    driver = Driver(pth, preds = preds, dupes = dupes)
    os.remove(pth)
    print(f'Finding dirty cells in sheet with shape {driver.clean_mat.shape}')
    driver.find_dirty_cells()
    print(f'Cleaning {driver.dirty_inds.shape[0]} cells')
    driver.clean_all_cells()
    driver.save_clean(CLEAN_PATH)
    driver.save_excel(CLEAN_XL_PATH)
    driver.highlight_excel(CLEAN_XL_PATH)
    driver.save_pie_chart(PIE_PATH)
    print('Processing complete.')

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

def launch_server():
    """Launches the server UI."""
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False, port = 5000, threaded=True)
