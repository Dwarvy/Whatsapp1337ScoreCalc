#!/usr/bin/python3
class Line(object):
    def __init__(self, date, time, person, message):
        self.date = date
        self.time = time
        self.person = person
        self.message = message

class WhatsappChat(object):
    def __init__(self, whatsappExport):
        self.lines = str(whatsappExport).split('\n')
        self.lang = self.detectLang(self.lines[0])
        
    def detectLang(self, line):
        if line.find('-') < 5:
            return "NL"
        elif line.find('/') < 7:
            return "EN"
        else:
            return "ERROR"
     
    def parseLine(self, line):
        line = line.replace('\\xe2\\x80\\xaa', "")
        line = line.replace('\\xe2\\x80\\xac', "")
        line = line.replace("\u202c", "")
        line = line.replace("\u202a", "")
        if self.lang == "EN":
            if len(line) >= 6:
                if line.find(',') > 9:
                    return "ERROR"
                #remove some weird chars
                
                DateTimeAndPersonMessage = line.split("-", 1)
                if len(DateTimeAndPersonMessage) != 2:
                    return "ERROR"
                    
                DateAndTime = DateTimeAndPersonMessage[0].split(",", 1)
                if len(DateAndTime) != 2:
                    return "ERROR"
                
                PersonAndMessage = DateTimeAndPersonMessage[1].split(":", 1)
                if len(PersonAndMessage) != 2:
                    return "ERROR"
                    
                date = DateAndTime[0].strip()
                time = DateAndTime[1].strip()
                person = PersonAndMessage[0].strip()
                message = PersonAndMessage[1].strip()
                
        return Line(date, time, person, message)