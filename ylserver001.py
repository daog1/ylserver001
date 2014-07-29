from flask import Flask
from flask import request
from flask import redirect,url_for,flash,render_template,session
from Model import Device,Sensor,db,User
from myForm import RegistrationForm,DeviceForm,SensorForm

app = Flask(__name__)
@app.route('/v1.0/device/<did>/sensor/<sid>/datapoints',methods=['POST', 'GET'])
def datapoints(did,sid):
    dl = Device.query.filter_by(id=did).all()
    if len(dl)>0 :
        sl = Sensor.query.filter_by(id=sid).all()
        if len(sl)>0 :
            s = sl[0]
            if s.status == 1:
                return "{1}"
    return "{0}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
def valid_login(user,passwd):
    return True
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            session['username'] = request.form['username']
            return  redirect(url_for('index'))
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)
@app.route('/index', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        #return redirect(url_for('adddevice'))
        user = User.query.filter_by(username=session['username']).first()
        return render_template('index.html',user=user)
    return redirect(url_for('login'))
@app.route('/', methods=['POST', 'GET'])
def root():
    return redirect(url_for('index'))

@app.route('/adddevice', methods=['POST', 'GET'])
def adddevice():
    form = DeviceForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=session['username']).first()
        dev = Device(form.name.data,user.id,form.tags.data,
                    form.description.data)
        db.session.add(dev)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('device',id=dev.id))
    return render_template('addDevice.html', form=form)
@app.route('/device', methods=['POST', 'GET'])
def device():
    print request
    id = request.values['id']
    url = url_for('addsensor',did=id)
    dev = Device.query.get(id);
    return render_template('Device.html', addsesorurl=url,dev = dev)
@app.route('/addsensor', methods=['POST', 'GET'])
def addsensor():
    bdid = request.values.has_key('did')
    form = SensorForm(request.form)
    if bdid:
       form.did.data = request.values['did']
    if request.method == 'POST' and form.validate():
        sen = Sensor(form.name.data,form.did.data,form.tags.data,
                    form.description.data,form.status.data)
        db.session.add(sen)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('device',id=form.did.data))
    url = url_for('addsensor')
    return render_template('addsensor.html', form=form,action = url)

@app.route('/editsensor', methods=['POST', 'GET'])
def editsensor():
    #bdid = request.values.has_key('did'
    id = request.values['id']
    sen = Sensor.query.get(id)
    form = SensorForm(request.form,obj=sen)
    url = url_for('savesensor',id=id)
    return render_template('addsensor.html', form=form,action = url)
@app.route('/savesensor', methods=['POST', 'GET'])
def savesensor():
    id = request.values['id']
    sen = Sensor.query.get(id)
    form = SensorForm(request.form,obj=sen)
    form.populate_obj(sen)
    db.session.commit()
    #sen.save()
    return  redirect(url_for('index'))
    #pass
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run(host='0.0.0.0')
