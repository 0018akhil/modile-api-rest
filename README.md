
# Truecaller type REST API

Here, is the REST API designed for moblie application to detect the whether the caller is spammer.

For assumption we have cosidered the global database where every number is present with the spam likelyhood rating.

When user downloads the moblie app the contacts are swithced to the user database after registration or login. When user adds the caller to spammers list the global database sapm likelyhood rating will be updated.

Adding email for the user is optional. User can add email after registration.

(user authentication is done through Token)

### Environment setup

```
virtualenv env
env\Scripts\activate

pip install django djangorestframework
```

### API Endpoints
#### SignUp

```
  POST /signup
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. username |
| `password` | `string` | **Required**. password |
| `phone_number` | `string` | **Required**. phone number |
| `name` | `string` | **Required**. your name |

```
Response:{Token}
```

#### SignIn

```
  POST /signin
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. username |
| `password` | `string` | **Required**. password |

```
Response:{Token}
```

#### Get contacts from global database by name

```
  GET /search?name={name}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `string` | **Required**. name |

```
Response:{name, phone_number, spam_likely_hood}
```
#### Get contacts from global database by number

```
  GET /search?number={number}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `number` | `string` | **Required**. number |

```
Response:{name, phone_number, spam_likely_hood}
```
The person’s email is only displayed if the person is a registered user and the  who is searching is in the person’s contact list.
```
Response:{name, phone_number, spam_likely_hood, email}
```
#### Add number to spam

```
  GET /spam?number={number}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `number` | `string` | **Required**. number |

```
Response:{phone_number, report_time}
```
#### Add Email

```
  POST /addemail
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**. email |

```
Response:{message}
```