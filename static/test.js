function toclip(id) {{
    var r = document.createRange();
    r.selectNode(document.getElementById(id));
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(r);
    document.execCommand('copy');
    document.getElementById("this").innerHTML = "Copied!";
    console.log(f)

                    }}
function check() {{
  document.getElementById("text").checked = true;
                }}
function uncheck() {{
  document.getElementById("file").checked = true;
                    }}
function exifcheck() {{
  document.getElementById("exif").checked = true;
                    }}