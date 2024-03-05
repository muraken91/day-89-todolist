from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Date
from form import TodoForm
import os


# Setting up Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
ckeditor = CKEditor(app)
Bootstrap5(app)


# Setting up Database
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///todo.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# To-do Table Configuration
class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    task: Mapped[str] = mapped_column(String(250), nullable=False)
    due_date: Mapped[str] = mapped_column(Date, nullable=False)
    priority: Mapped[str] = mapped_column(String(250), nullable=False)
    status: Mapped[str] = mapped_column(String(250), nullable=False)
    type: Mapped[str] = mapped_column(String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


# Create Routes
@app.route("/", methods=["GET", "POST"])
def home():
    result = db.session.execute(db.select(Todo))
    tasks = result.scalars().all()
    return render_template("index.html", all_tasks=tasks)


@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    form = TodoForm()
    if form.validate_on_submit():
        new_task = Todo(
            task=form.task.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            status=form.status.data,
            type=form.type.data,
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-task.html", form=form)


@app.route("/change-status/<int:task_id>", methods=["GET", "POST"])
def change_status(task_id):
    task = db.get_or_404(Todo, task_id)
    new_status = request.form.get("new_status")
    task.status = new_status
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = db.get_or_404(Todo, task_id)
    edit_form = TodoForm(
        task=task.task,
        due_date=task.due_date,
        priority=task.priority,
        status=task.status,
        type=task.type,
    )
    if edit_form.validate_on_submit():
        task.task = edit_form.task.data
        task.due_date = edit_form.due_date.data
        task.priority = edit_form.priority.data
        task.status = edit_form.status.data
        task.type = edit_form.type.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-task.html", form=edit_form, is_edit=True)


@app.route("/delete-task/<int:task_id>", methods=["GET", "POST"])
def delete_task(task_id):
    task = db.get_or_404(Todo, task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
