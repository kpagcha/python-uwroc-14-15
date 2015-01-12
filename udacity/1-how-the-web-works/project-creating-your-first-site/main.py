import webapp2

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Hello, Udacity!")

app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)