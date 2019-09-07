Quickstart contact form processing
----------------------------------

This will be useful if...

* You want to forward a simple contact form to your email
* You have a (S3) static site and don't want to run a server

Usage
-----

Grab a [Mailgun](https://www.mailgun.com) account and make a note of your API key.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Create your form like so:

```html
<form action="https://{YOUR_APP_NAME}.herokuapp.com">
  Email: <input type="text" name="name"><br>
  Name: <input type="text" name="email"><br>
  Message: <textarea name="message" cols="40" rows="5"></textarea>
  <input type="submit" value="Send Message">
</form> 
```

