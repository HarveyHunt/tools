from jinja2 import Environment
import json
from bottle import get, post, run, request
import os
html = """
<html>
<body>
<form method="post">
<div class="row">
    <label for="txtarea_Jinja2Template" id="Jinja2Template-ariaLabel">Jinja2 Template</label>
    <textarea id="txtarea_Jinja2Template" name="txtarea_Jinja2Template" cols="120" rows="20" aria-labelledby="Jinja2Template-ariaLabel">{0}</textarea>
</div>
<div class="row">
    <label for="txt_Jinja2JSONData" id="Jinja2JSONData-ariaLabel">Jinja2 JSON Data</label>
    <input id="txt_Jinja2JSONData" name="txt_Jinja2JSONData" type="text" size=120" aria-labelledby="Jinja2JSONData-ariaLabel" value="{1}" />
</div>
<div class="row">
    <label for="txt_Jinja2JSONFile" id="Jinja2JSONData-ariaLabel">Jinja2 JSON File</label>
    <input id="txt_Jinja2JSONFile" name="txt_Jinja2JSONFile" type="text" size=120" aria-labelledby="Jinja2JSONFile-ariaLabel" value="{2}" />
</div>
<div class="row">
    <label for="txtarea_Result" id="Result-ariaLabel">Result</label>
    <textarea id="txtarea_Result" name="txtarea_Result" cols="120" rows="20" aria-labelledby="Result-ariaLabel">{3}</textarea>
</div>
<div class="row">
<input type="submit" value="Submit" />
</div>
</form>
</html>
</body>
"""


@get('/')
def index():
    return html.format("", "", os.getcwd(), "")


@post('/')
def index():
    filename = request.forms.get('txt_Jinja2JSONFile')
    env = Environment(extensions=['jinja2.ext.do'])
    tmpl = request.forms.get('txtarea_Jinja2Template')
    try:
        # Prevent a bug whereby the app crashes if the file doesn't exist.
        json_data = request.forms.get('txt_Jinja2JSONData')
        if filename is not '' and 'json' in os.path.splitext(filename)[-1]:
            json_data = open(filename, 'r').read()
        jinja_tmpl = env.from_string(tmpl)
        return html.format(tmpl, json_data, filename, jinja_tmpl.render(data=json.loads(json_data), set=set))
    except Exception as e:
        return html.format(tmpl, json_data, filename, e.__class__.__name__ + ": " + str(e))
run(host='0.0.0.0', port=8080, reloader=True)
