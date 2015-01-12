import webapp2
import re
import cgi

form = """
<h2>Enter some text to ROT13:</h2>
<form method="post">
	<textarea name="text" style="height: 100px; width: 400px;">%s</textarea>
	<br>
	<input type="submit">
</form>
"""


user_form = """
<style type="text/css">
    .label {text-align: right}
    .error {color: red}
</style>
<h2>Signup</h2>
<form method="post">
	<table>
		<tbody>
		    <tr>
		      <td class="label">Username</td>
		      <td> <input type="text" name="username"></td>
		      <td class="error">%(error_username)s</td>
		    </tr>
		    <tr><td class="label">Password</td><td>
		        <input type="password" name="password"></td>
		      <td class="error">%(error_password)s</td>
		    </tr>
		    <tr>
		      <td class="label">Verify Password</td><td><input type="password" name="verify"></td>
		      <td class="error">%(error_verify)s</td>
		    </tr>
			<tr>
		      <td class="label">Email (optional)</td>
		      <td><input type="text" name="email"></td>
		      <td class="error">%(error_email)s</td>
		    </tr>
		</tbody>
	</table>
	<input type="submit">
</form>
"""

class UserHandler(webapp2.RequestHandler):
	def write_form(self, e_username="", e_password="", e_verify="", e_email=""):
		self.response.out.write(user_form % {
				"error_username": e_username,
				"error_password": e_password,
				"error_verify": e_verify,
				"error_email": e_email
			});

	def get(self):
		self.write_form()

	def post(self):
		username = self.valid_username(self.request.get("username"))
		password = self.valid_password(self.request.get("password"))
		verify = ""
		if not password:
			verify = self.valid_verify(self.request.get("password"), self.request.get("verify"))
		if verify:
			password = ""
		email = self.valid_email(self.request.get("email"))

		if not username and not password and not verify and not email:
			escaped_username = cgi.escape(self.request.get("username", True))
			self.redirect("/welcome?username=%s" % escaped_username)
		else:
			self.write_form(username, password, verify, email);

	def valid_username(self, username):
		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		if USER_RE.match(username):
			return ""
		return "That's not a valid username."

	def valid_password(self, password):
		PASSWORD_RE = re.compile(r"^.{3,20}$")
		if PASSWORD_RE.match(password):
			return ""
		return "That wasn't a valid password."

	def valid_verify(self, password, confirm):
		if password == confirm:
			return ""
		return "Your passwords didn't match."

	def valid_email(self, email):
		if not email:
			return ""
		EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
		if EMAIL_RE.match(email):
			return ""
		return "That's not a valid email."

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Welcome, %s!" % self.request.get("username"))


def ROT13(s):
	result = ""
	alphabet_down = "abcdefghijklmnopqrstuvwxyz"
	alhabet_up = alphabet_down.upper()
	for c in s:
		if c in alphabet_down:
			result += alphabet_down[(alphabet_down.index(c)+13)%26]
		elif c in alhabet_up:
			result += alhabet_up[(alhabet_up.index(c)+13)%26]
		else:
			result += c
	return result

class MainHandler(webapp2.RequestHandler):
	def write_form(self, rot13=""):
		self.response.out.write(form % rot13)

	def get(self):
		self.write_form()

	def post(self):
		rot13 = ROT13(self.request.get("text"))
		self.write_form(rot13)

app = webapp2.WSGIApplication([('/', MainHandler),
									('/user', UserHandler),
									('/welcome', WelcomeHandler)], debug=True)