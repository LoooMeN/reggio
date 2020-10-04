# coding: utf-8
from flask import render_template, url_for, redirect, request

from reggio import app, db
from reggio.utils import *


@app.route('/settings/color')
def color():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    colors = getColorSettings()
    return render_template('colorSettings.html',
                           title='Налаштування',
                           menu=defineMenu(),
                           colors=colors)


@app.route('/saveSettings')
def saveSettings():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    valueStr = request.args.get('values')
    print(valueStr)
    return redirect(url_for('color'))


def getColorSettings():
    scssFile = os.path.join(app.root_path, 'static', 'scss', 'variables.scss')
    varList = []
    varDictList = []
    with open(scssFile) as f:
        data = f.read()
        varList = data.split('\n')
        for var in varList:
            if var:
                temp = var.split(' ')
                varDictList.append({'variable': temp[0], 'value': temp[1].replace(';', '').replace('px', '')})
    return varDictList
