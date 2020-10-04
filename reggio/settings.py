# coding: utf-8
from flask import render_template, url_for, redirect, request

from reggio import app, db
from reggio.utils import *


@app.route('/settings/color')
def color():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    styleSettings = getStyleSettings()
    return render_template('colorSettings.html',
                           title='Налаштування',
                           menu=defineMenu(),
                           styleSettings=styleSettings)


@app.route('/saveSettings')
def changeStyleSettings():
    if not checkPageAvailability([]):
        return redirect(url_for('main'))
    scssFile = os.path.join(app.root_path, 'static', 'scss', 'variables.scss')
    backupFile = os.path.join(app.root_path, 'static', 'scss', 'backup.scss')
    if request.args.get('id') == 'save':
        styleSettings = request.args.get('values').replace(';', ';\n')
        with open(scssFile, 'w') as f:
            f.write(styleSettings)
            f.close()
    if request.args.get('id') == 'reset':
        f = open(backupFile, 'r')
        backupStyles = f.read()
        f.close()
        f = open(scssFile, 'w')
        f.write(backupStyles)
        f.close()

    return redirect(url_for('color'))


def getStyleSettings():
    scssFile = os.path.join(app.root_path, 'static', 'scss', 'variables.scss')
    varList = []
    varDictList = []
    with open(scssFile, 'r') as f:
        data = f.read()
        varList = data.split('\n')
        for var in varList:
            if var:
                temp = var.split(' ')
                varDictList.append({'variable': temp[0], 'value': temp[1].replace(';', '').replace('px', '')})
    return varDictList
