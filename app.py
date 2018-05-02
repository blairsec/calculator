from flask import Flask, render_template, request, session
app = Flask(__name__)
app.secret_key = "pleasedonthackuseventhoughyoucanseethis"

def next_level():
    if "level" not in session: session["level"] = 0
    session["level"] += 1
    return "Completed level "+str(session["level"])

def check_blacklist(string, blacklist):
    for item in blacklist:
        if item in string: return True
    return False

def calculate(problem, sanitization):
    try:
        if sanitization == 0:
            return eval(problem)
        elif sanitization == 1:
            return eval(problem.replace("next_level", "").replace("session", ""))
        elif sanitization == 2:
            return eval(problem) if not check_blacklist(problem, ["next_level", "session", "calculate"]) else "Input blocked"
        elif sanitization == 3:
            return eval(problem) if not check_blacklist(problem, ["next_level", "exec", "eval", "session", "calculate"]) else "Input blocked"
        elif sanitization == 4:
            return eval(problem) if not check_blacklist(problem, ["next_level", "exec", "eval", "session", "globals", "calculate"]) else "Input blocked"
        elif sanitization == 5:
            return eval(problem, {'__builtins__':{}}) if not check_blacklist(problem, ["next_level", "session", "calculate"]) else "Input blocked"
        else:
            return "Nice job, you finished!"
    except Exception as e: return e

@app.route("/", methods=['GET', 'POST'])
def calculator():
    if request.method == 'GET':
        return render_template("calculator.html")
    elif request.method == 'POST':
        return render_template("calculator.html", answer=calculate(request.form["problem"], session["level"] if "level" in session else 0))


app.run()