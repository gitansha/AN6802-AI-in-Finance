from flask import Flask, render_template, request
import sqlite3
import datetime
import google.generativeai as genai
import time, requests
import markdown
import re
import wikipedia
import os

app = Flask(__name__)
flag = True
api = os.getenv("makersuite")
api = "AIzaSyCCXOIplLPvb7lvtigD68LNXgRdKUXXjso"

# telegram_api = os.getenv("telegram")
telegram_api = "8092694123:AAEG4eCfv6xIvWd6AcRUEZQHfC_vZmydi0E"
url = f"https://api.telegram.org/bot{telegram_api}/"

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
    # ques = request.form.get("response")
    genai.configure(api_key= api)
    model = genai.GenerativeModel("gemini-1.5-flash")
    answer= model.generate_content("Risk Assessment in Finance")
    answer = markdown.markdown(answer.text)
    answer = re.sub(r'<.*?>', '', answer)
    return(render_template("FAQ2.html", answer = answer))

@app.route("/FAQ3", methods = ['POST','GET'])
def faq3():
    # ques = request.form.get("response")
    genai.configure(api_key= api)
    model = genai.GenerativeModel("gemini-1.5-flash")
    answer= model.generate_content("Economic Indicators")
    answer = markdown.markdown(answer.text)
    answer = re.sub(r'<.*?>', '', answer)
    return(render_template("FAQ3.html", answer = answer))

@app.route("/FAQ1input", methods = ['POST','GET'])
def faq_ques():
    ques = request.form.get("ques")
    genai.configure(api_key= api)
    model = genai.GenerativeModel("gemini-1.5-flash")
    answer= model.generate_content(ques)
    answer = markdown.markdown(answer.text)
    answer = re.sub(r'<.*?>', '', answer)
    return(render_template("FAQ1input.html", r=answer))

@app.route("/test_result", methods = ['POST','GET'])
def test_result():
    answer= request.form.get("answer")
    if answer == "false":
        return(render_template("pass.html"))
    elif answer == "true":
        return(render_template("fail.html"))
    
@app.route('/telegram', methods=['GET','POST'])
def telegram():
    flag = ""
    chat_id = "6466874020"
    prompt = "Please enter the inflation rate in %: (Type exit to break)"
    err_msg = "Please enter a number"
    while True:
        msg = url + f"sendMessage?chat_id={chat_id}&text={prompt}"
        requests.get(msg)
        time.sleep(5)
        response = requests.get(url + 'getUpdates')
        data = response.json()
        text = data['result'][-1]['message']['text']
        if flag != text:
            flag = text
            if text.isnumeric():
                r = "The predicted interest rate is " + str(float(text)+1.5)
                msg = url + f"sendMessage?chat_id={chat_id}&text={r}"
                requests.get(msg)
            else:
                if text == 'exit':
                    break
                else:
                    msg = url + f"sendMessage?chat_id={chat_id}&text={err_msg}"
                    requests.get(msg)
    return(render_template("telegram.html"))
    
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