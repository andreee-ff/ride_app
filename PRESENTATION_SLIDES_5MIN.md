# 🚴‍♂️ SafeRide API
### Making Group Cycling Safer with GPS Tracking
*ReDI School Munich - Final Project*

> **Gamma.app tip:** Use image of cyclists riding in a group on a scenic road

---

# 1️⃣ Why This Project? 💡

> **Gamma.app tip:** Use image showing cyclists spread out on a road (illustrating the problem)

## The Problem I Wanted to Solve
- Group cycling is popular in Germany
- Groups get "stretched out" - some riders fall behind
- **Safety risk:** Riders at the back get lost or separated
- Hard to know who needs help

## My Personal Motivation
- ✅ I cycle and faced this problem myself
- ✅ Wanted to build something **real and useful**
- ✅ Perfect chance to apply **FastAPI, JWT, GPS, databases**

**Goal:** Make group cycling safer with real-time GPS tracking

---

# 2️⃣ What I Built 🛠️

> **Gamma.app tip:** Use tech icons or API diagram illustration

## Tech Stack
- **FastAPI** - REST API framework
- **SQLite + SQLAlchemy** - Database with GPS coordinates
- **JWT tokens** - Secure authentication
- **Pytest** - 50 automated tests ✅

## Core Features
1. **Create bicycle rides** → get unique 6-char code
2. **Join rides** → using the code
3. **Send GPS location** → latitude, longitude, timestamp
4. **Track participants** → see everyone's position

---

# 2️⃣ Development Process 📋

> **Gamma.app tip:** Use a 4-step process diagram or roadmap visual

## How I Built It (4 Phases)

**Phase 1: Planning** 🎨
- Designed database: Users, Rides, Participations (with GPS)
- Mapped REST API endpoints

**Phase 2: Building** 🏗️
- Database models + repositories
- REST endpoints + JWT auth
- GPS coordinate storage

**Phase 3: Testing** 🧪
- 50 automated tests (100% passing!)
- TDD approach - tests first, then code

**Phase 4: Documentation** 📚
- README, Swagger docs, Postman collection

---

# 3️⃣ Results & Impact 🌟

> **Gamma.app tip:** Use split-screen: code/API screenshot on left, impact icons on right

## What Works Right Now
✅ Complete REST API with CRUD operations
✅ Secure JWT authentication
✅ GPS coordinate tracking (latitude/longitude)
✅ Unique ride codes for easy sharing
✅ 50 passing tests - production ready!

## Real-World Impact

**Safety** 🚨
- Organizers see if someone falls behind
- GPS helps locate riders in trouble

**Environment** 🌍
- Promotes cycling over driving

**Community** 👥
- Easy to organize group rides
- Build cycling communities

---

# 4️⃣ Challenges I Overcame 💪

> **Gamma.app tip:** Use problem-solution visual (before/after comparison or checkmarks)

## 3 Biggest Challenges

**1. JWT Authentication** 🔐
- **Problem:** Security setup was complex
- **Solution:** FastAPI docs + dependency injection
- **Learned:** Security frameworks make it manageable

**2. Database Relationships** 🗄️
- **Problem:** Cascade delete errors
- **Solution:** Soft deletes (is_active flag)
- **Learned:** Plan relationships upfront

**3. GPS Data Validation** 📍
- **Problem:** Validate latitude/longitude correctly
- **Solution:** Pydantic schemas with Numeric type
- **Learned:** Good validation prevents bugs

---

# 5️⃣ Future Improvements 🚀

> **Gamma.app tip:** Use futuristic tech imagery or mobile app mockup

## Technical Enhancements
- **WebSockets** → Real-time GPS updates
- **Analytics** → Calculate group "spread" distance
- **Mobile App** → React Native with background GPS
- **Route History** → Store complete GPS tracks

## New Features
- Auto-alerts when riders fall too far behind
- Heat maps showing problem areas
- Weather integration
- Route planning with elevation

## Real-World Use Cases
- 🎓 University cycling clubs
- 💼 Corporate wellness programs
- 🎉 Charity rides & events
- 🚴 Long-distance touring groups

---

# Live Demo 🎬

> **Gamma.app tip:** Use screenshot of Swagger UI or terminal with passing tests

## What I'll Show You

1. **Swagger UI** (auto-generated docs)
2. **Register users** (organizer + participant)
3. **Create ride** → get unique code
4. **Join ride** → using code
5. **Send GPS coordinates** → Munich location!
6. **Run tests** → all 50 pass ✅

**Numbers that matter:**
- 📊 50 tests passing
- 🔒 JWT security
- 📍 Real GPS tracking
- ⚡ FastAPI performance

---

# Key Takeaways 🎯

> **Gamma.app tip:** Use celebratory image or success visualization

## What This Project Shows

1. **Real Application** - Not just theory, but working software
2. **Solves Real Problems** - Cycling safety & group coordination
3. **Professional Quality** - Tests, docs, clean architecture
4. **Future Ready** - Can scale to real users

## What I Learned
✅ FastAPI & REST API design
✅ JWT authentication & security
✅ Working with GPS coordinates
✅ Test-driven development (TDD)
✅ Clean code architecture

**Building something real is way more fun than tutorials!** 🎉

---

# Thank You! 🙏

> **Gamma.app tip:** Use friendly image of person presenting or team collaboration

## Resources
- 📁 **GitHub:** https://github.com/andreee-ff/saferide_api
- 📚 **Swagger Docs:** http://localhost:8000/docs
- 📮 **Postman Collection:** In the repo

## Questions? 💬
Happy to discuss:
- Technical details
- Challenges I faced
- Future improvements
- Real-world applications

**Let's make group cycling safer!** 🚴‍♂️🌍

---

# BACKUP: Technical Details

---

# Database Schema 🗄️

```
Users
├─ id, username, password
└─ organized_rides, participated_in_rides

Rides
├─ id, title, description, start_time
├─ code (unique 6-char)
├─ created_by_user_id, is_active
└─ has_participants

Participations (GPS Tracking!)
├─ id, user_id, ride_id
├─ latitude, longitude (GPS!)
└─ updated_at (timestamp)
```

**Key:** Participations store GPS coordinates + timestamp

---

# API Endpoints 🔌

**Authentication**
- `POST /users/` - Register
- `POST /auth/login` - Get JWT token

**Rides**
- `POST /rides/` - Create ride (auth required)
- `GET /rides/` - List all rides
- `GET /rides/code/{code}` - Get by code

**GPS Tracking**
- `POST /participations/` - Join ride
- `PUT /participations/{id}` - **Send GPS coordinates**

---

# Testing Strategy 🧪

**50 Tests Total (100% passing!)**

- 24 original tests (unit + integration)
- 26 comprehensive tests (edge cases)

**What's Tested:**
✅ Authentication & JWT
✅ Ride creation & management
✅ GPS coordinate validation
✅ Error handling
✅ Authorization (who can do what)

**TDD Approach:** Tests written first, then code!
