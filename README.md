# 🚴‍♂️ SafeRide API - Backend for Group Bicycle Rides.

A modern FastAPI-based REST API for organizing and tracking group bicycle rides in real-time with GPS coordinates, user authentication, and ride management.

## 🧭 Project Status
- Codebase audited and streamlined by AI_Assistant
- 50 tests passing (24 original + 26 comprehensive)
- Auth examples unified around demo user `vadim` / `123456`
- Windows PowerShell instructions prioritized and verified
- Ready for GitHub commit and usage

## 🎯 Features

- ✅ User registration and authentication (JWT tokens)
- ✅ Create bicycle rides with unique join codes
- ✅ Join rides using ride code
- ✅ Send GPS coordinates during rides (latitude/longitude/timestamp)
- ✅ Track all participants' positions in real-time
- ✅ Future: Analyze group "spread" and identify stragglers and problems
- ✅ Comprehensive API documentation (Swagger UI)
- ✅ 50 comprehensive tests (100% passing)
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Pydantic data validation

## ✨ Core Functionality

**1. User Registration & Authentication**
- Users register with username/password
- Login with JWT token authentication
- Identify current user via `/auth/me`

**2. Create Bicycle Rides**
- Organizer creates a ride (title, description, start time)
- System generates unique 6-character join code (e.g., `A3X9K2`)
- Share code with participants

**3. Join Rides by Code**
- Participants join by entering the ride code
- Creates participation record in database

**4. Send GPS Coordinates (After Authentication)**
- Participants send their GPS location during the ride
- Update coordinates via `PUT /participations/{id}`
- System records: latitude, longitude, timestamp

**5. Group Analytics (Future Development)**
- Calculate distances between participants
- Identify riders falling behind
- Visualize group dynamics and spread

## 🗄️ Database Choice

**Database**: SQLite

**Justification for choosing SQLite:**

SQLite was selected as the database for the following reasons:

**Development Benefits:**
- No separate database server installation or configuration required
- Entire database in a single file (ride.db) - easy version control and sharing
- Built-in Python support - no external dependencies needed
- Simple testing workflow (seed_data.py easily resets and populates the database)

**Technical Considerations:**
- Full SQL and ACID transaction support
- Sufficient performance for the current application scale
- Excellent integration with SQLAlchemy ORM
- Easy migration to PostgreSQL in the future (thanks to SQLAlchemy abstraction layer)

**Limitations (acknowledged):**
- Not suitable for high-load production systems with concurrent writes
- Limited to a single server (no distributed setup)
- PostgreSQL recommended for production deployment

## 📚 API Endpoints

### Users (`/users`)
- `POST /users/` - Create new user
- `GET /users/{id}` - Get user by ID
- `GET /users/` - Get all users

### Authentication (`/auth`)
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user profile

### Rides (`/rides`)
- `POST /rides/` - Create new ride
- `GET /rides/` - Get all rides
- `GET /rides/{id}` - Get ride by ID
- `GET /rides/code/{code}` - Get ride by code
- `PUT /rides/{id}` - Update ride
- `DELETE /rides/{id}` - Delete ride

### Participation (`/participations`)
- `POST /participations/` - Join a ride by code
- `GET /participations/` - Get all participations
- `GET /participations/{id}` - Get participation details
- `PUT /participations/{id}` - Send GPS coordinates (latitude, longitude, timestamp)

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- pip

### Installation

**1. Clone and enter project:**
```sh
cd saferide_api
```

**2. Create virtual environment:**
```sh
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate
```

**3. Install dependencies:**
```sh
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

### Running the Application

**Start the server:**
```sh
# Default (localhost:8000)
uvicorn app.main:create_app --factory --reload

# Custom host/port
uvicorn app.main:create_app --factory --host=0.0.0.0 --port=8000 --reload
```

**Access API documentation:**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Testing with Postman

**Import the Postman collection:**
1. Open Postman
2. Click **Import** button
3. Select `SafeRide_API.postman_collection.json` from the project root
4. Set base URL variable: `baseUrl = http://127.0.0.1:8000`
5. Start testing endpoints with ready-made requests!

The collection includes all API endpoints organized by feature (Users, Authentication, Rides, Participations).

### Running Tests

```sh
# Run all tests (original + comprehensive)
pytest

# Run only the original tests (24 tests)
pytest tests/ -v

# Run comprehensive AI-generated tests (26 tests)
pytest AI_Assistant_Analysis/comprehensive_tests/ -v

# Run specific test class
pytest AI_Assistant_Analysis/comprehensive_tests/test_comprehensive.py::TestSecurityAndAuthorization -v

# Run with coverage report
pytest --cov=app --cov-report=html
```

