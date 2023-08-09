import os
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
# imports from models
from models import db, User, Fees, Document, Case
from serealizers import fees_schema, user_schema, document_schema, case_schema
# app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# config
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fees.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SESSION_COOKIE_SECURE'] = True
app.config["JWT_SECRET_KEY"] = "super-zombie5$45secret"
app.config['SECURITY_PASSWORD_SALT'] = 'your-password-salt'


# middlewares
jwt = JWTManager(app)
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)


# login logic
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.user_id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from models import User
    identity = jwt_data["sub"]
    return User.query.filter_by(user_id=identity).one_or_none()


# user
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user_schema.dump(user)

    def patch(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        data = request.get_json()
        if 'name' in data:
            user.name = data['name']
        if 'group' in data:
            user.group = data['group']
        if 'is_client' in data:
            user.is_client = data['is_client']
        if 'is_admin' in data:
            user.is_admin = data['is_admin']

        db.session.commit()
        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 204


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return user_schema.dump(users, many=True)

    def post(self):
        data = request.get_json()
        new_user = User(**data)

        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201

# Fees resource


class FeesResource(Resource):
    def get(self, fees_id):
        fees = Fees.query.get(fees_id)
        if not fees:
            return {'message': 'Fees not found'}, 404
        return fees_schema.dump(fees)

    def patch(self, fees_id):
        fees = Fees.query.get(fees_id)
        if not fees:
            return {'message': 'Fees not found'}, 404

        data = request.get_json()
        if 'deposit_fees' in data:
            fees.deposit_fees = data['deposit_fees']
        if 'final_fees' in data:
            fees.final_fees = data['final_fees']
        if 'deposit_pay' in data:
            fees.deposit_pay = data['deposit_pay']
        if 'final_pay' in data:
            fees.final_pay = data['final_pay']

        db.session.commit()
        return fees_schema.dump(fees)

    def delete(self, fees_id):
        fees = Fees.query.get(fees_id)
        if not fees:
            return {'message': 'Fees not found'}, 404

        db.session.delete(fees)
        db.session.commit()
        return {'message': 'Fees deleted'}, 204


class FeesListResource(Resource):
    def get(self):
        fees = Fees.query.all()
        return fees_schema.dump(fees, many=True)

    def post(self):
        data = request.get_json()
        new_fees = Fees(**data)

        db.session.add(new_fees)
        db.session.commit()

        return fees_schema.dump(new_fees), 201
# Document resource


class DocumentResource(Resource):

    def get(self, document_id):
        document = Document.query.get(document_id)
        if not document:
            return {'message': 'Document not found'}, 404
        return document_schema.dump(document)


class CaseResource(Resource):

    def get(self, case_id):
        case = Case.query.get(case_id)
        if not case:
            return {'message': 'Case not found'}, 404
        return case_schema.dump(case)


# Add the resources to the API

api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(FeesResource, '/fees/<int:fees_id>')

api.add_resource(FeesListResource, '/fees')
api.add_resource(DocumentResource, '/document/<int:document_id>')
api.add_resource(CaseResource, '/case/<int:case_id>')

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5500)
