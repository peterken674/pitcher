from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Category, Pitch, Comment
import click
from flask.cli import with_appcontext

# Creating app instance.
app = create_app("production")

manager = Manager(app)
manager.add_command('server', Server)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app = app, db = db, User = User, Category = Category, Pitch = Pitch, Comment = Comment)

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()


if __name__ == '__main__':
    manager.run()