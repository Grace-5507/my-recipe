import unittest
from main import create_app
from config import TestConfig
from exts import db



class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)

        self.client = self.app.test_client(self)


        with self.app.app_context():
            db.init_app(self.app)

            db.create_all()



    def test_hello_world(self):
        hello_response=self.client.get('/Hello') 

        json=hello_response.json

        self.assertEqual(json,{'message':"Hello world"}) 

        #print(json)  

    def test_Signup(self):
        signup_response=self.client.post('/auth/signup',
            json={"username":"testuser",
            "email":"testuser@gmail.com",
            "password":"pass1234"}
        )

        status_code = signup_response.status_code
        self.assertEqual(status_code, 201)


    def test_Login(self):
        signup_response=self.client.post('/auth/signup',
            json={"username":"testuser",
            "email":"testuser@gmail.com",
            "password":"pass1234"}
        )

        login_response=self.client.post('/auth/login',
            json={"username":"testuser",
            "password":"pass1234"}
        )

        status_code = login_response.status_code

        json = login_response.json

        print(json)

        self.assertEqual(status_code, 200)


    def test_get_all_recipes(self):
        response = self.client.get('/recipe/recipes')

        status_code = response.status_code

        self.assertEqual(status_code, 200)



    def test_get_one_recipe(self):
        response = self.client.get('/recipe/recipe/<id=2>')

        status_code = response.status_code

        self.assertEqual(status_code, 404)

    def test_create_recipe(self):
        signup_response=self.client.post('/auth/signup',
            json={"username":"testuser",
            "email":"testuser@gmail.com",
            "password":"pass1234"}
        )

        login_response=self.client.post('/auth/login',
            json={"username":"testuser",
            "password":"pass1234"}
        )

        access_token = login_response.json['access_token']

        create_recipe_response = self.client.post(
            '/recipe/recipes', 
            json={
                'title':'test cookies',
                'description':'test cookiie recipe description'
                },
            headers={
                "Authorization":f"Bearer {access_token}"
            }
            )

        status_code = create_recipe_response.status_code

        print(create_recipe_response.json)

        self.assertEqual(status_code, 201)


    def test_update_recipe(self):
        signup_response=self.client.post('/auth/signup',
            json={"username":"testuser",
            "email":"testuser@gmail.com",
            "password":"pass1234"}
        )

        login_response=self.client.post('/auth/login',
            json={"username":"testuser",
            "password":"pass1234"}
        )

        access_token = login_response.json['access_token']

        create_recipe_response = self.client.post(
            '/recipe/recipes', 
            json={
                'title':'test cookies',
                'description':'test cookiie recipe description'
                },
            headers={
                "Authorization":f"Bearer {access_token}"
            }
            )
        status_code = create_recipe_response.status_code
 
        id = 1
        update_response = self.client.put(
            f'/recipe/recipe/{id}', 
            json={
                'title':'test cookies update',
                'description':'test cookiie updated recipe description'
                },
            headers={
                "Authorization":f"Bearer {access_token}"
            }

            )

        status_code = update_response.status_code
        self.assertEqual(status_code, 200)

    def test_delete_recipe(self):
        signup_response=self.client.post('/auth/signup',
            json={"username":"testuser",
            "email":"testuser@gmail.com",
            "password":"pass1234"}
        )

        login_response=self.client.post('/auth/login',
            json={"username":"testuser",
            "password":"pass1234"}
        )

        access_token = login_response.json['access_token']

        create_recipe_response = self.client.post(
            '/recipe/recipes', 
            json={
                'title':'test cookies',
                'description':'test cookiie recipe description'
                },
            headers={
                "Authorization":f"Bearer {access_token}"
            }
            )
        status_code = create_recipe_response.status_code
 
        id = 1
        delete_response = self.client.delete(
            f'/recipe/recipe/{id}',
            headers={
                "Authorization":f"Bearer {access_token}"
            })

        status_code = delete_response.status_code

        self.assertEqual(status_code, 200)


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()



if __name__ == "__main__":
    unittest.main()