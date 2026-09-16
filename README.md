# Smart College Event & Participation Management System (CampusPulse)

CampusPulse is a full-stack web application for college event discovery, student registration, and coordinator management. Built with **React**, **Vite**, **TypeScript**, **Django REST Framework**, and **PostgreSQL / SQLite**.

---

## ⚠️ Important Note on GitHub Pages vs Real Deployment

> [!WARNING]
> **Why GitHub Pages shows `README.html` when clicking "Visit site"**:
> GitHub Pages is a hosting service meant for static HTML/CSS/JS websites or documentation pages. When enabled on a source repository without static output configuration, GitHub Pages automatically converts `README.md` into `README.html`.
> 
> A full-stack application (Django Python API + JWT Auth + Database + React Frontend) **cannot** run on GitHub Pages because GitHub Pages does not execute server-side Python code or host databases.
> 
> **How to fix "Visit site" on GitHub Pages**:
> 1. Go to your GitHub repository -> **Settings** -> **Pages**.
> 2. Under **Build and deployment** -> **Source**, select **Disabled** (or configure a custom workflow pointing to your deployed domain).
> 3. Add your **Real Live Deployed URL** (e.g., on Render or Vercel) to your GitHub repository's **Website** link at the top right of the main repository page (About -> Website).

---

## 🚀 Live Production Deployment Options

This project is fully configured for cloud deployment across free/low-cost platforms.

### Option 1: Render 1-Click Blueprint (Recommended Fullstack Deployment)

