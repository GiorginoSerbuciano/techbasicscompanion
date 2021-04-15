# Tech Basics Companion v0.1.0-alpha

_This project is built from scratch, following CoreyMS's Flask-SQLAlchemy tutorial series. You can find these code snippets [forked on my GitHub profile](https://github.com/GiorginoSerbuciano/code_snippets/tree/master/Python/Flask_Blog)._

Before starting work on TBCOMP, I had been planning to repurpose one of my other applications, DesktopSort, into a Python code analyser/file manipulation software, but I ultimately decided against that for the following reasons:
1. Around the time that I wanted to start developing my next application, I began using VS Code again. Very quickly, I discovered that it had all the features I had been planning to implement, and it did so much better than I ever could have;
2. Developing software that manipulates system files implies security risks;
3. I was given the opportunity to work on the collaborative and social project that TBCOMP is purposed to become.
4. Creating a website is a very intricate visual and logical challenge. This threw me into the deep end of the Flask-SQLAlchemy library.

Starting off, I had a very vague clue about how one might design a website using Python. I had had some positive experiences using Flask in class that I felt very good about because I was naive enough to believe that I knew what I was doing. I had also understood objects and classes and I had become familiar with Python syntax and imports to a good enough degree that I did not meet any substantial difficulties in any of these domains.

The difficulties, of course, started where my competences ended. Knowing how to build routes and create simple Jinja templates is one thing; but Flask-SQLAlchemy introduces a whole new wonderful layer of database interaction. Coupled with WTForms for user input and Bootstrap for functionally-styled templates, the task of creating this website got complicated almost instantaneously. 

What made it particularly difficult getting started is that the documentation for Flask-SQLAlchemy assumes a good grasp of SQLAlchemy&mdash;which I did not have&mdash;so it only describes how _some_ SQLAlchemy principles translate into Flask-SQLAlchemy, and only very broadly so. Because of my lack of experience, I was often unable to translate documentation into my very specific use-case; as always, there is hardly a how-to available on the internet for every single scenario.

