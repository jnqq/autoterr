from monit import Plug, Sensors, Csv, Lcd, Fan, startmonit, Atom

if __name__ == '__main__':

    sen = Sensors()
    plug = Plug()
    csvdata = Csv()
    display = Lcd()
    fan = Fan()
    atom = Atom() 
    #monit = Monit(sen, plug, csvdata, display, fan)
    #monit.start()
    
    startmonit(sen, plug, csvdata, display, fan, atom)	
