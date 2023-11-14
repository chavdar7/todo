from flask import Flask , render_template , request , redirect , url_for 
import psycopg2

app = Flask(__name__)

# DATABASE'İ GENEL APP'E BAĞLAMAK İÇİN AŞAĞIDAKİ KODLARI KULLANIRIZ. 
###############################################################################################

# Connect to the database
conn = psycopg2.connect(
    database = "flask_db",
    user = "postgres",
    password = "1453",
    host = "localhost",
    port = "5432"
)  

# create a cursor
cur = conn.cursor() 

# if you already have any table or not id doesnt matter this  
# will create a products table for you.

# cur.execute('''
#     CREATE TABLE IF NOT EXISTS people(
#         id SERIAL PRIMARY KEY,
#         name varchar(255) NOT NULL,
#         surname varchar(255) NOT NULL,
#         price FLOAT NOT NULL
#     )
# ''')

# Insert some data into the table 
# cur.execute('''
#     INSERT INTO people(name,surname,price)
#     VALUES('Ahmet','Çakar',1000)
# ''')

# commit the changes
conn.commit() 

# close the cursor and connection 
cur.close()
conn.close() 

#BÜTÜN GÖREVLERİN GÖZÜKTÜĞÜ ANA SAYFAMIZ
###############################################################################################


@app.route("/")
def index():

    conn = psycopg2.connect(
        database = "flask_db",
        user = "postgres",
        password = "1453",
        host = "localhost",
        port = "5432"
    )

    cur = conn.cursor()

    # Select all products from the table 
    cur.execute("SELECT * FROM todo")

    # Fetch all the records
    data = cur.fetchall()


    conn.commit()
    cur.close()
    conn.close()

    return render_template("index.html", data = data)


#GÖREV EKLEMEK İÇİN GEREKEN ROUTE/ SONRASINDA İNDEXE YÖNLENDİRİYORUZ
###############################################################################################

@app.route("/add", methods = ["POST"])
def add():

    conn = psycopg2.connect(
        database = "flask_db",
        user = "postgres",
        password = "1453",
        host = "localhost",
        port = "5432"
    )

    cur = conn.cursor()

    # get data from the form
    date = request.form["date"]
    title = request.form["title"]
    description = request.form["description"]
    is_finish = request.form["is_finish"]

    # Insert data into the table
    cur.execute('''
        INSERT INTO todo(data,title,description,is_finish)
        VALUES(%s,%s,%s,%d)''',(date,title,description,is_finish)
    )

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("index"))


#GÖREV GÜNCELLEMEK İÇİN GEREKEN ROUTE/ SONRASINDA İNDEXE YÖNLENDİRİYORUZ
###############################################################################################

@app.route('/guncel', methods=['POST']) 
def update(): 
    conn = psycopg2.connect(database="flask_db", 
                            user="postgres", 
                            password="1453", 
                            host="localhost", 
                            port="5432"
                        ) 
  
    cur = conn.cursor() 
  
    # Get the data from the form 
    name = request.form['name'] 
    surname = request.form['surname']
    price = request.form['price'] 
    id = request.form['id'] 
  
    # Update the data in the table 
    cur.execute( 
        '''UPDATE people 
        SET name=%s, price=%s, surname=%s WHERE id=%s''', (name, price, surname, id)) 
  
    # commit the changes 
    conn.commit() 
    return redirect(url_for('index')) 


#GÖREV SİLMEK İÇİN GEREKEN ROUTE/ SONRASINDA İNDEXE YÖNLENDİRİYORUZ
###############################################################################################

@app.route("/delete" , methods = ["POST"])
def delete():
    conn = psycopg2.connect(
        database = "flask_db",
        user = "postgres",
        password = "1453",
        host = "localhost",
        port = "5432"
    )

    cur = conn.cursor()

    #get id from the form
    id = request.form["id"]

    cur.execute('''
    DELETE FROM people WHERE id = %s''',(id,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("index"))

#PROGRAMIN ÇALIŞMASINI VE DEĞİŞİKLİK YAPTIĞIMIZDA KAPANMAMASINI SAĞLAYAN KOD
###############################################################################################

if __name__ == '__main__':
    app.run(debug=True)

###############################################################################################
