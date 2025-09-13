# API Documentation

This document outlines the available API endpoints, expected request/response structures, and authentication requirements

---

## API Status Codes Reference

This section explains common HTTP status codes used across the backend.

| Status Code          | Meaning              | Description                                                                   |
| -------------------- | -------------------- | ----------------------------------------------------------------------------- |
| **200 OK**           | Success              | The request was processed successfully and a valid response is returned.      |
| **201 Created**      | Resource Created     | The request was successful and a new resource has been created.               |
| **400 Bad Request**  | Invalid Input        | The request is malformed or required fields are missing/invalid.              |
| **401 Unauthorized** | Access Token Expired | Authentication failed due to missing or expired access token.                 |
| **403 Forbidden**    | Access Denied        | The request is understood but not allowed. The user lacks proper permissions. |

## Base URL

For local development: http://localhost:8000

### Authentication API

#### `POST /seed-data/`

Allow seeding data into database

**Note** Accepts only .xlxs file format

**Request Body:**

```json
{
  "loans":<FILE>,
  "customers":<FILE>
}
```

**Response Body:**

```json
{
  "message": "Files uploaded successfully",
  "customer_file": "E:\\projects\\alemeno\\uploads\\customer_data.xlsx",
  "loan_file": "E:\\projects\\alemeno\\uploads\\loan_data.xlsx"
}
```

#### `POST /register/`

Allow registering new customers

**Request Body:**

```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "age": 30,
  "monthly_salary": 50000,
  "phone_number": "9876543210"
}
```

**Response Body:**

```json
{
  "customer_id": 1235,
  "name": "Jane Doe",
  "age": 30,
  "monthly_income": 50000.0,
  "approved_limit": 1800000.0,
  "phone_number": "9876543210"
}
```

#### `GET /view-loans/{customer_id}`

Allow fetching of all present loans of a customer

**Request Params:**

```bash
customer_id
```

**Response Body:**

```json
{
  "loans": [
    {
      "loan_id": 2295,
      "loan_amount": 900000.0,
      "interest_rate": 8.2,
      "monthly_installment": 15344.0,
      "repayments_left": 15
    },
    {
      "loan_id": 2619,
      "loan_amount": 700000.0,
      "interest_rate": 16.32,
      "monthly_installment": 28701.0,
      "repayments_left": 0
    },
    {
      "loan_id": 2772,
      "loan_amount": 800000.0,
      "interest_rate": 13.19,
      "monthly_installment": 21773.0,
      "repayments_left": 12
    },
    {
      "loan_id": 2799,
      "loan_amount": 700000.0,
      "interest_rate": 10.2,
      "monthly_installment": 233333.0,
      "repayments_left": 0
    }
  ]
}
```

#### `GET /view-loan/{loan_id}`

Allow fetching loan info via loan id

**Request Params:**

```bash
loan_id
```

**Response Body:**

```json
{
  "loan_id": 2295,
  "customer": {
    "id": 948,
    "first_name": "Adaline",
    "last_name": "Diaz",
    "phone_number": "9519253076",
    "age": 65
  },
  "loan_amount": 900000.0,
  "tenure": 129,
  "interest_rate": 8.2,
  "monthly_installment": 15344.0
}
```

#### `POST /check-eligibility/`

Allow client and operation to request for password change

**Request Body:**

```json
{
  "customer_id": 948,
  "loan_amount": 100000,
  "interest_rate": 10,
  "tenure": 10
}
```

**Response Body:**

```json
{
  "customer_id": 948,
  "loan_amount": 100000.0,
  "interest_rate": 10.0,
  "tenure": 10
}
```

#### `POST /create-loan/`

Allow client and operation to request for token refresh

**Request Body:**

```json
{
  "customer_id": 948,
  "loan_amount": 100000,
  "interest_rate": 10,
  "tenure": 10
}
```

**Response Body:**

```json
{
  "customer_id": 948,
  "loan_approved": true,
  "monthly_installment ": 10464.04,
  "loan_id": 3048,
  "message": "Loan approved"
}
```
