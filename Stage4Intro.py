import webapp2
import jinja2
import os
import time
from google.appengine.ext import ndb
import logging



class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                                                        autoescape = True)
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        error = 0
        Help = Helper()
        data = Help.get_data()
        [disableLesson, disableConcept, disableInformation] = Help.radio_buttons()
        self.render('template.html', data = data, disableLesson = disableLesson, 
                   disableConcept = disableConcept, disableInformation = disableInformation, 
                   error = error)
class Submit(Handler):
    def get(self):
        note_text = self.request.get("note_text")
        if note_text:
            error = 0
            ID = Note()
            ID.type_of_note = self.request.get('type_of_note')
            ID.note_text = note_text
            ID.put()
            time.sleep(1)
            Help = Helper()
            data = Help.get_data()
            [disableLesson, disableConcept, disableInformation] = Help.radio_buttons()
            self.render('template.html', data = data, disableLesson = disableLesson, 
                   disableConcept = disableConcept, disableInformation = disableInformation, 
                   error = error)
        else:
            error = 1
            Help = Helper()
            data = Help.get_data()
            [disableLesson, disableConcept, disableInformation] = Help.radio_buttons()
            self.render('template.html', data = data, disableLesson = disableLesson, 
                   disableConcept = disableConcept, disableInformation = disableInformation, 
                   error = error)
class Helper:
    def get_data(self):
        return Note.query().order(Note.date)
    def radio_buttons(self):
        qry = Note.query().order(-Note.date).fetch(1)
        if qry:
          type_of_note = qry[0].type_of_note
          if type_of_note == 'Lesson':
              return ['disabled', '', 'disabled']
          if type_of_note == 'Concept':
              return ['disabled', 'disabled', '']
          else:
              return ['', '', '']
        else:
            return ['','disabled','disabled']
class Note(ndb.Model):
    type_of_note = ndb.StringProperty()
    note_text = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
app = webapp2.WSGIApplication([('/', MainPage), 
															('/Submit', Submit)],
															 debug=True)

