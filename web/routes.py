from flask import Blueprint, render_template, request, jsonify, flash, send_from_directory, redirect, url_for, Response, session
import hashlib
import time
from . import db
from .models import users, animals, live
import os
import pandas as pd
from . import cam, led
routes = Blueprint('routes', __name__)
from calendar import monthrange

def liveSettings(d_temp,n_temp,d_wet,n_wet,d_start,n_start,mode,name):
	settings = live.query.filter_by(id = 1).first()
	settings.dayTemp = d_temp
	settings.nightTemp = n_temp
	settings.dayWet = d_wet
	settings.nightWet = n_wet
	settings.dayStart = d_start
	settings.nightStart = n_start
	settings.selectedMode = mode
	settings.name = name
	dTemp = settings.dayTemp
	nTemp = settings.nightTemp
	dWet = settings.dayWet
	nWet = settings.nightWet
	dStart = settings.dayStart
	nStart = settings.nightStart
	sMode = settings.selectedMode
	db.session.commit()

@routes.route('/_wykres',methods = ['GET','POST'])
def charts_process():
    df = pd.read_csv('/home/pi/github/webpage/web/.txts/random.csv')
    value = request.args.get('value')
    days = int(request.args.get('time'))
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    day = int(request.args.get('day'))
    temp = {}
    if value == 'temp' or value == "wilg" :

        tab = []
        counter = 0
        num_days = monthrange(year, month)[1]
        for _ in range(days):
            if day+counter > num_days:
                if month == 12:
                    month = 1
                    year += 1
                else:
                    month += 1
                counter = 0
                day = 1
            tmp = df.loc[(df['dzienmsc'] == day + counter) & (df['miesiac'] == month) & (df['rok'] == year)]
            tab.append(tmp)
            counter += 1

        tempp = pd.concat(tab)
        if tempp.empty:
            return "false"
        tempp = tempp.to_dict('dict')
        temp[0] = tempp
        return jsonify(temp)

    elif value == 'ruch':
        ruchh = {}
        df = pd.read_csv('/home/pi/github/webpage/web/.txts/motion.csv')
        ruch = df.loc[(df['dzien'] == day) & (df['miesiac'] == month)]
        if ruch.empty:
            return "false"
        ruch = ruch.to_dict('dict')
        ruchh[0] = ruch
        ruchh = jsonify(ruchh)
        return ruchh


@routes.route('/upload_vids/<path:filename>')
def downloadvid(filename):
	vids = "/home/pi/github/webpage/web/Videos/"
	return send_from_directory(vids, filename)

@routes.route('/upload_pics/<path:filename>')
def downloadpic(filename):
	pics = "/home/pi/github/webpage/web/Pictures/"
	return send_from_directory(pics, filename)

@routes.route('/_recording', methods = ['GET','POST'])
def recording():
	if request.method == 'POST':
		time = request.form.get('time')
		cam.recording(int(time))

	return redirect(url_for('routes.home')), flash("Rozpoczęto nagrywanie najbliższych " + time +  " sekund...", category='success')

@routes.route('/_screenshot')
def screenshot():
	cam.takescreen()
	flash("Screenshot zrobiony!", category='success')
	return redirect(url_for('routes.home'))

@routes.route('/_background_process')
def background_proces():
    data = []
    with open('web/.txts/actual.txt', 'r') as f:
        for line in f:
            data.append(line.strip())
    with open('web/.txts/last_motion.txt', 'r') as f:
        last = f.read()
        data.append(last)
    return jsonify(data)

@routes.route('/_ledOn')
def ledOn():
	led.On()
	return redirect(url_for('routes.home'))

@routes.route('/_ledOff')
def ledOff():
	led.Off()
	return redirect(url_for('routes.home'))

