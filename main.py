import os
from flask import Flask, request, redirect, render_template


UPLOAD_FOLDER = 'D:\\Загрузка и выгрузка файлов\\answers'
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg', 'py'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        name = request.form.get("name")
        surname = request.form.get("surname")
        classroom = request.form.get("class-num") + request.form.get("class-letter")
        if classroom not in os.listdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER + "\\" + classroom)
        if str(surname + " " + name) not in os.listdir(UPLOAD_FOLDER + "\\" + classroom):
            os.mkdir(UPLOAD_FOLDER + "\\" + classroom + "\\" + surname + " " + name)
        for i in range(1, int(request.form.get("quality")) + 1):
            number = "file" + str(i)
            file = request.files[number]
            if file:
                if allowed_file(file.filename):
                    extension = file.filename.split(".")[-1]
                    filename = surname + " " + name + " " + classroom + " " + "задание " + str(i) + "." + extension
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "\\" + classroom + "\\" + surname + " " + name, filename))
    return render_template("main.html")


app.run(debug=True)
