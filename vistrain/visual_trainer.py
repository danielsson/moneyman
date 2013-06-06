
from flask import *
from flask.ext.login import login_required
from database import *

import csv


visual_trainer = Blueprint('visual_trainer', __name__, template_folder="templates")


@visual_trainer.route('/', methods=['POST', 'GET'])
@login_required
def vis_index():
    if request.method == 'POST':
        file_ = request.files['file']
        if file_:
            try:
                dialect = csv.Sniffer().sniff(file_.read(1024))
                file_.seek(0)

                reader = csv.reader(file_, dialect)
                reader.next() #Skip header

                return render_template("classify.html", reader=reader)

            finally:
                file_.close()

        else:
            flash("File not found")


    return render_template("train.html")

@visual_trainer.route("/p")
def prew():
    return render_template("classify.html")