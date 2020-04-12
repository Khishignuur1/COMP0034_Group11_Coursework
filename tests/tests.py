"""
Written by 17075800
"""
from run import app
import unittest
import sqlite3
from base import BaseTestCase

# 1.Ensuring correct loading of basic pages and login required pages
class LoadPageTest(BaseTestCase):

    # 1.1.Ensuring correct loading of basic pages

    # Ensure Index page loads correctly
    def test_Index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertIn(b'Welcome', response.data)

    # Ensure About page loads correctly
    def test_About(self):
        tester = app.test_client(self)
        response = tester.get('/about', content_type='html/text')
        self.assertIn(b'About page', response.data)

    # Ensure Items page loads correctly
    def test_Items(self):
        tester = app.test_client(self)
        response = tester.get('/home', content_type='html/text')
        self.assertIn(b'Description', response.data)

    # 1.2.Ensuring correct loading of user login required pages and functions

    # Ensure Account page requires user login
    def test_account_requires_login(self):
        tester = app.test_client(self)
        response = tester.post('/account', follow_redirects=True)
        self.assertIn(b'You must be logged in', response.data)

    # Ensure Logout requires user login
    def test_logout_requires_login(self):
        tester = app.test_client(self)
        response = tester.post('/logout', follow_redirects=True)
        self.assertIn(b'Not Allowed', response.data)

    # Ensure Create item page requires user login
    def test_create_item_requires_login(self):
        tester = app.test_client(self)
        response = tester.post('item/create', follow_redirects=True)
        self.assertIn(b'You must be logged in', response.data)

    # Ensure Item update requires user log in
    def test_update_item_requires_login(self):
        tester = app.test_client(self)
        response = tester.post('/item/1/update', follow_redirects=True)
        self.assertIn(b'You must be logged in', response.data)

    # Ensure Delete item page requires user login
    def test_delete_item_requires_login(self):
        tester = app.test_client(self)
        response = tester.post('/item/1/delete', follow_redirects=True)
        self.assertIn(b'You must be logged in', response.data)