## 📊 Test Coverage

**Total: 50 tests (100% passing)** ✅

| Category | Tests | Status |
|----------|-------|--------|
| Original Tests | 24 | ✅ PASS |
| Comprehensive Tests | 26 | ✅ PASS |
| **Total** | **50** | **✅ PASS** |

### Test Categories
- Authentication & Authorization
- Ride Management
- Participation Management
- Data Validation
- Edge Cases
- Security & JWT handling
- API Contract Compliance
- Concurrency

**See `AI_Assistant_Analysis/README_AI.md` for detailed test breakdown, comparison with original tests, and enhancement recommendations.**

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication.

**How to authenticate:**
1. Create a user: `POST /users/` with username and password
2. Login: `POST /auth/login` with credentials (returns JWT token)
3. Use token: Add `Authorization: Bearer {token}` header to protected endpoints

### Windows PowerShell Usage (Primary Example)

Demo user: `vadim` / `123456` (created by `seed_data.py`).

PowerShell does NOT treat single quotes inside JSON like bash. Escape inner double quotes or build JSON via `ConvertTo-Json`. Always invoke `curl.exe` (native binary) rather than the `curl` alias (which maps to `Invoke-WebRequest`).

#### Step 1: Create user (idempotent)
```powershell
curl.exe -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d "{\"username\":\"vadim\",\"password\":\"123456\"}"
```
If the user already exists you will get `409 Conflict`.

Readable alternative:
```powershell
$body = @{ username = "vadim"; password = "123456" } | ConvertTo-Json
curl.exe -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d $body
```

#### Step 2: Login and get token
```powershell
$login = curl.exe -X POST "http://127.0.0.1:8000/auth/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=vadim&password=123456"
$token = ($login | ConvertFrom-Json).access_token
Write-Host "Token: $token"
```

#### Step 3: Authenticated request
```powershell
curl.exe -X GET "http://127.0.0.1:8000/auth/me" -H "Authorization: Bearer $token"
```

#### One-line quick workflow
```powershell
curl.exe -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d "{\"username\":\"vadim\",\"password\":\"123456\"}"; $login = curl.exe -X POST "http://127.0.0.1:8000/auth/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=vadim&password=123456"; $token = ($login | ConvertFrom-Json).access_token; curl.exe -X GET "http://127.0.0.1:8000/auth/me" -H "Authorization: Bearer $token"
```

#### Common PowerShell pitfalls
- Using `curl` alias instead of `curl.exe` → headers lost / wrong behavior
- Not escaping quotes inside JSON → 422 JSON decode error
- Trailing spaces after backticks in multiline → malformed body
- Single quotes around JSON keys/values → invalid JSON for this API

### POSIX (Linux / macOS) Example

#### Step 1: Create a User
```bash
curl -X POST "http://127.0.0.1:8000/users/" \
	-H "Content-Type: application/json" \
	-d '{"username": "vadim", "password": "123456"}'
```

**Response:**
```json
{
	"id": 1,
	"username": "vadim"
}
```

#### Step 2: Login and Get Token
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
	-H "Content-Type: application/x-www-form-urlencoded" \
	-d "username=vadim&password=123456"
```

**Response:**
```json
{
	"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
	"token_type": "bearer"
}
```

**Copy the `access_token` value** - you'll use it in the next step.

#### Step 3: Use Token to Access Protected Endpoints
Replace `{your_token_here}` with the token from Step 2:

```bash
curl -X GET "http://127.0.0.1:8000/auth/me" \
	-H "Authorization: Bearer {your_token_here}"
