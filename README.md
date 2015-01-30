Quickstart contact form processing
----------------------------------

This will be useful if...

* You want to forward a simple contact form to your email
* You have a (S3) static site and don't want to run a server

Usage
-----

Register your email:

```bash
    $ curl --data "email=<your_email>" https://fwdform.herokuapp.com/register
    Token: 780a8c9b-dc2d-4258-83af-4deefe446dee
    
```

Test (optional):

```bash
    $ curl --data "email=person@form.com&name=person&message=hello" \
           https://fwdform.herokuapp.com/user/<token>
```

Put into action:

```html
<form action="https://fwdform.herokuapp.com/user/<token>">
  Email: <input type="text" name="name"><br>
  Name: <input type="text" name="email"><br>
  Message: <textarea name="message" cols="40" rows="5"></textarea>
  <input type="submit" value="Send Message">
</form> 
```

NB: Required parameters are: `email`, `name` and `message`. Other parameters will be ignored.

Privacy concerns?
-----------------

Spin up your own free [Heroku](http://www.heroku.com) instance. A [Mandrill](http://mandrill.com) account required for email delivery.

```bash
    $ git clone https://github.com/samdobson/fwdform.git
    $ heroku create
    $ heroku config:set MANDRILL_API_KEY=<KEY>
    $ heroku addons:add heroku-postgresql:dev
    $ heroku pg:promote HEROKU_POSTGRESQL_COLOR
    $ heroku ps:scale web=1
```

Deploy the application to your Heroku instance.

```bash
    $ git push heroku master
```

Create the database.

```bash
    $ heroku run python
    >>> from app import db
    >>> db.create_all()
    >>> exit()
```