The repository includes a `render.yaml` infrastructure-as-code file that deploys the Django REST API, PostgreSQL database, and React frontend automatically on [Render](https://render.com).

1. Push this repository to GitHub.
2. Log in to [Render](https://render.com) and click **New +** -> **Blueprint**.
3. Connect your GitHub repository `Smart-College-Event-Participation-Management-System`.
4. Render will automatically detect `render.yaml` and provision:
   - **`campuspulse-backend`**: Django Web Service running Gunicorn and WhiteNoise.
   - **`campuspulse-db`**: PostgreSQL Database instance.
   - **`campuspulse-frontend`**: React/Vite Static Site with SPA routing.
5. Click **Apply**. Once built, open your live deployed frontend URL!

---

### Option 2: Vercel (Frontend) + Render / Railway (Backend)

#### Step 1: Deploy Backend to Render / Railway
- **Environment**: Python 3.11+
- **Build Command**: `bash backend/build.sh`
- **Start Command**: `cd backend && gunicorn config.wsgi:application`
- **Environment Variables**:
  - `DJANGO_SECRET_KEY`: (Generate a secure secret key)
  - `DJANGO_DEBUG`: `0`
  - `ALLOWED_HOSTS`: `*`
  - `CORS_ALLOW_ALL_ORIGINS`: `1` (or specify frontend domain)
  - `DATABASE_URL`: (PostgreSQL connection string from Render/Railway/Neon)

#### Step 2: Deploy Frontend to Vercel
- Import repository into [Vercel](https://vercel.com).
- **Framework Preset**: Vite
- **Root Directory**: `./` (or `frontend`)
- **Build Command**: `pnpm --filter @workspace/college-events run build`
- **Output Directory**: `frontend/dist/public`
- **Environment Variable**:
  - `VITE_API_BASE_URL`: `https://your-backend-service.onrender.com`

---

### Option 3: Containerized Deployment (Docker & Docker Compose)

To run the complete production setup locally or on a Virtual Private Server (VPS / EC2):

```bash
docker compose up --build -d
```

This will launch PostgreSQL on port `5432` and the Django production container on port `8000`.

---

## 🛠️ Technology Stack

| Layer | Technology |
| --- | --- |
| **Frontend** | React 19, Vite, TypeScript, Wouter, Tailwind CSS, TanStack React Query |
| **Backend** | Python 3.11+, Django 5.2, Django REST Framework |
| **Authentication** | JWT with `djangorestframework-simplejwt` |
| **Database** | PostgreSQL (Production via `DATABASE_URL`) / SQLite (Local Development) |
| **API Contract** | OpenAPI 3.1 with Orval-generated React Query hooks |
| **Static Files** | WhiteNoise |
| **WSGI Server** | Gunicorn |

---

## ⚙️ Environment Variables Reference

### Backend Environment Variables (`backend/.env`)

| Variable | Required | Description | Example |
| --- | --- | --- | --- |
| `DJANGO_SECRET_KEY` | Yes (Prod) | Django encryption key | `random-50-char-secret-key` |
| `DJANGO_DEBUG` | Yes | `0` for production, `1` for dev | `0` |
| `ALLOWED_HOSTS` | Yes | Comma-separated allowed hosts | `campuspulse-backend.onrender.com,*` |
| `CORS_ALLOWED_ORIGINS` | No | Allowed frontend domains | `https://campuspulse.vercel.app` |
| `CSRF_TRUSTED_ORIGINS` | No | Trusted origins for CSRF | `https://campuspulse.vercel.app` |
| `DATABASE_URL` | No | PostgreSQL connection URL | `postgres://user:pass@host:5432/dbname` |

### Frontend Environment Variables (`frontend/.env`)

| Variable | Required | Description | Example |
| --- | --- | --- | --- |
| `VITE_API_BASE_URL` | Yes (Prod) | URL of deployed Django REST API | `https://campuspulse-backend.onrender.com` |

---

## 💻 Local Development Setup

1. **Clone Repository**:
   ```bash
   git clone https://github.com/madhumitha-42/CampusPulse-College-Event-Management-System.git
   cd Smart-College-Event-Participation-Management-System
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate

   pip install -r requirements.txt
   python manage.py migrate
   python manage.py load_demo_data
   python manage.py runserver 0.0.0.0:8000
   ```

3. **Frontend Setup**:
   ```bash
   pnpm install
   pnpm --filter @workspace/college-events run dev
   ```

---

## 🔑 Demo Credentials

Loaded automatically by `python manage.py load_demo_data`:

- **Coordinator / Admin**: `admin@campuspulse.demo` / `CampusDemo!2026`
- **Student**: `mira@campuspulse.demo` / `StudentDemo!2026`
- Additional demo students: `rohan@campuspulse.demo`, `diya@campuspulse.demo` (Same password: `StudentDemo!2026`)

---

## 🧪 Testing & Verification Commands

```bash
# Run backend unit tests
python backend/manage.py test core

# Check Django production readiness
python backend/manage.py check --deploy

# Build React frontend for production
pnpm --filter @workspace/college-events run build
```

---

## 📋 VSB Skill Vault Demonstration Walkthrough

When presenting this project during evaluation:

1. **Show Live Deployed URL**: Demonstrate that the frontend and backend are running live on cloud infrastructure (e.g. Render / Vercel) connected via `VITE_API_BASE_URL`.
2. **Student Event Registration Flow**:
   - Log in as student (`mira@campuspulse.demo`).
   - Browse events, use search and category filters.
   - Click **Register** on an upcoming event.
   - Show duplicate registration prevention (clicking Register again yields instant validation feedback).
3. **Coordinator Operations Flow**:
   - Log in as coordinator (`admin@campuspulse.demo`).
   - Access **Event Management** to create a new event or edit an existing one.
   - Access **Taxonomy / Categories** to create a new event category.
   - View **Participant Roster** and update attendance status (Registered -> Attended).
   - Show live **Dashboard Statistics** updating dynamically.
4. **Codebase & Architecture**:
   - Highlight clean REST API design in Django (`backend/core/views.py`).
   - Highlight TypeScript type-safety and generated API hooks (`lib/api-client-react`).
   - Point to test cases (`docs/TEST_CASES.md`) and API contract (`lib/api-spec/openapi.yaml`).