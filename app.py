import os
import json
import unittest
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Patient, Doctor
from auth import AuthError, requires_auth

Doctors_PER_PAGE = 5


def paginate_doctor(request, allDoctors):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * Doctors_PER_PAGE
    end = start + Doctors_PER_PAGE

    doctors = [i.format() for i in allDoctors]
    current_doctors = doctors[start:end]

    return current_doctors


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return jsonify({
            "success": True,
            "Project": "Welcome to Capstone Project!",
        })

    # ---------------------------------------------------------------------------------
    # Doctors
    # ---------------------------------------------------------------------------------

    # get all doctors with their info

    @app.route('/doctors', methods=['GET'])
    @requires_auth('get:doctors')
    def show_doctors(payload):
        allDoctors = Doctor.query.all()
        theDoctor = paginate_doctor(request, allDoctors)

        return jsonify({
            'success': True,
            'doctors': theDoctor
        })

    # Post a doctor

    @app.route('/doctors', methods=['POST'])
    @requires_auth('post:doctor')
    def new_doctor(payload):
        try:
            body = request.get_json()
            new_doctor = Doctor(name=body['name'],
                                deparment=body['deparment'],
                                level=body['level'])

            new_doctor.insert()
            return jsonify({
                'success': True,
                'doctor': new_doctor.format()
            })

        except Exception:
            abort(422)

    # Delete a doctor
    @app.route('/doctors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:doctor')
    def delete_doctor(payload, id):

        try:
            doctors = Doctor.query.filter(Doctor.id == id).one_or_none()
            if doctors is None:
                abort(404)

            doctors.delete()

            return jsonify({
                'success': True,
                'Deleted doctor': id})

        except Exception:
            abort(422)

    # Patch a doctor
    @app.route('/doctors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:doctor')
    def patch_doctor(payload, id):

        body = request.get_json()

        doctors = Doctor.query.filter(Doctor.id == id).one_or_none()

        doctors.name = body['name']
        doctors.deparment = body['deparment']
        doctors.level = body['level']

        doctors.update()

        return jsonify({
            'success': True,
            'updated doctor': doctors.format()})

    # ---------------------------------------------------------------------------------
    # Patient
    # ---------------------------------------------------------------------------------

    # get all Patient with their info

    @app.route('/patient', methods=['GET'])
    @requires_auth('get:patient')
    def show_patient(payload):

        patients = Patient.query.all()

        data = []
        for x in patients:
            data.append(x.format())

        return jsonify({
            'success': True,
            'patients': data
        })

    # Post a Patient
    @app.route('/patient', methods=['POST'])
    @requires_auth('post:patient')
    def new_patient(payload):
        try:

            body = request.get_json()
            new_patient = Patient(name=body['name'],
                                  age=body['age'],
                                  gender=body['gender'],
                                  doctor_id=body['doctor_id'],
                                  date_of_appointment=body[
                                      'date_of_appointment']
                                  )

            new_patient.insert()
            return jsonify({
                'success': True,
                'patient': new_patient.format()
            })

        except Exception:
            abort(422)

    # Delete a Patient
    @app.route('/patient/<int:id>', methods=['DELETE'])
    @requires_auth('delete:patient')
    def delete_Patient(payload, id):
        try:

            patient = Patient.query.filter(Patient.id == id).one_or_none()

            if patient is None:
                abort(404)

            patient.delete()

            return jsonify({
                'success': True,
                'Deleted patient': id})

        except Exception:
            abort(422)

    # Patch a patient

    @app.route('/patient/<int:id>', methods=['PATCH'])
    @requires_auth('patch:patient')
    def patch_patient(payload, id):

        body = request.get_json()

        patient = Patient.query.filter(Patient.id == id).one_or_none()

        patient.name = body['name']
        patient.age = body['age']
        patient.gender = body['gender']
        patient.doctor_id = body['doctor_id']
        patient.date_of_appointment = body['date_of_appointment']

        patient.update()

        return jsonify({
            'success': True,
            'updated patient': patient.format()})

    # Error Handling

    @ app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @ app.errorhandler(404)
    def not_found(error):

        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @ app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "Bad Request"
        }), 400

    @ app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            "success": False,
            "error": "medd",
            "message": e.error,
            "code": e.status_code
        }), e.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