```

**Response:**
```json
{
	"id": 1,
	"username": "vadim"
}
```

### Using Swagger UI (Recommended for Testing)

The easiest way to test the API is using Swagger UI:

1. **Start the server:**
	 ```sh
	 uvicorn app.main:create_app --factory --reload
	 ```

2. **Open Swagger UI:**
	 ```
	 http://127.0.0.1:8000/docs
	 ```

3. **Test endpoints directly in browser:**
	 - Create a user: Click "POST /users/" → "Try it out"
	 - Login: Click "POST /auth/login" → "Try it out"
	 - Get token automatically stored by Swagger
	 - Test other endpoints with automatic auth

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Missing or invalid token | Check token is correct and not expired |
| `422 Unprocessable Content` | Invalid request format | Check JSON format and required fields |
| `409 Conflict` | Username already exists | Use different username |
| `404 Not Found` | Endpoint doesn't exist | Check endpoint URL spelling |

## 🌱 Database Management & Seeding

The app uses SQLite database (auto-created on first run).

### Reset Database
Remove all tables and recreate empty schema:
```sh
python seed_data.py --reset
```

### Seed Default Demo Data
Creates demo users, rides, and participation records:
```sh
python seed_data.py
```
Creates:
- User: `vadim` / password: `123456`
- Several demo rides
- Sample participation records

Script is idempotent (won't create duplicates).

### Seed Large Dataset
Generate random test data:
```sh
python seed_data.py --massive
```
Creates:
- Fixed user: `vadim` / `123456`
- Random users
- Random rides
- Random participation entries

### Custom Data Volume
```sh
python seed_data.py --massive --users=50 --rides=100 --participations=500
```

## ⚙️ Environment Variables

Configuration via `.env` file (optional, has safe defaults):

```env
# JWT Configuration
SECRET_KEY="dev-secret-key-change-me"  # Change for production!
ALGORITHM="HS256"                       # Token algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=60          # Token expiration time
```

**For Production:**
```bash
export SECRET_KEY="your-secure-random-key"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 📁 Project Structure

```
saferide_api/
├── app/                          # Core application
│   ├── main.py                  # FastAPI app factory with routes
│   ├── models.py                # SQLAlchemy ORM models (User, Ride, Participation with GPS)
│   ├── schemas.py               # Pydantic validation schemas
│   ├── routers.py               # API endpoint definitions
│   ├── repositories.py          # Data access layer (ride code generation, GPS updates)
│   ├── security.py              # JWT token management
│   ├── injections.py            # Dependency injection
│   └── __init__.py
│
├── tests/                        # Original test suite (24 tests)
│   ├── test_auth_login.py       # Authentication tests
│   ├── test_auth_register.py    # User registration tests
│   ├── test_operate_with_ride.py # Ride management tests
│   ├── test_participations.py   # Participation + GPS tests
│   ├── test_unit_auth_and_ride.py # Unit tests
│   └── conftest.py              # Pytest fixtures
│
├── AI_Assistant_Analysis/        # AI-generated materials
│   ├── README_AI.md             # Test analysis overview
│   ├── TEST_COMPARISON_EN.md    # Test comparison (English)
│   ├── TEST_ENHANCEMENT_ROADMAP.md # Future improvements
│   └── comprehensive_tests/     # 26 comprehensive tests
│
├── .env                         # Environment variables
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── seed_data.py                 # Database seeding script
├── SafeRide_API.postman_collection.json  # Postman API collection
└── README.md                    # This file
```

## 🛠️ Development

### Technology Stack
- **FastAPI** - Main backend framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Data storage
- **Pydantic** - Data schemas and validation
- **pytest** - Testing framework
- **TDD approach** - Tests first, then code

### Code Style
- Type hints throughout
- Pydantic for data validation
- SQLAlchemy ORM for database
- FastAPI for API framework

### Adding New Tests
Tests should go in `/tests` for original tests or `AI_Assistant_Analysis/comprehensive_tests/` for additional integration tests.

Running tests:
```sh
pytest tests/ -v
```

## 🐛 Troubleshooting

**Virtual environment not activating?**
- Windows: Use `.\venv\Scripts\Activate.ps1` (PowerShell)
- Mac/Linux: Use `source venv/bin/activate`

**Database locked error?**
- Delete `*.db` files and restart
- Run `python seed_data.py` to reseed

**Port 8000 already in use?**
```sh
uvicorn app.main:create_app --factory --port=8001 --reload
```

**Tests failing?**
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version: 3.13+ required
- Clear cache: `pytest --cache-clear`

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)

## 📄 License

Maybe ... one day ;)

## 🎓 About This Project

This project was created as a final project after completing the Python Backend Development course at **ReDI School of Digital Integration Munich**.

## 🤝 Development Process

**Developer: Vadim Andreev**
- All code logic, API design, and implementation decisions
- Core test suite in `/tests` directory (24 tests)

**AI Assistance: Claude**
- README.md documentation structure and formatting
- Comprehensive test suite in `/AI_Assistant_Analysis/comprehensive_tests` (26 additional tests)
- Code review and analysis

**Note**: The comprehensive AI-generated tests passed successfully without any modifications to the existing codebase, validating the quality of the original implementation.

---

**Last Updated:** November 29, 2025  
**Status:** Production Ready ✅