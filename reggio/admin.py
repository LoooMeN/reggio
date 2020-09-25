# coding: utf-8
from flask import request, flash, redirect, url_for, render_template

from reggio import app, db
from reggio.models import individualClass
from reggio.utils import *


@app.route('/admin/individualClasses')
def adminIndividualClasses():
    if not checkPageAvailability(['admin']):
        return redirect(url_for('main'))
    individualClasses = individualClass.query.all()
    return render_template(
        'adminIndividualClasses.html',
        individualClasses=individualClasses,
        title=u'Індивідулки',
        menu=defineMenu())


@app.route('/admin/deleteIndividualClasses', methods=["GET"])
def deleteIndividualClasses():
    if not checkPageAvailability(['admin']):
        return redirect(url_for('main'))
    IndividualClassesID = request.args.get('id')
    IndividualClasses = db.session.merge(individualClass.query.filter_by(id=IndividualClassesID).first())
    db.session.delete(IndividualClasses)
    db.session.commit()
    return redirect(url_for('adminIndividualClasses'))
