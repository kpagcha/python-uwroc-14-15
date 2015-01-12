# !/usr/bin/env python

import webapp2
import json
import datetime

import functions
import entities

from google.appengine.api import memcache

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = functions.jinja_env.get_template(template)
		params["user"] = self.user
		return t.render(params)

	def render(self, template, **params):
		self.write(self.render_str(template, **params))

	def render_json(self, d):
		json_txt = json.dumps(d)
		self.response.headers["Content-Type"] = "application/json; charset=UTF-8"
		self.write(json_txt)

	def set_secure_cookie(self, name, val):
		cookie_val = functions.make_secure_val(val)
		self.response.headers.add_header(
			"Set-Cookie",
			"%s=%s; Path=/" % (name, cookie_val)
		)

	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		return cookie_val and functions.check_secure_val(cookie_val)

	def login(self, user):
		self.set_secure_cookie("user", str(user.key().id()))

	def logout(self):
		self.response.headers.add_header(
			"Set-Cookie",
			"user=; Path=/"
		)

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie("user")
		self.user = uid and entities.User.by_id(int(uid))

		if self.request.url.endswith(".json"):
			self.format = "json"
		else:
			self.format = "html"

class BlogHandler(Handler):
	def get(self):
		currentBlogs = functions.top_blogs()

		if currentBlogs:
			currentPosts, age = currentBlogs
			secondsSince = functions.age_str(age)

		if self.format == "html":
			points = []
			for p in currentPosts:
				if p.coords:
					points.append(p.coords)

			img_url = None
			if points:
				img_url = functions.gmaps_img(points)

			self.render("blog.html", currentPosts=currentPosts, img_url=img_url, secondsSince = secondsSince)

		elif self.format == "json":
			return self.render_json([p.as_dict() for p in currentPosts])

		else:
			self.error(500)
			return

class PermalinkHandler(Handler):
	def get(self, post_id):
		content = functions.perma_link(post_id)
		if content:
			post, age = content
			secondsSince = functions.age_str(age)

		if not content:
			self.error(404)
			return

		point = None
		if post.coords:
			point = post.coords

		img_url = None
		if point:
			img_url = functions.gmaps_img([point])

		if self.format == "html":
			self.render("permalink.html", currentPosts = [post], img_url=img_url, secondsSince = secondsSince)
		elif self.format == "json":
			self.render_json(post.as_dict())
		else:
			self.error(500)
			return

class NewPostHandler(Handler):
	def get(self):
		if self.user:
			self.render("newpost.html")
		else:
			self.redirect("/blog/signup")

	def post(self):
		if self.user:
			subject = self.request.get("subject")
			content = self.request.get("content")
			coords = functions.get_coords(self.request.remote_addr)

			if subject and content:
				e = entities.BlogPost(parent = functions.blog_key(), subject=subject, content=content)
				if coords:
					e.coords = coords
				e.put()
				functions.top_blogs(True)
				this_id = str(e.key().id())

				self.redirect("/blog/%s" % this_id)

			else:
				error = "We need both a subject and a blog post!"
				self.render("newpost.html", subject=subject, content=content, error=error)

		else:
			self.redirect("/blog/signup")

class SignupHandler(Handler):
	def get(self):
		self.render("signup.html")

	def post(self):
		self.username = self.request.get("username")
		self.password = self.request.get("password")
		self.verify = self.request.get("verify")
		self.email = self.request.get("email")

		have_error = False
		params = {"username": self.username,
			"password": self.password,
			"verify": self.verify,
			"email": self.email
		}

		if not functions.valid_username(self.username):
			params["error"] = "That's not a valid username."
			have_error = True
		elif not functions.valid_password(self.password):
			params["error"] = "That's not a valid password."
			have_error = True
		elif self.password != self.verify:
			params["error"] = "Your passwords don't match."
			have_error = True
		elif not functions.valid_email(self.email):
			params["error"] = "That's not a email."
			have_error = True
		elif entities.User.by_name(self.username):
			params["error"] = "That username has already been taken."
			have_error = True

		if have_error:
			self.render("signup.html", **params)
		else:
			u = entities.User.register(self.username, self.password, self.email)
			u.put()

			self.login(u)
			self.redirect("/blog/welcome")

class WelcomeHandler(Handler):
	def get(self):
		if self.user:
			self.render("welcome.html", username = self.user.name)
		else:
			self.redirect("/blog/signup")

class LoginHandler(Handler):
	def get(self):
		self.render("login.html")

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")

		u = entities.User.login(username, password)

		if u:
			self.login(u)
			self.redirect("/blog/welcome")
		else:
			self.render("login.html", error = "Invalid login.")

class LogoutHandler(Handler):
	def get(self):
			self.logout()
			self.redirect("/blog/signup")

class FlushHandler(Handler):
	def get(self):
		memcache.flush_all()
		self.redirect("/blog")