Luckily, [@CoreyMSchafer](https://github.com/CoreyMSchafer) had made a tutorial series on Flask-SQLAlchemy (available [on YouTube](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)) where he goes through the process of creating a whole blog from the first lines of code all the way to deployment. I followed this tutorial along, step by step, until I was able to "take my own flight", figuratively speaking, and make my own additions and modifications to the structure of the project. Naturally, I wanted this project to be fit for its purpose, and while Corey's final product is a blog, this website only implements some blog-like features&mdash;otherwise, it could've just as well been a fork of Corey's.

At first, the use of SQLAlchemy seemed superfluous, and having had some experience using SQLite, I considered "swapping out" the SQLAlchemy elements with SQLite. In hindsight, I am glad I gave up on the idea because I now realize that implementing SQLite back into Flask would've caused me more trouble that it would've spared me. After getting used to the way FLask-SQLALchemy works, I realized that it's actually very neat&mdash;even neater than regular SQLAlchemy! This is mostly thanks to the fact that database tables are defined as classes, while its rows can be instantiated as objects, which is an advantage I would've lost had I used SQLite instead.

As useful as Flask-SQLAlchemy turned out to be, it was also very challenging to debug. One issue I had early on, for example, is that running the site wouldn't build a database file if one didn't exist. This meant I had to build it myself a couple of times, but this was obviously not viable for an efficient development environment, let alone for deploying into production. I wasn't able to fix this until much later on with a simple but non-obvious [modification](https://github.com/GiorginoSerbuciano/techbasicscompanion/commit/8d396e14ab60fd6ea5b781a4653742a8b1a61050) to main.py.

Of all the frameworks this website uses, I found Jinja templating to be the simplest, but also the most constrictive. One problem I came across was creating a drop-down list of tags, which happened somewhere between [the 25th](a90cd1d5b8c3dfebe36ae6a574fb7dce647a4013) and [the 27th](2beee7e2120e7cb6a0d72ad76811c0b079db4986) of Feburary, 2021. Not knowing that Flask can take care of that for me, I tried using some mind-twisting iterators to generate a drop-down entry for each item in a list of tags inside of the Jinja template... This was simply a non-starter, until I looked into how one might create a proper drop-down list. The result was the following code:

```
	<select>
		{% for tag in form.tag %}
			<option value="{{tag}}">{{tag}}</option>
		{% endfor %}
	</select>
```
Putting aside that this made each entry appear twice in the drop-down list, it seemed to work, but it only _seemed_ to: I had fixed the Jinja-related problem of creating a drop-down field, but the Flask-WTForms it represented was failing silently. At first glance, it looks like it is a drop-down based on the options of a form. It turned out that the error was to take the drop-down field's options from `ProjectForm.dropdown_tags` rather than `ProjectForm.tag`. The catch is that `ProjectForm.dropdown_tags` is not a `wtforms.fields.core.SelectField` class attributed to `class ProjectForm(FlaskForm)`, but is simply a list of the choices to be displayed by the `ProjectForm.tag` field, which is a `SelectField`. Essentially, `<option value="{{tag}}">{{tag}}</option>` doesn't return any data to `ProjectForm.tag`, which meant that the form was not validating despite all entries appearing to be fulfilled.

It turns out that silent failures are actually very easy to cause in WTForms; not because it isn't working well, but because it's working too well. For example, it took me a while to understand the distinctions between:

object | role
------------ | -------------
`FormName.field_name.data` | The data returned from field `field_name` from form `FormName`, seen from outside the context of the form.
`field_name.data` | The data returned from field `field_name`, seen from inside the context of a form.
`field_name` | The field entity.
`FieldType('Field_Name')` | The type and label of the field, which determines how the field is displayed in HTML.

Before I got the hang of it, I mixed these up quite a couple of times, breaking the form-route-database information transfer errorlessly.

Nevertheless, Flask-WTForms is very elegant. As far as I can tell, this is what the basic structure of a form looks like:

```

	class FormName(FlaskForm):

		field_name = FieldType('Field_Name', validators = [ValidatorOne(), ValidatorTwo()]
		submit = SubmitField('SubmitText')
    
		def custom_validator(self, field_one):
			<condition>:
				raise ValidationError('ErrorText')
```

Validators are also very smoothly implemented; not only the pre-existing set, but defining custom validators. One of the most useful validators that I have used in this project uses this conditional pattern:

```
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is already in use.')
```

Admittedly, this isn't much of a deviation from Corey's version, but it's kind of beautiful in its simplicity nevertheless. My favourite validator&mdash;which I did have to design myself&mdash;is a validator that checks if a https://github.com URL is being assigned to `ProjectForm.github_repo` _and_ that this GitHub repo is not already being used by a different project:

```
	def validate_github_repo(self, github_repo):
		project = Project.query.filter_by(github_repo=github_repo.data).first()
		if project:
			raise ValidationError('This GitHub repository is linked to a different project. Please update the already-existing project if you are a contributor.')
		elif parse.scheme != 'https' or parse.netloc != 'github.com':	#security: raise error if not secure http
			raise ValidationError('Invalid URL.')
```
This one was so exiciting because it worked with such precision despite being a shot in the dark.

Another challenge was Bootstrap. As versatile as it might be, I wanted to make some changes to some of the styles it provided, but none of the changes that I coded in `main.css` showed up in my webpages and I couldn't figure out why. As I learned from [this thread](https://stackoverflow.com/a/27704409/13841237), I fixed this by increasing the specificity of my styless in order to override Bootstrap's. Everything else was down to me learning a bit of HTML and CSS on the fly (and occasionally "cheating" using Firefox Mozilla's font controls in the element inspector :>).

Not all problems were equally educative. I had set up the password reset email system ([4cee86f]) perfectly, yet to my frustration, it wasn't sending any emails when I requested a password reset. It took me two whole hours to debug this; I'll spare you the pain of scanning through the entire project in search of the bug, but see if you can find it:

```
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
	app.config['MAIL_SERVER'] = 'smtp.gmail.com'
	app.config['MAIL_POST'] = 587
	app.config['MAIL_USE_TLS'] = True
	app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
	app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

```

A brief note on using GitHub: If you look at the commits on the project, you'll notice that my interaction with GitHub got more sophisiticated at some point in March. This is when I figured out how pushing, pulling, stashing, branching, etc. all work, so I've been using them to the greatest extent that I can. It's actually turning out to be very useful in a number of ways, the most important of which is that I can now commit changes very precisely; I sometimes commit one file at a time if the change I have made is significant only to that file. I'm also getting into the habit of creating issues and working on branches. All of this helps me navigate the project's history much quicker&mdash;which also makes it easier to document&mdash;and lets me reverse experimentation on one file without reversing what already worked well in 50 others.

I would like to look at a very recent example of an issue that really stretched my nerves, namely #8 Project creators cannot set contributors. In this issue, I dealt with many-to-many relationships between Flask-SQLAlchemy models for the first time. I'm going to use a slash to mirror the task: The task was to assign users as contributors to projects,/and to assign projects with contributors which were users. The left side of the slash was necessary in order to allow multiple users to be contributors of projects, while the right side allows projects to keep a record of which users are contributing to it for look-up purposes. The reason why I want to attribute multiple contributors to each project (and not just one author) is because, first of all, it's not impossible that more than one person works on a project&mdash;it's actually quite common in Tech Basics seminars, as it turns out&mdash;, so I want multiple people to be able to create posts on the project's page (yet to be implemented) and to edit projects (I have not yet figured out what the privileges of a project admin should be, if any).

Let me give you an overview of my classes:

```
	class User(db.Model):
		__tablename__='user'
```

id | username | email | image_file | password | is_admin
------------ | ------------- | ------------- | ------------- | ------------- | -------------
INT PK | STRING(20) UNIQUE NOT NULL | STRING(120) UNIQUE NOT NULL | STRING(20) NOT NULL DEFAULT='default.jpg' | STRING(60) NOT NULL | BOOL

```
	class Post(db.Model):
		__tablename__='post'
```

id | title | date | content | author_id | project_id
------------ | ------------- | ------------- | ------------- | ------------- | -------------
INT PK | STRING(120) NOT NULL | DATETIME NOT NULL DEFAULT=datetime.utcnow | TEXT NOT NULL | INT FK('user.id') NOT NULL | INT FK('project.id') NOT NULL

```
	class Project(db.Model):
		__tablename__='project'
```

id | title | date | content | github_repo | admin_id | tag
------------ | ------------- | ------------- | ------------- | ------------- | ------------- | -------------
INT PK | STRING(120) NOT NULL | DATETIME NOT NULL DEFAULT=datetime.utcnow | TEXT NOT NULL | STRING(120) NOT NULL UNIQUE | INT FK('user.id') NOT NULL | STRING NOT NULL


