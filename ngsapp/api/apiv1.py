from flask import Blueprint
from flask_restplus import Api

from ngsapp.resources.kyc import ns_kyc
from ngsapp.resources.notification import ns_notify
from ngsapp.resources.project import ns_project
from ngsapp.resources.project_comment import ns_proj_comment
from ngsapp.resources.project_files import ns_proj_files
from ngsapp.resources.protected import protected
from ngsapp.resources.tag import ns_tag
from ngsapp.resources.task import ns_task
from ngsapp.resources.team import ns_team
from ngsapp.resources.ticket import ns_ticket
from ngsapp.resources.ticket_comment import ns_ticket_comments
from ngsapp.resources.users import ns_user
from ngsapp.security import auth

bapi = Blueprint('api', __name__, url_prefix='/api')
api = Api(bapi, title='Ngsapp')

api.add_namespace(auth)
api.add_namespace(ns_kyc)
api.add_namespace(ns_notify)
api.add_namespace(ns_project)
api.add_namespace(ns_proj_comment)
api.add_namespace(ns_proj_files)
api.add_namespace(ns_user)
api.add_namespace(protected)
api.add_namespace(ns_tag)
api.add_namespace(ns_task)
api.add_namespace(ns_ticket)
api.add_namespace(ns_ticket_comments)
api.add_namespace(ns_team)
