from marshmallow import Schema, fields, validate, validates, ValidationError


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1))
    group = fields.String()
    is_client = fields.Boolean()
    is_admin = fields.Boolean()
    fees = fields.Nested('FeesSchema', many=True, exclude=('user',))
    documents = fields.Nested('DocumentSchema', many=True, exclude=('user',))
    cases = fields.Nested('CaseSchema', many=True, exclude=('user',))

    @validates('name')
    def validate_name(self, value):
        if not value:
            raise ValidationError('Name is required')


class FeesSchema(Schema):
    id = fields.Integer(dump_only=True)
    record = fields.Integer()
    file_reference = fields.String(validate=validate.Length(min=1))
    clients_reference = fields.String()
    case_no_or_parties = fields.String()
    deposit_fees = fields.Integer()
    final_fees = fields.Integer()
    deposit_pay = fields.Integer()
    final_pay = fields.Integer()
    outstanding = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deposit = fields.Integer()
    user_id = fields.Integer(dump_only=True)
    user = fields.Nested(UserSchema, exclude=('fees', 'documents', 'cases'))

    @validates('file_reference')
    def validate_file_reference(self, value):
        if not value:
            raise ValidationError('File reference is required')


class DocumentSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    user = fields.Nested(UserSchema, exclude=('fees', 'documents', 'cases'))

    @validates('name')
    def validate_name(self, value):
        if not value:
            raise ValidationError('Document name is required')


class CaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    user = fields.Nested(UserSchema, exclude=('fees', 'documents', 'cases'))

    @validates('description')
    def validate_description(self, value):
        if not value:
            raise ValidationError('Case description is required')


user_schema = UserSchema()
fees_schema = FeesSchema()
document_schema = DocumentSchema()
case_schema = CaseSchema()
