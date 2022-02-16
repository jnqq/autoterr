from . import db

class users(db.Model):
    id = db.Column('user_id',db.Integer,primary_key= True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(55))
    role = db.Column(db.String(55))
    avatar = db.Column(db.String(150))

    def __init__(self,username,password, role, avatar):
        self.username = username
        self.password = password
        self.role = role
        self.avatar = avatar

class animals(db.Model):
    id = db.Column('animal_id',db.Integer,primary_key= True)
    animal_name = db.Column(db.String(50))
    day_temp = db.Column(db.Integer)
    night_temp = db.Column(db.Integer)
    day_wet = db.Column(db.Integer)
    night_wet = db.Column(db.Integer)
    day_start = db.Column(db.Integer)
    night_start = db.Column(db.Integer)
    id_user = db.Column(db.Integer)
    mode = db.Column(db.Integer)

    def __init__(self,animal_name,day_temp,night_temp,day_wet,night_wet,day_start, night_start, id_user,mode):
        self.animal_name = animal_name
        self.day_temp = day_temp
        self.night_temp = night_temp
        self.day_wet = day_wet
        self.night_wet = night_wet
        self.day_start = day_start
        self.night_start = night_start
        self.id_user = id_user
        self.mode = mode

class live(db.Model):
    id = db.Column('setting_id',db.Integer,primary_key= True)
    dayTemp = db.Column(db.Integer)
    nightTemp = db.Column(db.Integer)
    dayWet = db.Column(db.Integer)
    nightWet = db.Column(db.Integer)
    dayStart = db.Column(db.Integer)
    nightStart = db.Column(db.Integer)
    selectedMode = db.Column(db.Integer)
    name = db.Column(db.String(50))
    light = db.Column(db.Integer)
    record = db.Column(db.String(50))

    def __init__(self,dayTemp,nightTemp,dayWet, nightWet, dayStart, nightStart, selectedMode, name, light, record):
        self.dayTemp = dayTemp
        self.nightTemp = nightTemp
        self.dayWet = dayWet
        self.nightWet = nightWet
        self.dayStart = dayStart
        self.nightStart = nightStart
        self.selectedMode = selectedMode
        self.name = name
        self.light = light
        self.record = record

