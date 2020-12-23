import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'D:\\Загрузка и выгрузка файлов\\answers'
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg', 'py'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
messange = ""



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global messange
    if request.method == 'POST':
        file = request.files['file']
        name = request.form.get("name")
        surname = request.form.get("surname")
        classroom = request.form.get("classroom")
        task = request.form.get("task")
        if classroom not in os.listdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER + "\\" + classroom)
        if str(surname + " " + name) not in os.listdir(UPLOAD_FOLDER + "\\" + classroom):
            os.mkdir(UPLOAD_FOLDER + "\\" + classroom + "\\" + surname + " " + name)
        if file:
            if allowed_file(file.filename):
                extension = file.filename.split(".")[-1]
                filename = surname + " " + name + " " + classroom + " " + "задание " + str(task) + "." + extension
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "\\" + classroom + "\\" + surname + " " + name, filename))
                messange = "Файл загружен"
                return redirect("/")
            else:
                messange = "Не разрешённый формат файла"
        else:
            messange = "Файл не выбран"
    return render_template("main.html", messange=messange)


@app.route('/viewfiles/')
def viewfiles():
    folders = []
    for dir in os.listdir(UPLOAD_FOLDER):
        folders.append(dir)
    return render_template("viewfolders.html", folders=folders)


@app.route('/viewfiles/<classroom>/')
def viewpeoples(classroom):
    folders = []
    for dir in os.listdir(UPLOAD_FOLDER + "\\" + classroom):
        folders.append(dir)
    return render_template("view_class_crew.html", classroom=classroom, folders=folders)


@app.route("/viewfiles/<classroom>/<who>/")
def viewpeople(classroom, who):
    files = []
    for file in os.listdir(UPLOAD_FOLDER + "\\" + classroom + "\\" + who):
        files.append(file)
    return render_template("viewpeople.html", who=who, files=files, classroom=classroom)


@app.route("/viewfiles/<classroom>/<who>/<file>")
def viewfile(classroom, who, file):
    f = open(UPLOAD_FOLDER + "\\" + classroom + "\\" + who + "\\" + file, "r")
    text = f.read()
    f.close()
    return render_template("viewfile.html", classroom=classroom, who=who, file=file, text=text)


@app.route("/delete/<classroom>/<who>/<file>", methods=["POST", "GET"])
def delete_file(classroom, who, file):
    os.remove(UPLOAD_FOLDER + "\\" + classroom + "\\" + who + "\\" + file)
    return redirect("/viewfiles/{}".format(classroom))


app.run(debug=True)