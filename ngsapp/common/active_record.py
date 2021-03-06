from flask_restful import abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ngsapp.ext import db


class ActiveRecord:
    def save(self, **kwargs):
        try:
            db.session.add(self)
            db.session.commit()
            # kwargs.update({'id': self.id})
            return {'data': kwargs}
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            return abort(500, )

            # return {'msg': 'Something bad happened'}, 500

    def delete(self, **kwargs):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return abort(500, )
