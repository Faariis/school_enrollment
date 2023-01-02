# school_enrollment
Transparent enrollment of students in public/private schools and univerisites.

### Routes
#### Authentication for users app teachersAuth
- This app should support login,logout and registration of teachers and CRUD operations
- Only super admin can register and delete teachers (and update)
- Teachers can update their profiles (todo whcih route?)
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
  2.1 GET /api/register:
- It has to be loggedin as `super user` and returned value will be a list:
```bash
[{"id":1,"first_name":"Anel","last_name":"Husakovic","email":"anel@eacon.ba"},{"id":4,"first_name":"teache3 - used by superuser","last_name":"","email":"t3@t"},{"id":2,"first_name":"teacher1","last_name":"","email":"teacher1@t"},{"id":3,"first_name":"teacher2","last_name":"","email":"teacher2@t"}]
```
- If it is not logged in as a super user, error
```bash
{"message":"Current user is not super user. Registration not allowed!"}
```
- If it is anonymous user
```bash
{"detail":"Unauthenticated access"}
```
  2.2 POST /api/register:
- Again super user has rights to do this
- If it is empty or already exist:
```bash
{"email":["This field is required."],"password":["This field is required."]}
{"email":["Nastavnik with this email already exists."]}
```
3. `/api/teachers`
  3.1 GET /api/teacher
  - Returns current teacher that is loggedin with jwt
  ```bash
    {"id":4,"first_name":"teache3 - used by superuser","last_name":"","email":"t3@t"}
  ```
4. `/api/logout`
  4.1 POST /api/logout
```bash
{
    "message": "success"
}
```