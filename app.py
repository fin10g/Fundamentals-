#import mysql.connector
#from mysql.connector import Error
from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
import paramiko

app = Flask(__name__)
app.config['ENV'] = "Development"
app.config['DEBUG'] = True
@app.route('/')
def hello_world():
    return 'hello test'

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/search', methods=['GET'])
def search():
    item = request.args.get("item")
    instance_ip = "54.217.225.49"  # Public IP# CHANGE THIS
    securityKeyFile = "/home/student/.ssh/UbuntuCT169.pem"  # CHANGE THIS
    searchTerm = item # CHANGE THIS

    #cmd = "python3 ~/Desktop/1SDC1/Semester 2/Fundamentals of Cloud/Assignment Project/wiki.py"  # CHANGE THIS
    cmd = "python3 ~/FlaskAssignment/wiki.py"  # CHANGE THIS


    if not item:
        return '''
               <!DOCTYPE html>
               <html lang="en">
               <head>
                   <meta charset="UTF-8">
                   <title>Search</title>
               </head>
               <body>
                   <h2>Search</h2>
                   <form method="GET" action="/search">
                       <label>Item: </label>
                       <input type="text" name="item" placeholder="Enter item"/>
                       <input type="submit" value="Search"/>
                   </form>
               </body>
               </html>
           '''
   # mysql.connector.connect(host="localhost", user="root", password="mypassword", database="wiki")

    try:
        # Connect/ssh to an instance
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file(securityKeyFile)
        client.connect(hostname=instance_ip, username="ubuntu", pkey=key)

        # Execute a command(cmd) after connecting/ssh to an instance
        stdin, stdout, stderr = client.exec_command(cmd + " " + searchTerm)
        stdin.close()
        outerr = stderr.readlines()
        print("ERRORS: ", outerr)
        output = stdout.readlines()

        # Get/Use the result
        print("output:", output)
        for items in output:
            print(items, end="")

        # Close the client connection once the job is done
        client.close()
    except Exception as e:
        print(e)
        return f"Error: {str(e)}"

    finally:
                print("Connection is closed")

        # Return results from wiki.py
    return '''
           <!DOCTYPE html>
           <html lang="en">
           <head>
               <meta charset="UTF-8">
               <title>Search Results</title>
               <style>
                pre {
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    font-family: Arial, sans-serif;
                    font-: 14px;
                    line-height: 1.6;
                    max-width: 900px;
                    margin: 20px auto;
                    padding: 20px;
                }
                h2 { text-align: center; }
                .back { display: block; text-align: center; margin: 20px; }
                </style>
           </head>
           <body>
               <h2>Results for: ''' + item + '''</h2>
               <pre>''' + ''.join(output) + '''</pre>
               <a class="back" href="/search">Search again</a>
           </body>
           </html>
       '''

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888)