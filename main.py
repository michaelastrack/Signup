#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re


page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>

"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

response = """
<h2> Signup </h2> <br>
<form action= "/welcome" method= "post">
<h4> Username </h4> <input type = "text" name= "username" value = "%(username)s" >
<h4> Password </h4><input type = "password" name= "pass" >
<h4> Verify Password </h4> <input type = "password" name= "vpass" >
<h4> Email (optional) </h4> <input type = "text" name= "email" value = "%(email)s" >
<input type = "submit">
</form>
"""

user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return user_re.match(username)

pass_re = re.compile(r"^.{3,20}$" )
def valid_pass(password):
    return pass_re.match(password)

email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$" )
def valid_email(email):
    return email_re.match(email)


class MainHandler(webapp2.RequestHandler):
    def write_response(self, username="", email=""):

        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        username = self.request.get("username") 
        email = self.request.get("email")

        full_response = page_header + (response % {"username": username, "email": email}) + error_element + page_footer
        self.response.out.write(full_response)

    def get(self):

        self.write_response()

class WelcomeHandler(webapp2.RequestHandler):
    def post(self):

        user_name = self.request.get("username")
        password = self.request.get("pass")
        vpassword = self.request.get("vpass")
        email = self.request.get("email")

        error = ""

        if not valid_username(user_name):
            error += "Invalid username.  "

        if not password == vpassword:
            error += "Passwords do not match.  "

        if not valid_pass(password):
            error += "Invalid password.  "

        if not (valid_email(email) or email == ""):
            error += "Invalid email address.  "

        if error != "":
            self.redirect("/?username=" + user_name + "&email=" + email + "&error=" + error)

        welcome = "<h2> Welcome, " + user_name + "! </h2>"
        full_welcome = page_header + welcome + page_footer
        self.response.write(full_welcome)

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/welcome', WelcomeHandler)
], debug=True)
