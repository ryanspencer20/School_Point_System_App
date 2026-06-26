# School Point System App

This project is an experiment for a Django Python web app.

The objective is to create a school spirit collective for the school — like Hogwarts teams receiving or deducting points for behavior, events, or initiatives.

This app helps a school create and manage customized teams during the school year and award points accordingly.

This is an experiment and a personal learning project.

## Database structure

The database lives in the **`schools`** Django app. Every table is scoped to a **School**, so each school's data stays isolated.

### Tables (implemented)

| Table | Purpose |
|-------|---------|
| **School** | Registered school (name, slug, contact email). Starts inactive until approved. |
| **SchoolRegistration** | Signup request queue (pending → approved/rejected) before a school is activated. |
| **SchoolYear** | Academic year for a school (e.g. `2025-2026`). Points are tracked per year. |
| **SchoolMembership** | Links a Django user to a school with a role and permissions. |
| **Team** | Spirit team / house for a school year (name, color, motto, display order). |
| **TeamMembership** | Optional assignment of a user to a team. |
| **PointCategory** | Groupings for awards (e.g. behavior, events, initiatives). |
| **PointAward** | Individual +/− point changes for a team, with reason and audit trail. |

### Users and roles

Login credentials are stored in Django's built-in **`auth_user`** table (passwords are hashed — never stored in custom tables).

Each person belongs to a school through **SchoolMembership**:

| Role | Who it's for | Permissions (intended) |
|------|----------------|-------------------------|
| **admin** | School principal / lead administrator (approved by the school board) | Full school setup, user management, approve teams and categories |
| **staff** | Teachers and staff who award points | Award and deduct points for teams |
| **student** | Students | View teams and leaderboard for their school |
| **viewer** | Read-only access (e.g. office staff, guests) | View standings only |

The hierarchy is built from these memberships — app access and permissions flow from role + school, not from separate credential tables.

### Point categories and teams

- **PointCategory** — Custom per school (behavior, events, initiatives, etc.).
- **Team** — Custom spirit teams per **SchoolYear** (teams can change or reset each year).
- **PointAward** — Records each change: team, amount (+ or −), reason, category, who awarded it, and when.

### Leaderboards

There is **no separate leaderboard table**. Standings are calculated by summing **PointAward** amounts per team for a given school year. A leaderboard view will read from `PointAward` at runtime.

### Security model

- **Per-school isolation** — Teams, categories, memberships, and point awards all belong to one school.
- **Approval gate** — New schools submit a **SchoolRegistration** request; the **School** record stays inactive until approved.
- **Role-based access** — Only staff and admins can create point awards; students and viewers are read-only.
- **Audit trail** — Every point change records `awarded_by` and `created_at`.

## Project layout

```
School_Point_System_App/
├── config/          # Django project settings and URLs
├── schools/         # Database models, admin, migrations
├── polls/           # Placeholder app (to be replaced or removed)
└── manage.py
```

## Local setup

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin site: http://127.0.0.1:8000/admin/

## Planned next steps

- Public school registration form
- Login and role-based views (staff vs student)
- Leaderboard page (computed from PointAward)
