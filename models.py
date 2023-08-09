from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    group = db.Column(db.String)
    is_client = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)

    # Relationships
    fees = db.relationship('Fees', backref='user_relation', lazy=True)  # Change the backref name
    documents = db.relationship('Document', backref='user_relation', lazy=True)
    cases = db.relationship('Case', backref='user_relation', lazy=True)
    @staticmethod
    def find_by_name(name):
        return User.query.filter_by(name=name).first()

    @classmethod
    def find_by_group(cls, group_name):
        return cls.query.filter_by(group=group_name).all()

    def get_role_name(self):
        return self.role.name if self.role else None

    def get_fees_total(self):
        return sum([fee.amount for fee in self.fees])

    def get_document_count(self):
        return len(self.documents)

    def get_case_count(self):
        return len(self.cases)

    def validate(self):
        if not self.name:
            raise ValueError("Name is required")


class Fees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record = db.Column(db.Integer)
    file_reference = db.Column(db.String)
    clients_reference = db.Column(db.String)
    case_no_or_parties = db.Column(db.String)
    deposit_fees = db.Column(db.Integer)
    final_fees = db.Column(db.Integer)
    deposit_pay = db.Column(db.Integer)
    final_pay = db.Column(db.Integer)
    outstanding = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    deposit = db.Column(db.Integer)

    # Relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    @staticmethod
    def find_by_reference(reference):
        return Fees.query.filter_by(file_reference=reference).all()

    def get_total_fees(self):
        return self.deposit_fees + self.final_fees

    def get_total_pay(self):
        return self.deposit_pay + self.final_pay

    def get_balance(self):
        return self.get_total_fees() - self.get_total_pay()

    from sqlalchemy import or_

    @classmethod
    def search(cls, **kwargs):
        query = cls.query  # Initialize the base query to select all records
        filters = []       # List to store individual filter conditions

        for field, value in kwargs.items():
            if hasattr(cls, field):  # Check if the field exists in the model
                # Check if the field is a string column
                if isinstance(getattr(cls, field).type, db.String):
                    # Add ilike filter for case-insensitive partial string match
                    filters.append(getattr(cls, field).ilike(f"%{value}%"))
                else:
                    # Add equality filter for non-string fields
                    filters.append(getattr(cls, field) == value)

        if filters:
            # Apply OR conditions to the filters
            query = query.filter(or_(*filters))

        return query.all()  # Execute the query and return the results

    def validate(self):
        if not self.file_reference:
            raise ValueError("File reference is required")


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
   

    def validate(self):
        if not self.name:
            raise ValueError("Document name is required")


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  

    def validate(self):
        if not self.description:
            raise ValueError("Case description is required")
