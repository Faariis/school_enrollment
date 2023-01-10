# school_enrollment
Transparent enrollment of students in public/private schools and univerisites.

### Routes
- For all routes see `APIOverview` go to: `api/`
#### Authentication for users app teachersAuth
- This app should support login,logout and registration of teachers and CRUD operations
- Only super admin can register and delete teachers (and update)
- Teachers can update their profiles (todo whcih route?)
0. `/api/`
  - This should show all routes
1. `/api/login`
  - Api doesn't handle empty `email` and `password` it is expected to be there
  - If user doesn't exist, incorrect password
    ```bash
    {"detail":"User not found!"}
    {"detail":"Incorrect password"}
    ```
  - If user exists, jwt is generated, that has `secret` inside
    ```bash
    {"jwt":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwiZXhwIjoxNjcyNjgwOTgwLCJpYXQiOjE2NzI2NzczODB9.tPi6xBw0SxuNFPKjATQiucoF4mrxKVedlAsrpaiFDTQ"}
    ```
2. `/api/register`

  - 2.1 GET /api/register:
    - Teacher has to be loggedin as `super user` and returned value will be a list:
    ```bash
    [{"id":1,"first_name":"Anel","last_name":"Husakovic","email":"anel@eacon.ba"},{"id":4,"first_name":"teache3 - used by superuser","last_name":"","email":"t3@t"},{"id":2,"first_name":"teacher1","last_name":"","email":"teacher1@t"},{"id":3,"first_name":"teacher2","last_name":"","email":"teacher2@t"}]
    ```
    - **Task**: in this case (for `super user` only ) we have to have 2 buttons:
      - `Delete` - when this button is clicked it will ask for confirmation of actio
                   to delete the teacher. If yes frontened should send request to
                   `/api/teacher/delete/<int:pk>`.
                   It will remove the teacher and generate the message.
      - `Update` - This button should update the teacher. It should go to route
                   `/api/teacher/update/<int:pk>`
  - If it is not logged in as a super user, error
    ```bash
    {"message":"Current user is not super user. Registration not allowed!"}
    ```
  - If it is anonymous user
    ```bash
    {"detail":"Unauthenticated access"}
    ```
  - 2.2 POST /api/register:
    - Again only super user has rights to do this.
      The surved request results in inserting new teacher and returns the json.

    - If the request is empty or teacher already exist, error is returned:
      ```bash
      {"email":["This field is required."],"password":["This field is required."]}
      {"email":["Nastavnik with this email already exists."]}
      ```

3. `/api/teacher`
  - 3.1 GET /api/teacher
    - Returns current teacher that is loggedin from `jwt`
      ```bash
      {"id":4,"first_name":"teache3 - used by superuser","last_name":"","email":"t3@t"}
      ```

4. `/api/logout`
  - 4.1 POST /api/logout
    ```bash
    {
      "message": "success"
    }
    ```
5. `/api/teacher/update/<int:pk>`
  - Meaning of this route is that super user or current teacher can see the basic
    information about that teacher.
  - In case of `super user`, on this route there will be 2 buttons `Delete teacher`

6. `/api/teacher/delete/<int:pk>`


### Note
- When using tests we must add to default connection `TEST` dictionary with `NAME` of specific database (by default `test_<db>`) and do grant privileges on that db before running test:
```sql
MariaDB [(none)]> grant all privileges on my_test.* to anel@localhost;
```
