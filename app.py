from flask import Flask, request ,escape
import sys,basecrack,exifread,os
from werkzeug.utils import secure_filename

app = Flask(__name__,static_folder='static/')
app.config["DEBUG"] = True

UPLOAD_FOLDER = 'uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1000 

home = '''<html>
        <head>
        <link rel="shortcut icon" type="image/png" href="/static/favicon.png">
        </head>
    <title>Basecrack-web</title>
            <body>
            <script src="/static/test.js"></script>
            <link rel="shortcut icon" type="image/png" href="/static/favicon.png">
            <link rel= "stylesheet" type= "text/css" href="/static/main.css">

                {errortext}

                <div class=layout-container>     
                <main>
                <p>[*] Enter your encode base here :</p>
                <script type="text/javascript"></script>
                
                <form method="post" action="." enctype="multipart/form-data"> 
                <p><input type="radio" name="type1" value="text" id="text" style="display:none;" >From text : <textarea type="text" name="base" onclick="check();" class="fixed"></textarea>  <input type="reset" value="Reset"></p>   
                    <p>[*] OR upload encoded base from file :</p>                           
                <p><input type="radio" name="type1" value="file" id="file" style="display:none;" >From file <input onchange="validateSize(this)" type="file" name="basefile1" onclick="uncheck();"/><small>(NB:5 MB max for all files)</small></p>  
                   <p>[*] OR From exif data! :</p>
                    <p><input type="radio" name="type1" value="exif" id="exif" style="display:none;" >From image <input type="file" onchange="validateSize(this)" name="exif" onclick="exifcheck();"  accept="image/*"/></p>
                    <p><input type="submit" value="Upload & Decode!" /></p>
                </form>
                
                </main>
                <here>
                <aside>
                <p><b>Supported Encoding Schemes : </b></p>
                <ul class=no>
                    <li>Base16</li>
                    <li>Base32</li>
                    <li>Base36</li>
                    <li>Base58</li>
                    <li>Base62</li>
                    <li>Base64</li>
                    <li>Base64Url</li>
                    <li>Base85</li>
                    <li>Ascii85</li>
                    <li>Base91</li>
                    <li>Base92</li>
                    <li>Base100</li>
                </ul>
                </aside>
                </here>
                </div>
                <p>This is built using mufeedvh's <a href="https://github.com/mufeedvh/basecrack" target="_blank" >basecrack</a> and its API support ; Feel free to leave a 🌟 there <p>
                <footer> 
            <ul> <a href="https://github.com/b1nslashsh/basecrack-web" target="_blank" ><img src="/static/github.png" style="width:25px;height:25px;"></a> 
            <a href=mailto:admin@b1nslashsh.tech target="_blank" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Report an issue / Feedback </a>
            </ul></footer> 
            </body>
        </html>
    '''
