import werkzeug
from flask_jwt_extended import current_user, jwt_required
from flask_restplus import Resource, fields
from flask_restplus.reqparse import RequestParser

from backend import api, pagination
from backend.common import ProtectedDirField
from backend.models import Project, ProjectFile
from backend.resources.project import project_schema
from backend.utils import delete_file, file_upload

project_files_schema = api.model('ProjectFiles', {
    'id': fields.Integer(),
    'project': fields.Nested(project_schema),
    'attached_file': ProtectedDirField(),
    'description': fields.String()
})


class ProjectFileResource(Resource):
    method_decorators = [jwt_required]

    @api.marshal_with(project_files_schema, envelope='data')
    def get(self, uuid, pk):
        if current_user.role == 'CLIENT':
            project = current_user.projects.filter_by(uuid=uuid).first_or_404()
            return project.files.filter_by(id=pk).first_or_404()
        proj = Project.query.filter_by(uuid=uuid).first_or_404()
        return proj.files.filter_by(id=pk).first_or_404()

    def delete(self, uuid, pk):
        if current_user.role == 'CLIENT':
            project = current_user.projects.filter_by(uuid=uuid).first_or_404()
            file = project.files.filter_by(id=pk).first_or_404()
            delete_file(file.attached_file)
            return file.delete(), 202
        proj = Project.query.filter_by(uuid=uuid).first_or_404()
        file = proj.files.filter_by(id=pk).first_or_404()
        delete_file(file.attached_file)
        return file.delete(), 202


xparser = RequestParser(bundle_errors=True, trim=True)
xparser.add_argument('files', required=True, location='files', type=werkzeug.datastructures.FileStorage,
                     action='append')
xparser.add_argument('description', required=True, location='form', type=str)


class ProjectFileResourceList(Resource):
    method_decorators = [jwt_required]

    def get(self, uuid):
        project_files_schema.pop('project')
        if current_user.role == 'CLIENT':
            fil = current_user.projects.filter_by(uuid=uuid).first_or_404()
            return pagination.paginate(fil.files, schema=project_files_schema)

    def post(self, uuid):
        args = xparser.parse_args(strict=True)
        project = current_user.projects.filter_by(uuid=uuid).first_or_404()
        for file in args.files:
            data = file_upload(file)
            if data.get('error'):
                return data, 400
        for file in args.files:
            data = file_upload(file, )
            data.get('upload').save(data.get('full_path'))
            project.files.append(ProjectFile(attached_file=data.get('filename'), description=args.description))
        return project.save(), 202