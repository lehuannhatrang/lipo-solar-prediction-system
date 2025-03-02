from datetime import datetime
from flask import request
from flask_restful import Resource
from flasgger import swag_from
from models.user_license import UserLicense, UserLicenseStatus
from models import db
from middlewares import require_authentication

class UserLicenseResource(Resource):
    @swag_from("../swagger/user_license/GET.yml")
    @require_authentication
    def get(self, email):
        """Get user license by email"""
        try:
            user_license = UserLicense.get_by_email(email)
            if not user_license:
                return {"message": "User license not found"}, 404
                
            return user_license.to_dict(), 200
        except Exception as e:
            return {"message": f"Error retrieving user license: {str(e)}"}, 500

    @swag_from("../swagger/user_license/PUT.yml")
    @require_authentication
    def put(self, email):
        """Update user license status"""
        try:
            data = request.get_json()
            if not data or 'status' not in data:
                return {"message": "Status is required"}, 400

            # Validate status
            try:
                new_status = UserLicenseStatus(data['status'])
            except ValueError:
                return {"message": f"Invalid status. Must be one of: {[s.value for s in UserLicenseStatus]}"}, 400

            user_license = UserLicense.get_by_email(email)
            if not user_license:
                return {"message": "User license not found"}, 404

            # Update status and optionally expired_ts
            user_license.status = new_status
            if 'expired_ts' in data:
                try:
                    user_license.expired_ts = datetime.fromisoformat(data['expired_ts'])
                except ValueError:
                    return {"message": "Invalid expired_ts format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}, 400

            db.session.commit()
            return user_license.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating user license: {str(e)}"}, 500

class UserLicenseListResource(Resource):
    @require_authentication
    def get(self):
        """Get all user licenses"""
        try:
            user_licenses = UserLicense.query.all()
            return [license.to_dict() for license in user_licenses], 200
        except Exception as e:
            return {"message": f"Error retrieving user license: {str(e)}"}, 500

    @swag_from("../swagger/user_license/POST.yml")
    def post(self):
        """Create new user license"""
        try:
            data = request.get_json()
            if not data or 'email' not in data:
                return {"message": "Email is required"}, 400

            # Check if license already exists
            existing_license = UserLicense.get_by_email(data['email'])
            if existing_license:
                return {"message": "User license already exists"}, 409

            # Create new license
            new_license = UserLicense(
                email=data['email'],
                user_id=data.get('user_id'),
                expired_ts=datetime.fromisoformat(data['expired_ts']) if 'expired_ts' in data else None,
                status=UserLicenseStatus(data['status']) if 'status' in data else UserLicenseStatus.INACTIVE
            )

            db.session.add(new_license)
            db.session.commit()

            return new_license.to_dict(), 201
        except ValueError as e:
            db.session.rollback()
            return {"message": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error creating user license: {str(e)}"}, 500
