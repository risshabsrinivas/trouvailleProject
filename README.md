Trouvaille Travel Portal
![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)


## Tech Stack

**Client:** HTML, CSS, JavaScript

**Server:** Django, Python, MySQL


## Installation - Pre Requisites

Install my-project with npm
Download SQLite
```bash
  npm install my-project
  pip3 install mysqlconnector
```
    
## Run Locally

Clone the project

```bash
  git clone https://github.com/risshabsrinivas/trouvailleProject
```

Go to the project directory

```bash
  cd mysite
```

Install dependencies

```bash
  pip3 install django
```

Start the server

```bash
  python3 manage.py runserver
```


## API Reference

#### Get all items

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.


## Documentation

[Documentation](https://linktodocumentation)


## Features

- Light/dark mode toggle
- Live previews
- Fullscreen mode
- Cross platform