@routes.route('/stream')
def stream():
	return Response(cam.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@routes.route('/', methods = ['GET', 'POST'])
def home():
    if "user" in session:
        settings = live.query.filter_by(id = 1).first()
        dTemp = settings.dayTemp
        nTemp = settings.nightTemp
        dWet = settings.dayWet
        nWet = settings.nightWet
        dStart = settings.dayStart
        nStart = settings.nightStart
        sMode = settings.selectedMode
        name = settings.name
        record = ""
        if sMode == 1:
            mode = "automatyczny"
        elif sMode == 2:
            mode = "manualny"
        else:
            mode = "niewybrany"

        if request.method != 'POST':
            with open('web/.txts/set.txt', 'w') as f:
                f.write(str(dTemp) + '\n')
                f.write(str(nTemp) + '\n')
                f.write(str(dWet) + '\n')
                f.write(str(dStart) + ":00:00" + '\n')
                f.write(str(nStart) + ":00:00" + '\n')

            return render_template("index.html", user=session["user"],role = session['role'], day_temp = dTemp, night_temp = nTemp, day_wet = dWet, night_wet = nWet, day_start = dStart, night_start = nStart, mode = mode,animalName = name, pointer = led.pointer)
    else:
        flash("Musisz się zalogować", category='error')
        return redirect(url_for("routes.login"))


@routes.route('/wykresy')
def wykresy():
    if "user" in session:
        return render_template("wykresy.html", user=session["user"],role = session['role'])
    else:
        flash("Musisz się zalogować", category='error')
        return redirect(url_for("login"))

@routes.route('/climatesettings',methods = ['GET','POST'])
def climate():
	if "user" in session:
		if request.method != 'POST':
			return render_template("klimat.html", user=session["user"],role = session['role'],animals = animals.query.all(), selectedMode = 1)
		else:
			mode = int(request.form['mode'])

			if mode == 2:
				animal_day_temp = request.form['day_temp']
				animal_night_temp = request.form['night_temp']
				animal_day_wet = request.form['day_wet']
				animal_d_start = request.form['d_start']
				animal_n_start = request.form['n_start']
				liveSettings(animal_day_temp,animal_night_temp,animal_day_wet,10,animal_d_start,animal_n_start,mode,'')

				return render_template("klimat.html",animal_day_temp = animal_day_temp,animal_night_temp = animal_night_temp,animal_day_wet = animal_day_wet,animal_d_start = animal_d_start,animal_n_start = animal_n_start ,user=session["user"],role = session['role'],animals = animals.query.all(), selectedMode = mode)
			else :
				a_id = request.form['id']
				animal = animals.query.filter_by(id=a_id).first()
				name = animal.animal_name
				liveSettings(animal.day_temp,animal.night_temp,animal.day_wet,10, animal.day_start,animal.night_start,mode,name)

				return render_template("klimat.html",animalAuto = animals.query.get(a_id) ,user=session["user"],role = session['role'],animals = animals.query.all(), selectedMode = mode)
	else:
		flash("Musisz się zalogować", category='error')
		return redirect(url_for("routes.login"))


@routes.route('/photos_shots')
def photos_shots():
	if "user" in session:
		picList = os.listdir('/home/pi/github/webpage/web/Pictures')
		vidList = os.listdir('/home/pi/github/webpage/web/Videos')
		picList = sorted(picList, key = lambda x: int(x[10:-4]))
		vidList = sorted(vidList, key = lambda x: int(x[5:-4]))
		return render_template("zdjecia_filmy.html", user=session["user"],role = session['role'], picList = picList, vidList = vidList)
	else:
		flash("Musisz się zalogować", category='error')
		return redirect(url_for("routes.login"))


@routes.route('/settings',methods = ['GET','POST'])
def settings():
    if "user" in session:
        if request.method == 'POST':
            typ = request.args.get('typ')
            if typ == 'zmiana_hasla':
                passw1 = request.form.get('passw1')
                passw2 = request.form.get('passw2')
                if passw1 != passw2:
                    flash("Hasła nie są sobie równe", category='error')
                    return render_template("ustawienia.html", user=session["user"],role = session['role'],users = users.query.all())
                if len(passw1) < 6:
                    flash('Hasło musi składać się z conajmniej 6 znaków', category='error')
                    return redirect(url_for('settings'))
                user_name = request.args.get('user')
                user = users.query.filter_by(username = user_name).first()
                passw = hashlib.sha256(passw1.encode('utf-8'))
                user.password = passw.hexdigest()
                db.session.commit()
                return redirect(url_for('settings'))
            elif typ == 'zmiana_nazwy':
                username = request.form.get('username')
                username2 = request.form.get('username2')
                if username != username2:
                    flash("Nazwy nie są sobie równe", category='error')
                    return render_template("ustawienia.html", user=session["user"],role = session['role'],users = users.query.all())
                user_name = request.args.get('user')
                user = users.query.filter_by(username = user_name).first()
                user.username= username
                db.session.add(user)
                db.session.commit()

                flash('Nazwa użytkownika zmieniona')
                return redirect(url_for('settings'))
        return render_template("ustawienia.html", user=session["user"],role = session['role'],users = users.query.all())
    else:
        flash("Musisz się zalogować", category='error')
        return redirect(url_for("routes.login"))

@routes.route('/see_animals',methods = ['GET','POST'])
def see_animals():
    if "user" in session:
        if request.method != "POST":
            return render_template("zobacz_zwierz.html", user=session["user"],role = session['role'],animals = animals.query.all())

        elif request.form['delete']:
             animal_id = request.form['delete']
             animals.query.filter_by(id=animal_id).delete()
             db.session.commit()
             flash("Usunięto zwierzaka", category='success')
             return render_template("zobacz_zwierz.html", user=session["user"],role = session['role'],animals = animals.query.all())


    else:
        flash("Musisz się zalogować", category='error')
        return redirect(url_for("routes.login"))

@routes.route('/see_users', methods = ['GET', 'POST'])
def see_users():
    if "user" in session:

        if request.method != "POST":
             return render_template("zobacz_uz.html", user=session["user"],role = session['role'],users = users.query.all())

        elif request.form['delete']:
             user_id = request.form['delete']
             users.query.filter_by(id=user_id).delete()
             db.session.commit()
             flash("Usunięto użytkownika", category='success')
             return render_template("zobacz_uz.html", user=session["user"],role = session['role'],users = users.query.all())

    else:
        flash("Musisz się zalogować", category='error')
        return redirect(url_for("routes.login"))

@routes.route('/edit_user',methods = ['GET','POST'])
def edit_user():
    if "user" in session:
        if request.method != "POST":
            user_id = request.args.get('id')
            return render_template("edytuj_uz.html",userr = users.query.get(user_id), user=session["user"],role = session['role'])

        else:
            user_id = request.args.get('id')
            username = request.form['username']
            password = ""
            if request.form['password'] != "":
                password = request.form['password']
            role = request.form['role']

            if password != "":
                if len(password) < 6:
                    flash('Hasło musi składać się z conajmniej 6 znaków', category='error')
                    return render_template("edytuj_uz.html",userr = users.query.get(user_id), user=session["user"],role = session['role'])
                user = users.query.filter_by(id = user_id).first()
                user.username = username
                passw = hashlib.sha256(password.encode('utf-8'))
                user.password = passw.hexdigest()
                user.role = role
                db.session.commit()
                flash("Edytowano użytkownika", category='success')
                return render_template("zobacz_uz.html", user=session["user"],role = session['role'],users = users.query.all())
            else:
                user = users.query.filter_by(id = user_id).first()
                user.username = username
                user.role = role
                db.session.commit()
                flash("Edytowano użytkownika", category='success')
                return render_template("zobacz_uz.html", user=session["user"],role = session['role'],users = users.query.all())



    else:
        flash("Musisz się zalogować", category='error')
        return redirect(url_for("login"))

@routes.route('/edit_animal', methods=['GET','POST'])
def edit_animal():
    if "user" in session:
        if request.method != "POST":
            animal_id = request.args.get('id')
            return render_template("edytuj_animal.html",animal = animals.query.get(animal_id), user=session["user"],role = session['role'])

        else:
            animal_id = request.args.get('id')
            animal = animals.query.filter_by(id = animal_id).first()
            animal.animal_name = request.form['animalName']
            animal.day_temp = int(request.form['tempD'])
            animal.night_temp = int(request.form['tempN'])
            animal.day_wet = int(request.form['wetD'])
            animal.day_start = int(request.form['day_start'])
            animal.night_start = int(request.form['night_start'])
            db.session.commit()
            flash("Edytowano zwierzaka", category='success')
            return render_template("zobacz_zwierz.html", user=session["user"],role = session['role'],animals = animals.query.all())

    else:
        flash("Musisz się zalogować", category='error')
        return redirect(url_for("routes.login"))

@routes.route('/add_animal', methods = ['GET', 'POST'])
def add_animal():
        if "user" in session:
            if request.method == "POST":
                animal = animals(request.form['animalName'],int(request.form['tempD']),int(request.form['tempN']),int(request.form['wetD']),0,int(request.form['day_start']),int(request.form['night_start']),0,0)
                db.session.add(animal)
                db.session.commit()
                flash("Pomyślnie dodano zwierzaka", category="success")
                return render_template("dodaj_zwierz.html", user=session["user"],role = session['role'])
            else:
                return render_template("dodaj_zwierz.html", user=session["user"],role = session['role'])

        else:
            flash("Musisz się zalogować", category='error')
            return redirect(url_for("routes.login"))


@routes.route('/signUser', methods=['POST', 'GET'])
def signUser():
    if "user" in session and session['role'] == "admin":
        if request.method == "POST":
            if not request.form['username'] or not request.form['password'] or not request.form['rola']:
                flash('Wprowadź wszystkie potrzebne dane','error')
                return render_template('dodaj_uz.html')
            else:
                username = request.form.get('username')
                password = request.form.get('password')
                password2= request.form.get('password2')
                if len(username) < 2:
                    flash("Niepoprawna nazwa użytkownika.", category='error')
                    return render_template("dodaj_uz.html")
                elif len(password) < 6:
                    flash('Hasło musi składać się z conajmniej 6 znaków', category='error')
                    return render_template("dodaj_uz.html")
                elif password != password2:
                    flash('Hasła nie są takie same.', category='error')
                    return render_template("dodaj_uz.html")
                passwd1 = str(request.form['password'])
                passw = hashlib.sha256(passwd1.encode('utf-8'))
                user = users(request.form['username'], passw.hexdigest(),request.form['rola'],"")
                db.session.add(user)
                db.session.commit()
                flash("Pomyślnie utworzono konto", category="success")
                return redirect(url_for('routes.see_users'))
        else:
            return render_template("dodaj_uz.html", user=session["user"],role = session['role'])
    else:
        flash("Musisz mieć prawa administratora", category='error')
        return redirect(url_for("routes.login"))

@routes.route('/signup', methods=['POST', 'GET'])
def signup():
        if request.method == "POST":
            if not request.form['username'] or not request.form['password']:
                flash('Wprowadź wszystkie potrzebne dane','error')
                return render_template('rejestracja.html')
            else:
                username = request.form.get('username')
                password = request.form.get('password')
                password2= request.form.get('password2')
                if len(username) < 2:
                    flash("Niepoprawna nazwa użytkownika.", category='error')
                    return render_template("rejestracja.html")
                elif len(password) < 6:
                    flash('Hasło musi składać się z conajmniej 6 znaków', category='error')
                    return render_template("rejestracja.html")
                elif password != password2:
                    flash('Hasła nie są takie same.', category='error')
                    return render_template("rejestracja.html")
                passwd1 = str(request.form['password'])
                passw = hashlib.sha256(passwd1.encode('utf-8'))
                user = users(request.form['username'], passw.hexdigest(),"user","")
                db.session.add(user)
                db.session.commit()
                flash("Pomyślnie utworzono konto, możesz się zalogować", category="success")
                return redirect(url_for('routes.login'))
        else:
            return render_template("rejestracja.html")


@routes.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
        flash("Pomyślnie wylogowano", category='success')
        return redirect(url_for("routes.login"))
    else:
        return redirect(url_for("routes.login"))


@routes.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True
        if not request.form['username'] or not request.form['password']:
            flash('Wprowadź wszystkie dane', 'error')
            return render_template("login.html")
        else:
            username = request.form["username"]
            passwd = request.form["password"]
            user = users.query.filter_by(username=username).first()
            if not user or not hashlib.sha256(passwd.encode('utf-8')).hexdigest() == user.password:
                flash('Wprowadź poprawne dane', 'error')
                return render_template("login.html")

            session["user"] = username
            session["role"] = user.role
            flash("Pomyślnie zalogowano", category='success')
            return redirect(url_for("routes.home"))
    else:
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("login.html")