# 2. Ensure Sign up function works correctly
class UserSignupTests(BaseTestCase):

    # Ensure Signup page loads correctly
    def test_signup(self):
        tester = app.test_client(self)
        response = tester.get('/signup/', content_type='html/text')
        self.assertIn(b'Username', response.data)

    # Ensure Signup function works with valid credentials
    def test_valid_Signup(self):
        tester = app.test_client(self)
        response = tester.post('/signup/',
                               data={'name': 'random14', 'email': 'random14@gmail.com', 'password': 'password',
                                     'confirm': 'password'},
                               follow_redirects=True)
        self.assertIn(b'Signed up successfully', response.data)

    # Ensure Signup error messages function correctly with empty credentials
    def test_empty_Signup(self):
        tester = app.test_client(self)
        response = tester.post('/signup/', follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    # Ensure Signup error messages function correctly with invalid email
    def test_invalid_email_Signup(self):
        tester = app.test_client(self)
        response = tester.post('/signup/',
                               data={'name': 'random15', 'email': 'random14com', 'password': 'password',
                                     'confirm': 'password'},
                               follow_redirects=True)
        self.assertIn(b'Valid email address required', response.data)

    # Ensure Signup error messages function correctly with non-Unique username
    def test_non_Unique_username_Signup(self):
        tester = app.test_client(self)
        response = tester.post('/signup/',
                               data={'name': 'random12'}, follow_redirects=True)
        self.assertIn(b'username is taken', response.data)

    # Ensure Signup error messages function correctly with non-Unique email
    def test_non_Unique_email_Signup(self):
        tester = app.test_client(self)
        response = tester.post('/signup/',
                               data={'email': 'random11@gmail.com'}, follow_redirects=True)
        self.assertIn(b'email is taken', response.data)

    # Ensure Signup error messages function correctly with Un-matching password
    def test_un_matching_password_Signup(self):
        tester = app.test_client(self)
        response = tester.post('/signup/',
                               data={'password': 'Pass', 'confirm': 'password'},
                               follow_redirects=True)
        self.assertIn(b'Passwords must match', response.data)


# 3. Ensure Login function works correctly
class UserLoginTests(BaseTestCase):

    # Ensure login page loads correctly
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login/', content_type='html/text')
        self.assertIn(b'Email', response.data)

    # Ensure login functions correctly with correct credentials
    def test_valid_login(self):
        tester = app.test_client(self)
        response = tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'},
                               follow_redirects=True)
        self.assertIn(b'logged in', response.data)

    # Ensure login error messages function correctly with invalid
    def test_invalid_email_login(self):
        tester = app.test_client(self)
        response = tester.post('/login/', data={'email': 'random14', 'password': '1234'},
                               follow_redirects=True)
        self.assertIn(b'Invalid email address', response.data)

    # Ensure login error messages function correctly with empty credentials
    def test_empty_login(self):
        tester = app.test_client(self)
        response = tester.post('/login/', follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    # Ensure login error messages function correctly with incorrect credentials 1
    def test_invalid_login(self):
        tester = app.test_client(self)
        response = tester.post('/login/', data={'email': 'random11@gmail.com', 'password': '1234'},
                               follow_redirects=True)
        self.assertIn(b'Invalid email or password', response.data)

    # Ensure login error messages function correctly with incorrect credentials 2
    def test_invalid_login_2(self):
        tester = app.test_client(self)
        response = tester.post('/login/', data={'email': 'rand@mail.com', 'password': 'password'},
                               follow_redirects=True)
        self.assertIn(b'Invalid email or password', response.data)

    # Ensure a logged in user can logout
    def test_user_can_logout(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'})
            response = tester.get('/logout/', follow_redirects=True)
            self.assertIn(b'logged out', response.data)


# 4. Ensure Account info update function works correctly
class UserAccountTests(BaseTestCase):

    # Ensure Account page loads correctly when logged in
    def test_Account_logged_in(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.get('/account', content_type='html/text')
            self.assertIn(b'Account Info', response.data)

    # Ensure Account update with empty credentials loads correct message
    def test_Account_update_empty(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.post('/account', follow_redirects=True)
            self.assertIn(b'This field is required.', response.data)

    # Ensure Account update with Non-unique username loads correct message
    def test_Account_update_non_unique_username(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.post('/account', data={'name': 'random12', 'email': 'random12@gmail.com'},
                                   follow_redirects=True)
            self.assertIn(b'This username is taken.', response.data)

    # Ensure Account update with Non-unique email loads correct message
    def test_Account_update_non_unique_email(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.post('/account', data={'name': 'random11', 'email': 'random12@gmail.com'},
                                   follow_redirects=True)
            self.assertIn(b'This email is taken.', response.data)

    # Ensure Account update without change loads correct message
    def test_Account_update_no_change(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.post('/account', data={'name': 'random11', 'email': 'random11@gmail.com'},
                                   follow_redirects=True)
            self.assertIn(b'Your account has been updated!', response.data)

    # Ensure a logged in user can logout
    def test_user_can_logout(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data=dict(email="random11@gmail.com", password="password"), follow_redirects=True)
            response = tester.get('/logout/', follow_redirects=True)
            self.assertIn(b'logged out', response.data)


# 5. Ensure Create item function works correctly
class UserCreateItemTests(BaseTestCase):

    # Ensure Create item page loads correctly when logged in
    def test_create_item_logged_in(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.get('/item/create', content_type='html/text')
            self.assertIn(b'New Item', response.data)

    # Ensure Create item with empty fields loads correct message
    def test_create_item_empty(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.post('/item/create', follow_redirects=True)
            self.assertIn(b'This field is required.', response.data)

    # Ensure Create item with invalid price loads correct message
    def test_create_item_invalid_price(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.post('/item/create', data={'title': 'string', 'content': 'string', 'price': 'string'},
                                   follow_redirects=True)
            self.assertIn(b'This field is required.', response.data)

    # Ensure Create item with valid fields functions correctly
    def test_create_item_valid(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.post('/item/create', data={'title': 'Title', 'content': 'Content', 'color': 'green',
                                                         'size': 'xxl', 'price': '12'},
                                   follow_redirects=True)
            self.assertIn(b'Your item has been created!', response.data)


# 6. Ensure Update/Delete item function works correctly
class UserUpDelTests(BaseTestCase):

    # Ensure update or delete options do no appear for items created by other users
    def test_update_restriction(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.get('/item/7', follow_redirects=True)
            self.assertNotIn(b'Update', response.data)

    # Ensure update or delete options appear items created current user
    def test_update_appear(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.get('/item/2', content_type='html/text')
            self.assertIn(b'Update', response.data)

    # Ensure update item page loads correctly
    def test_update_item_logged_in(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.get('/item/2/update', content_type='html/text')
            self.assertIn(b'Update Item', response.data)

    # Ensure delete item function works correctly
    def test_delete_item_logged_in(self):
        tester = app.test_client(self)
        with tester:
            tester.post('/login/', data={'email': 'random11@gmail.com', 'password': 'password'}, follow_redirects=True)
            response = tester.get('/item/8/delete', follow_redirects=True)
            self.assertIn(b'Your item has been deleted!', response.data)


# 7. Ensure Search bar works correctly
class UserSearchTests(BaseTestCase):

    # Ensure search error messages function correctly with empty credentials
    def test_empty_search(self):
        tester = app.test_client(self)
        response = tester.post('/search', data={'search_term': ''}, follow_redirects=True)
        self.assertIn(b'Search field empty', response.data)

    # Ensure search error messages function correctly with no matching items
    def test_no_match_search(self):
        tester = app.test_client(self)
        response = tester.post('/search', data={'search_term': 'hifu6172310'}, follow_redirects=True)
        self.assertIn(b'No matching items', response.data)

    # Ensure search functions correctly with valid item
    def test_valid_search(self):
        tester = app.test_client(self)
        response = tester.post('/search', data={'search_term': 'shirt'}, follow_redirects=True)
        self.assertIn(b'Title', response.data)


# delete test account
def delete_test():
    mydb = sqlite3.connect('data.sqlite')
    c = mydb.cursor()
    c.execute(''' DELETE from user WHERE name LIKE '%random14%' ''')
    mydb.commit()


delete_test()

if __name__ == '__main__':
    unittest.main()
