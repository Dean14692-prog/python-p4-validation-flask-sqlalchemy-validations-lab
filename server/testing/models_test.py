import pytest
from app import app, db
from models import Author
from sqlalchemy.exc import IntegrityError

class TestAuthor:

    def test_requires_name(self):
        '''requires each record to have a name.'''
        with app.app_context():
            db.create_all()
            db.session.query(Author).delete()
            db.session.commit()

            with pytest.raises(ValueError):
                author = Author(name=None, phone_number='1234567890')
                db.session.add(author)
                db.session.commit()

    def test_requires_unique_name(self):
        '''requires each record to have a unique name.'''
        with app.app_context():
            db.create_all()
            db.session.query(Author).delete()
            db.session.commit()

            author_a = Author(name='Ben', phone_number='1231144321')
            db.session.add(author_a)
            db.session.commit()

            author_b = Author(name='Ben', phone_number='1231144321')
            db.session.add(author_b)

            # Expect an IntegrityError because name must be unique
            with pytest.raises(IntegrityError):
                db.session.commit()
            db.session.rollback()

    def test_phone_number_validation(self):
        '''requires phone number to be 10 digits.'''
        with app.app_context():
            db.create_all()
            db.session.query(Author).delete()
            db.session.commit()

            with pytest.raises(ValueError):
                author = Author(name='Alice', phone_number='12345')
                db.session.add(author)
                db.session.commit()
