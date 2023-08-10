from flask import Flask, render_template
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    db_conn = pymysql.connect(host='127.0.0.1', user='root',
            password='Hu$r9nq!', database='onlypixel',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    with db_conn:
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT title, content, image_path FROM news")
        news = db_cursor.fetchall()
    return render_template('home.html', news=news)

if __name__ == "__main__":
    app.run(debug=True)