type1 = ''
@app.route("/", methods=["GET","POST"])
def adder_page():
    errortext = ""
    errors = ""
    global home
    global type1
    if request.method == "POST":

        base = None
        basefile1 = None
        type1 = None
        exif = None
        filename = None
        try:

            base = escape(str(request.form["base"]))
            type1 = request.form.get("type1")

        except:
            errortext = "<p> <b><i> Error </i></b> : Please try anything to decode</p>\n"
        if type1 == "text" and base == "" :
            errortext = "<p> <b> <i>Error </i></b> : Please try anything to decode</p>\n"

        elif type1 == "text" : 
            base = base.strip()
            result =  basecrack.BaseCrack().decode(base)
            if result is not None:
                return '''
            <!DOCTYPE html>
            <html> 
            <head> 
            <title>Results </title> 

            <script src="/static/test.js"></script>
            <link rel= "stylesheet" type= "text/css" href="/static/main.css">
            <link rel="shortcut icon" type="image/png" href="/static/favicon.png">
            </head> 
            <body> 
            <div class="container"> 

                    <p><b>Encoded Base   : </b>"{encode}" </p>
                    <div style="overflow: hidden;">
                    <p style = "float : left;"> <b>Decoded Base  :</b>&nbsp;</p>
                    <textarea style = "float : center; "id="result" value="assa" class="result">{decode} </textarea>
                    <button id="this" onclick="toclip('result');"><code>Copy to clipboard</code></button>
                    </div>
                    <p><b>Encoded Scheme : </b>"{scheme}" </p>
                    <p><a href="/">Click here to decode Another one </a></p>

            </div> 
            <footer> 
            <ul> <a href="https://github.com/b1nslashsh" target="_blank"><img src="/static/github.png" style="width:25px;height:25px;"></a> 
            <a href=mailto:admin@b1nslashsh.tech target="_blank" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Report an issue / Feedback </a>
            </ul></footer> 
            </body>
            </html>
                '''.format(encode = base, decode = escape(result[0]),scheme = result[1])
            else:
                if len(base) > 20:
                    base = base[0:20]+"......"
                else :
                    pass
                errortext = "<p><b> <i>Error</i> </b>: '{}' Is not a valid base</p>\n".format(base)
        elif type1 == "exif":
            try :
                exif = request.files['exif'] 
                exif.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(exif.filename))) 
                filename = exif.filename
                result2,data2 = output(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(exif.filename)))
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            except Exception:
                errortext = "<p> <b> <i>Error </i></b> : This file doesn't contain exif data! or it can't be decode :( </p>\n"
            else:
                return fileoutput(result2,data2,filename)

        elif type1 == "file":
            try :
                f = request.files['basefile1']  
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                filename = f.filename              
                result1,data = basefilecrack(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            except Exception:
                errortext = "<p> <b> <i>Error </i></b> : Please select a valid base file to decode! </p>\n"
            else :
                return fileoutput(result1,data,filename)

    return home.format(errortext=errortext)


def basefilecrack(inputfile):
    result = []
    data = []

    with open(inputfile) as file:
        for line in file:
            result.append(basecrack.BaseCrack().decode(line.strip()))
            data.append(line.strip())
        return result,data    

def output(exif):
    result3 = []
    data3 = []
 
    read_image = open(exif, 'rb')
    exif_tags = exifread.process_file(read_image)
    for tag in exif_tags:

        split_tag = str(exif_tags[tag]).split(' ')
        for base in split_tag:
            if len(base) < 3 or '\\x' in base: continue
            for base in base.splitlines():
                result3.append(basecrack.BaseCrack().decode(base.strip()))
                data3.append(base)
    return result3,data3


def fileoutput(result1, data,filename):
    result = ""
    global home
    global type1
    if all(v is None for v in result1) != True:
        for i in range(len(result1)):
            if(result1[i] is not None):
                result += '''
                    <p>Encoded From : {encode1} </p>
                    <p>Decoded Base   : "{decode1}" </p>
                    <p>Encoded Scheme : "{scheme}" </p>
                    <br>
                '''.format(encode1=escape(data[i]), decode1=escape(result1[i][0]), scheme=result1[i][1])

        body = '''
                <!DOCTYPE html>
                <html> 
                <head> 
                <title>Results </title> 
                <script src="/static/test.js"></script>
                <link rel="shortcut icon" type="image/png" href="/static/favicon.png">
                <link rel= "stylesheet" type= "text/css" href="/static/main.css">
                </head> 
                <body> 
                <div class="container"> 
                    <p><b>Decoding Base Data From : </b>{basefile}</p>
                    {result}
                    <p><a href="/">Click here to decode Another one </a>
                </div> 
                <footer> 
                <ul> <a href="https://github.com/b1nslashsh" target="_blank" ><img src="/static/github.png" style="width:25px;height:25px;"></a> 
                </ul> </footer>  
                </body>
                </html>
            '''.format(basefile=escape(filename), result=result)   

        return body
    elif type1 == "exif" :
        errortext = "<p> <b> <i>Error </i></b> : This file doesn't contain exif data! or it can't be decode :( </p>\n"
        return home.format(errortext = errortext)
    else:
        errortext = "<p> <b> <i>Error </i></b> : Please select a valid base file to decode! </p>\n"
        return home.format(errortext = errortext)  

@app.errorhandler(404)
def page404(e):

    return ''' 
<html>
   <head>
      <link rel="shortcut icon" type="image/x-icon" href="favicon.ico">
      <meta http-equiv = "refresh" content="3 ; /" />
   </head>
   <body>
   <p>Thats not found ; hold on redirecting to home </p>
  </body>
</html>
    ''' , 404

if __name__ == '__main__':
    app.run()
