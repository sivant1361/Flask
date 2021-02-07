from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager,UserMixin,login_required,login_user,logout_user,current_user,login_required
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_BINDS']={
    'login':'sqlite:///login.db'
}

db=SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    __bind_key__='login'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
    password=db.Column(db.String(100))

@login_manager.user_loader
def get(id):
    return User.query.get(id)

class TODO(db.Model):
    num=db.Column(db.Integer,primary_key=True)
    todo=db.Column(db.Text,nullable=False)
    start=db.Column(db.Text,nullable=False,default=str(datetime.utcnow))
    end=db.Column(db.Text,nullable=False,default=str(datetime.utcnow))

    def __repr__(self):
        return "Num: "+str(self.num)

todo1=[
    {
        "name":"1st name",
        "todo":"1st todo"
    },
    {
        "name":"2nd name",
        "todo":"2nd todo"
    }
]

@app.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method=="POST":
        post_todo=request.form['todo']
        post_start=request.form['start']
        post_end=request.form['end']

        db.session.add(TODO(todo=post_todo,start=post_start,end=post_end))
        db.session.commit()
        return redirect('/')
    else:
        todo1=TODO.query.all()
        return render_template('home.html',Name="Home",Todo=todo1)

@app.route('/about')
@login_required
def about():
    return render_template('about.html',Name="About")

@app.route('/delete/<int:num>')
@login_required
def delete(num):
    post_delete=TODO.query.get_or_404(num)
    db.session.delete(post_delete)
    db.session.commit()
    return redirect('/')

@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login_post():
    username=request.form['username']
    password=request.form['password']
    user=User.query.filter_by(username=username).first()
    login_user(user)
    return redirect('/')

@app.route('/logout')
def log_out():
    logout_user()
    return redirect('/login')

# @app.route('/<int:a>/<int:b>')
# def manual(a,b):
#     return "<h1>Answer: "+str(a+b)+"</h1>"

if __name__=="__main__":
    app.run(debug=True)