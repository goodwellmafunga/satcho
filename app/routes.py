from flask import render_template, flash, redirect, url_for
from . import mail
from .forms import ContactForm, UploadForm
from flask_mail import Message
from werkzeug.utils import secure_filename
import os

def init_routes(app):

    @app.route('/')
    def home():
        return render_template('home.html', title='Home', company_name='Satco Academic and Rehoboth Wells & Resources')

    @app.route('/about')
    def about():
        return render_template('about.html', title='About Us', company_name='Satco Academic and Rehoboth Wells & Resources')

    @app.route('/services')
    def services():
        return render_template('services.html', title='Our Services', company_name='Satco Academic and Rehoboth Wells & Resources')

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            msg = Message('Contact Form Submission',
                          recipients=[app.config['MAIL_USERNAME']])
            msg.body = f"""
    From: {form.name.data} <{form.email.data}>

    {form.message.data}
    """
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('home'))
        return render_template('contact.html', title='Contact Us', form=form, company_name='Satco Academic and Rehoboth Wells & Resources')

    @app.route('/services/<service_name>')
    def service_detail(service_name):
        services = {
            "international-business": "Detailed description of International Business & Student Advisory Services.",
            "well-drilling": "Detailed description of Well Drilling and Resource Management.",
        }
        service_description = services.get(service_name, "Service not found.")
        return render_template('service_detail.html', title=service_name.replace('-', ' ').title(), description=service_description)

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        form = UploadForm()
        if form.validate_on_submit():
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename
            ))
            flash('Image successfully uploaded', 'success')
            return redirect(url_for('upload'))
        return render_template('upload.html', form=form)
