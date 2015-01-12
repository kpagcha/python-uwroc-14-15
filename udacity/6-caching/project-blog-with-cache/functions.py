# !/usr/bin/env python

import os
import jinja2
import hmac
import random
import string
import hashlib
import re
import urllib2
import logging
import datetime
import time

import entities

from xml.dom import minidom
from google.appengine.ext import db
from google.appengine.api import memcache

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
	autoescape = True)

SECRET = "imsosecret"

def hash_str(s):
	return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	val = h.split("|")[0]
	if h == make_secure_val(val):
		return val

def make_salt():
	return "".join(random.choice(string.ascii_letters) for x in range(5))

def make_pw_hash(name, pw, salt=None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return "%s|%s" % (salt, h)

def valid_pw(name, pw, h):
	salt = h.split("|")[0]
	return h == make_pw_hash(name, pw, salt)

def users_key(group = "default"):
	return db.Key.from_path("users", group)

def blog_key(name = "default"):
	return db.Key.from_path("blogs", name)

user_regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and user_regex.match(username)

pass_regex = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and pass_regex.match(password)

email_regex = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
	return not email or email_regex.match(email)

IP_URL = "http://api.hostip.info/?ip="

def get_coords(ip):
	url = IP_URL + ip
	xml = None
	try:
		xml = urllib2.urlopen(url).read()
	except URLError:
		return None

	if xml:
		x = minidom.parseString(xml)
		coords = x.getElementsByTagName("gml:coordinates")
		if coords and coords[0].childNodes[0].nodeValue:
			lon, lat = coords[0].childNodes[0].nodeValue.split(",")
			return db.GeoPt(lat, lon)

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=500x500&sensor=false&"

def gmaps_img(points):
	markers = "&".join("markers=%s,%s" % (p.lat, p.lon) for p in points)
	return GMAPS_URL + markers

def age_set(key, val):
	save_time = datetime.datetime.utcnow()
	memcache.set(key, (val, save_time))

def age_get(key):
	r = memcache.get(key)
	if r:
		val, save_time = r
		age = (datetime.datetime.utcnow() - save_time).total_seconds()
	else:
		val, age = None, 0
	return val, age

def top_blogs(update = False):
	mc_key = "top_blogs"
	posts, age = age_get(mc_key)
	if posts is None or update:
		logging.error("DB QUERY")
		if update:
			time.sleep(0.1)
		posts = entities.db.GqlQuery("SELECT * "
			"FROM BlogPost "
			"ORDER BY created DESC "
			"LIMIT 10")
		posts = list(posts)
		age_set(mc_key, posts)
	return posts, age

def perma_link(post_id):
	mc_key = str(post_id)
	post, age = age_get(mc_key)
	if not post:
		logging.error("DB QUERY")
		post = entities.BlogPost.get_by_id(int(mc_key), parent=blog_key())
		age_set(mc_key, post)
	return post, age

def age_str(age):
	s = "Queried %s seconds ago"
	age = int(age)
	if age == 1:
		s = s.replace("seconds", "second")
	return s % age