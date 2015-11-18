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
			jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))
			t = jinja_env.get_template(template)
			return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		error = 0
		self.render('base.html')
class TestHandler(Handler):
	def get(self):
		note_text = self.request.get("note_text")
		if note_text:
			error = 0
			ID = Note()
			ID.type_of_note = self.request.get('type_of_note')
			ID.note_text = note_text
			ID.put()
			self.render('base.html', type_of_note = ID.type_of_note, note_text = ID.note_text)
			logging.debug('ID: ' + str(ID) + 'Date: ' + str(ID.date) + 'text: ' + ID.note_text + 'type of note: ' + ID.type_of_note)
		else:
			error = 1
			self.render('base.html')
			other = self.get_data()
			self.response.write(other)
	def get_data(self):
		self.all_data = Note.query()
class Note(ndb.Model):
	type_of_note = ndb.StringProperty()
	note_text = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)
		
app = webapp2.WSGIApplication([('/', MainPage), 
															('/TestHandler', TestHandler)],
															 debug=True)

