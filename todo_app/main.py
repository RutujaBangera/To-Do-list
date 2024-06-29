from flask import Flask, render_template, url_for, request, redirect
import random

app = Flask(__name__)

todos= []

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if(request.method=="POST"):
        todo_name=request.form["todo_name"]
        cur_id=random.randint(1,1000)
        todos.append({
            'id': cur_id,
            'name': todo_name,
            'checked': False
        })
    return render_template("index.html", items=todos)

@app.route("/checked/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    for todo in todos:
        if todo['id']==todo_id:
            todo['checked']= not todo['checked']
            break
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    global todos
    for todo in todos:
        if todo['id']==todo_id:
            todos.remove(todo)
    return redirect(url_for("home"))

@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit_todo(todo_id):
    if request.method == "GET":
        for todo in todos:
            if todo['id'] == todo_id:
                return render_template("edit.html", todo=todo)  
        return redirect(url_for("home")) 

    if request.method == "POST":
        if "edited_todo" in request.form:  
            edited_todo = request.form["edited_todo"]
            for todo in todos:
                if todo['id'] == todo_id:
                    todo['name'] = edited_todo
                    break
            return redirect(url_for("home"))
        return redirect(url_for("edit_todo", todo_id=todo_id))  


if __name__=="__main__":
    app.run(debug=True)
