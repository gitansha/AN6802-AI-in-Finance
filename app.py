from flask import Flask, render_template, request
import sqlite3
import datetime
import google.generativeai as genai
import markdown
import re
import wikipedia

app = Flask(__name__)
flag = True
api = "AIzaSyCCXOIplLPvb7lvtigD68LNXgRdKUXXjso"

@app.route("/", methods = ['POST','GET'])
def index():
    return(render_template("index.html"))

@app.route("/main", methods = ['POST','GET'])
def main():
    global flag
    if flag:
        t = datetime.datetime.now()
        user_name= request.form.get("q")
        conn = sqlite3.connect('userdb.db')
        c= conn.cursor()
        conn.execute("insert into user (name,timestamp) values (?,?)",(user_name,t))
        conn.commit()
        c.close()
        conn.close
        flag = False
    return(render_template("main.html"))

@app.route("/foodexp", methods = ['POST','GET'])
def foodexp():
    return(render_template("foodexp.html"))

@app.route("/foodexp2", methods = ['POST','GET'])
def foodexp2():
    return(render_template("foodexp2.html"))

@app.route("/foodexp_pred", methods = ['POST','GET'])
def foodexp_pred():
    q = float(request.form.get("q"))
    return(render_template("foodexp_pred.html",r = f'{(q*0.4851)+147.4:.2f}'))

@app.route("/ethical_test", methods = ['POST','GET'])
def ethical_test():
    return(render_template("ethical_test.html"))

@app.route("/FAQ", methods = ['POST','GET'])
def faq():
    return(render_template("FAQ.html"))

@app.route("/FAQ1", methods = ['POST','GET'])
def faq1():
    ques = request.form.get("response")
    genai.configure(api_key= api)
    model = genai.GenerativeModel("gemini-1.5-flash")
    answer= model.generate_content("Factors for profit")
    answer = markdown.markdown(answer.text)
    answer = re.sub(r'<.*?>', '', answer)
    return(render_template("FAQ1.html", answer = answer))

@app.route("/FAQ2", methods = ['POST','GET'])
def faq2():
    ques = request.form.get("response")
    genai.configure(api_key= api)
    model = genai.GenerativeModel("gemini-1.5-flash")
    answer= model.generate_content("Factors for profit")
    answer = markdown.markdown(answer.text)
    answer = re.sub(r'<.*?>', '', answer)
    return(render_template("FAQ1.html", answer = answer))

@app.route("/FAQ1input", methods = ['POST','GET'])
def faq1_wiki():
    ques = request.form.get("ques")
    r = wikipedia.summary(ques)
    return(render_template("FAQ1input.html", r=r))

@app.route("/test_result", methods = ['POST','GET'])
def test_result():
    answer= request.form.get("answer")
    if answer == "false":
        return(render_template("pass.html"))
    elif answer == "true":
        return(render_template("fail.html"))
    
@app.route("/userLog", methods = ['POST','GET'])
def userLog():
    conn = sqlite3.connect('userdb.db')
    c= conn.cursor()
    c.execute("Select * from user")
    r =""
    for row in c:
        r = r + str(row) + "\n"
    print(r)
    c.close()
    conn.close
    return(render_template("userLog.html", r = r))

@app.route("/deleteLog", methods = ['POST','GET'])
def deleteLog():
    conn = sqlite3.connect('userdb.db')
    c= conn.cursor()
    c.execute("Delete from user")
    conn.commit()
    c.close()
    conn.close
    return(render_template("deleteLog.html"))
    

if __name__=="__main__":
    app.run(port=8000)