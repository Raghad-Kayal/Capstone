import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from app import create_app
from models import setup_db, Patient, Doctor


class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "hospital_test"
        self.database_path = "postgres://{}@{}/{}".format(
            'postgres:111', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_doctor = {
            'name': 'raghad',
            'deparment': 'Pediatric Surgery',
            'level': 'Consultant'
        }

        self.update_doctor = {
            'name': 'raghad kayal',
            'deparment': 'Pediatric Surgery',
            'level': 'Consultant'
        }

        self.new_patient = {
            'name': 'raghad',
            'age': 24,
            'gender': 'female',
            'doctor_id': 3,
            'date_of_appointment': '2021-01-13'
        }

        self.update_patient = {
            'name': 'raghad',
            'age': 25,
            'gender': 'female',
            'doctor_id': 3,
            'date_of_appointment': '2021-01-13'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # self.db.drop_all()
            # create all tables
            # self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # ----------------------------------------------
    # GET doctor test for success and fail
    # ----------------------------------------------

    def test_get_doctor(self):
        # Insert dummy doctor into database.
        n_doctor = Doctor(name='Leonardo Di Caprio',
                          deparment='Pediatric Surgery', level='Consltant')
        n_doctor.insert()
        res = self.client().get(
            '/doctors', headers={'Authorization': 'Bearer ' + TOKEN})
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['doctors'])

    def test_fail_get_doctor(self):
        # Insert dummy doctor into database.
        n_doctor = Doctor(name='Leonardo Di Caprio',
                          deparment='Pediatric Surgery', level='Consltant')
        n_doctor.insert()
        res = self.client().get(
            '/doctors/1', headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    # ----------------------------------------------
    # GET patient test for success and fail
    # ----------------------------------------------

    def test_get_patient(self):
        # Insert dummy patient into database.
        n_patient = Patient(name='leen', age=18, gender='female',
                            doctor_id=3, date_of_appointment='2021-01-13')
        n_patient.insert()
        res = self.client().get(
            '/patient', headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['patients'])

    def test_fail_get_patient(self):
        # Insert dummy patient into database.
        n_patient = Patient(name='leen', age=18, gender='female',
                            doctor_id=3, date_of_appointment='2021-01-13')
        n_patient.insert()
        res = self.client().get(
            '/patient/1', headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    # ----------------------------------------------
    # POST NEW doctor test for success and fail
    # ----------------------------------------------

    def test_post_new_doctor(self):
        res = self.client().post('/doctors', json=self.new_doctor,
                                 headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['doctor']['name'])
        self.assertTrue(data['doctor']['deparment'])
        self.assertTrue(data['doctor']['level'])

    def test_fail_post_new_doctor(self):
        res = self.client().post('/doctors/1/doctor', json=self.new_doctor,
                                 headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # ----------------------------------------------
    # POST NEW patient test for success and fail
    # ----------------------------------------------
    def test_post_new_patient(self):
        res = self.client().post('/patient', json=self.new_patient,
                                 headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['patient']['name'])
        self.assertTrue(data['patient']['age'])
        self.assertTrue(data['patient']['gender'])
        self.assertTrue(data['patient']['doctor_id'])
        self.assertTrue(data['patient']['date_of_appointment'])

    def test_fail_post_new_patient(self):
        res = self.client().post('/patient/1/doctor', json=self.new_patient,
                                 headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # ----------------------------------------------
    # DELETE a doctor test for success and fail
    # ----------------------------------------------

    def test_delete_doctor(self):

        # Insert a dummy doctor to database.
        n_doctor = Doctor(name='Leonardo Di Caprio',
                          deparment='Pediatric Surgery', level='Consltant')
        n_doctor.insert()

        res = self.client().delete('/doctors/%s' % (n_doctor.id),
                                   headers={'Authorization': 'Bearer ' + TOKEN}
                                   )
        data = json.loads(res.data)

        doctors = Doctor.query.filter(Doctor.id == n_doctor.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Deleted doctor'])
        self.assertEqual(data['Deleted doctor'], n_doctor.id)
        self.assertEqual(doctors, None)

    def test_fail_delete_doctor(self):
        res = self.client().delete(
            '/doctors/111', headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # ----------------------------------------------
    # DELETE a patient test for success and fail
    # ----------------------------------------------

    def test_delete_patient(self):

        p_patient = Patient(name='leen', age=18, gender='female',
                            doctor_id=3, date_of_appointment='2021-01-13')
        p_patient.insert()

        res = self.client().delete('/patient/%s' % (p_patient.id),
                                   headers={'Authorization': 'Bearer ' + TOKEN}
                                   )
        data = json.loads(res.data)

        patient = Patient.query.filter(
            Patient.id == p_patient.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Deleted patient'])
        self.assertEqual(data['Deleted patient'], p_patient.id)
        self.assertEqual(patient, None)

    def test_fail_delete_patient(self):
        res = self.client().delete(
            '/patient/111', headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # ----------------------------------------------
    # PATCH a DOCTOR test for success and fail
    # ----------------------------------------------

    def test_patch_doctor(self):

        p_doctor = Doctor(name='Leonardo Di Caprio',
                          deparment='Pediatric Surgery', level='Consltant')
        p_doctor.insert()

        res = self.client().patch('/doctors/%s' % (p_doctor.id),
                                  json=self.update_doctor,
                                  headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['updated doctor']['name'])
        self.assertTrue(data['updated doctor']['deparment'])
        self.assertTrue(data['updated doctor']['level'])

    def test_fail_patch_doctor(self):
        res = self.client().patch('/doctors', json=self.update_doctor,
                                  headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    # ----------------------------------------------
    # PATCH a patient test for success and fail
    # ----------------------------------------------

    def test_patch_patient(self):
        n_patient = Patient(name='leen', age=18, gender='female',
                            doctor_id=3, date_of_appointment='2021-01-13')
        n_patient.insert()
        res = self.client().patch('/patient/%s' % (n_patient.id),
                                  json=self.update_patient,
                                  headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['updated patient']['name'])
        self.assertTrue(data['updated patient']['age'])
        self.assertTrue(data['updated patient']['gender'])
        self.assertTrue(data['updated patient']['doctor_id'])
        self.assertTrue(data['updated patient']['date_of_appointment'])

    def test_fail_patch_patient(self):
        res = self.client().patch('/patient', json=self.update_patient,
                                  headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
