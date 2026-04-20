# AutomationExercise API — Collection Notes

Base URL: `https://automationexercise.com`
API List: https://automationexercise.com/api_list
Explored manually via Postman on: 2026-04-20

---

## Endpoints

### 1. GET /api/productsList

**Purpose:** Fetch all products available on the site.
**Auth required:** No

**Request:**
- Method: GET
- URL: `https://automationexercise.com/api/productsList`
- Body: None

**Observed response — status:** `200 OK`

**Sample response body:**
```json
{
  "responseCode": 200,
  "products": [
    {
      "id": 1,
      "name": "Blue Top",
      "price": "Rs. 500",
      "brand": "Polo",
      "category": {
        "usertype": { "usertype": "Women" },
        "category": "Tops"
      }
    }
  ]
}
```

**Notes:**
- Returns the full product catalogue in one call — no pagination.
- `responseCode` is a field inside the JSON body (not just the HTTP status).
- Product schema fields: `id`, `name`, `price`, `brand`, `category.usertype.usertype`, `category.category`.
- Useful for data-driven tests — can extract product IDs and names for cart/checkout flows.

---

### 2. POST /api/createAccount

**Purpose:** Register a new user account.
**Auth required:** No

**Request:**
- Method: POST
- URL: `https://automationexercise.com/api/createAccount`
- Body format: `form-data`

**Required fields:**
| Field | Example value |
|---|---|
| name | Test User |
| email | testuser@example.com |
| password | Test@1234 |
| title | Mr |
| birth_date | 1 |
| birth_month | January |
| birth_year | 1990 |
| firstname | Test |
| lastname | User |
| company | TestCorp |
| address1 | 123 Main St |
| address2 | Apt 4 |
| country | United States |
| zipcode | 10001 |
| state | New York |
| city | New York |
| mobile_number | 9999999999 |

**Observed response — status:** `200 OK`

**Sample response body:**
```json
{
  "responseCode": 201,
  "message": "User created!"
}
```

**Notes:**
- HTTP status is `200` but the internal `responseCode` is `201` (created).
- Use a unique email each run — duplicate email returns `responseCode: 400`.
- All fields above are required; missing any causes a 400-level internal response.
- In pytest this will live in a session-scoped API fixture for creating test users.

---

### 3. POST /api/verifyLogin

**Purpose:** Confirm that a user account's credentials are valid.
**Auth required:** No

**Request:**
- Method: POST
- URL: `https://automationexercise.com/api/verifyLogin`
- Body format: `form-data`

**Required fields:**
| Field | Example value |
|---|---|
| email | testuser@example.com |
| password | Test@1234 |

**Observed response — status:** `200 OK`

**Sample response body:**
```json
{
  "responseCode": 200,
  "message": "User exists!"
}
```

**Notes:**
- Call this immediately after `createAccount` to assert the account is usable.
- Wrong credentials return `responseCode: 404` with `"User not found!"`.
- This is the assertion step in the create-account test flow.

---

### 4. DELETE /api/deleteAccount

**Purpose:** Permanently delete a user account — used for test teardown.
**Auth required:** No (credentials passed in body)

**Request:**
- Method: DELETE
- URL: `https://automationexercise.com/api/deleteAccount`
- Body format: `form-data`

**Required fields:**
| Field | Example value |
|---|---|
| email | testuser@example.com |
| password | Test@1234 |

**Observed response — status:** `200 OK`

**Sample response body:**
```json
{
  "responseCode": 200,
  "message": "Account deleted!"
}
```

**Notes:**
- Always call this after any test that creates an account — keeps the environment clean.
- In pytest this belongs in a `yield` fixture so it runs even if the test fails.
- Deleting a non-existent account returns `responseCode: 404`.

---

## User Lifecycle Flow

POST /api/createAccount  →  POST /api/verifyLogin  →  (run test)  →  DELETE /api/deleteAccount

This sequence maps directly to a pytest fixture pattern:
- **Setup:** createAccount
- **Assert:** verifyLogin (responseCode 200 + "User exists!")
- **Teardown:** deleteAccount (inside `yield` fixture)

---

## Key Observations

- All endpoints return HTTP `200` regardless of outcome — the real status is inside `responseCode` in the JSON body. Your assertions must check `response["responseCode"]`, not just `response.status_code`.
- All write operations (POST, DELETE) use `form-data`, not JSON body.
- No Bearer token or API key needed for any of these endpoints.
- The site wraps every response in a consistent envelope: `{ "responseCode": int, "message": str }` (plus data for GET).