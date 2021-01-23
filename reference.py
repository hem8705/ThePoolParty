from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def main ():
    df_marks = pd.DataFrame({'name': ['Somu', 'Kiku', 'Amol', 'Lini'], 'physics': [68, 74, 77, 78], 'chemistry': [84, 56, 73, 69], 'algebra': [78, 88, 82, 87]})

    html = df_marks.to_html()

    text_file = open("templates/index.html", "w")
    text_file.write(html)
    text_file.close()

    return render_template('index.html')

if __name__ == '__main__' :
    app.run(debug=True)