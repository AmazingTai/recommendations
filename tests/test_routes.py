"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch

from flask import json
from service import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db
from service.models import Recommendations



# Product_id
PO = 3
PT = 5
RL = 1



######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.debug = False
        # global app
        Recommendations.init_db(app)
        # pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()
        db.create_all()
        self.app = app.test_client()


    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()
        # pass

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_a_recommendation(self):
        """ Create a recommendation and assert that it exists """
        recommendation = Recommendations()
        # self.assertEqual(recommendation.status, status.HTTP_201_CREATED)
        self.assertTrue(recommendation is not None)
        self.assertEqual(recommendation.id, None)
        self.assertEqual(recommendation.product_origin, None)
        self.assertEqual(recommendation.product_target, None)
        self.assertEqual(recommendation.relation, None)
        self.assertEqual(recommendation.is_deleted, None)
    

    def test_add_a_recommendation(self):
        """ Create a recommendation and add it to the database """
        recommendation_rawdata = {'product_origin': 2, 'product_target': 3, 'relation': 1} 
        data_json = json.dumps(recommendation_rawdata)
        resp = self.app.post("/recommendations", data = data_json, content_type='application/json')

        location = resp.headers.get('Location', None)
        self.assertTrue(location is not None)

        resp_data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp_data['product_origin'], 2)
        self.assertEqual(resp_data['product_target'], 3)
        self.assertEqual(resp_data['relation'], 1)
        self.assertEqual(resp_data['is_deleted'], 0)

        # post the same data  Missing 68-71 
        recommendation_rawdata = {'product_origin': 3, 'product_target': 4, 'relation': 1}
        data_json = json.dumps(recommendation_rawdata)
        resp = self.app.post("/recommendations", data = data_json, content_type='application/json')

        resp_data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp_data['product_origin'], 3)
        self.assertEqual(resp_data['product_target'], 4)
        self.assertEqual(resp_data['relation'], 1)
        self.assertEqual(resp_data['is_deleted'], 0)

        recommendation_rawdata = {'product_origin': 3, 'product_target': 4, 'relation': 1}
        data_json = json.dumps(recommendation_rawdata)
        resp = self.app.post("/recommendations", data = data_json, content_type='application/json')

        location = resp.headers.get('Location', None)
        self.assertTrue(location is not None)

        resp_data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp_data['product_origin'], 3)
        self.assertEqual(resp_data['product_target'], 4)
        self.assertEqual(resp_data['relation'], 1)
        self.assertEqual(resp_data['is_deleted'], 0)


        resp = self.app.get('/recommendations')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(resp is not None)

        resp = self.app.get('/recommendations/1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp is not None)

        # not found
        resp = self.app.get('/recommendations/99')
        resp_data = json.loads(resp.data)
        self.assertTrue(resp is not None)

        recommendation_rawdata = {'product_origin': 2, 'product_target': 3, 'relation': 1}
        data_json = json.dumps(recommendation_rawdata)
        resp = self.app.post("/recommendations", data = data_json, content_type='application/txt')
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)




