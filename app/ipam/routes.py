from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, current_user

from app import bcrypt, db
from app.ipam.forms import RequestIpForm
from app.ipam.ipamdata import IpamRegister, IpamLogin, AddressCheckout, IpamConnect

from flask import Blueprint, render_template
from flask_login import login_required

ipam = Blueprint('ipam', __name__)


@ipam.route('/ipam', methods=['GET', 'POST'])
@login_required
def index():
    
    ipamconnect = IpamConnect(current_user)
    if ipamconnect['status'] == 'success':
        ipam_token = ipamconnect['data']['token']
        flash(ipamconnect['message'], category='info')
        
        form = RequestIpForm(request.form)
        if form.validate_on_submit():
            fqdn = str(form.fqdn.data).lower()
            network = form.network.data
            ipcount = form.ipcount.data

            ipRequest = {
                'network': network, 
                'fqdn': fqdn,
                'ipcount': ipcount,
                'ipam_token': ipam_token
            }
            result = AddressCheckout(ipRequest)

            flash('Successfully requested IP Addresses '+ str(result), category='info')
    else:
        
        flash(ipamconnect['data']['error'], category='danger')

    return render_template('ipam/index.html',form=form)
