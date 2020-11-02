from flask import Flask, render_template
import glob
import os

app = Flask('app')

@app.route('/splitscreen/<tab_num>')
def splitscreen(tab_num):
  return render_template("splitscreen.html", tabs=tab_num)

@app.route('/<path>')
def folder(path):
  print(path)
  path = path.replace("|SEP|", "/")
  print(path)
  print(os.path.isfile(path))
  if os.path.isdir("/" + path) is False:
    path = "/" + path
    with open(path, "rb") as f:
      temp = "".join([line.decode("utf-8") for line in f])
      return render_template("file.html", file=temp, path=path)

  expression = "/" + path + "/*"
  if path == "/":
    expression = "/*"
  files = glob.glob(expression)
  files.sort()
  link = '|SEP|'.join(path.split('/')[:1])
  if link == path:
    link = "/"
  files_formatted = [
    {
      "filename": "..",
      "filetype": "folder",
      "size": "",
      "link": link
    }
  ]
  for file in files:

    filetype = "file"
    size = ""
    if os.path.isdir(file):
      new_expression = f"{file}/*"
      #print(new_expression)
      size = len(glob.glob(new_expression))
      filetype = "directory"
    else:
      size = str(os.path.getsize(file) / 1000) + "kb"

    
  
    files_formatted.append({
      "filename": file,
      "filetype": filetype,
      "size": size,
      "link": file[1:].replace('/', '|SEP|')
      })
    
  return render_template("folder.html", folders=files_formatted, path=path)

@app.route("/")
def index():
  return folder("/")

app.run(host='0.0.0.0', port=8080)