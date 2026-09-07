# Household Chore Tracker

A local web app for tracking shared household chores, assigned to household members, with support for recurring schedules.
Visit https://ai-native-developer-workflow.onrender.com . Deployment could take few minutes.


See [`_docs/plan.md`](_docs/plan.md) for the full spec and [`_docs/backlog.md`](_docs/backlog.md) for the build backlog.

## Requirements

- Python 3.10+

## Installation

```bash
# Clone the repo
git clone https://github.com/rahimcc/AI-Native-Developer-Workflow-.git
cd AI-Native-Developer-Workflow-

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up the database
python manage.py migrate
```

## Running the app

```bash
source venv/bin/activate
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. The chore list is the homepage.

## Usage

- **Chores** (homepage, `/`): add, edit, delete, filter by member, sort by due date or member, and mark chores complete.
  - Set "Repeat every N days" when adding a chore to make it recurring (e.g. 1 = daily, 7 = weekly). Leave it blank for a one-off chore.
  - Marking a **recurring** chore complete advances its due date by N days and keeps it in the list.
  - Marking a **one-off** chore complete removes it from the list.
- **Members** (`/members/`): add, edit, and delete household members. No login is required — anyone using the app can act as any member.
- **Admin** (`/admin/`): Django admin for direct data inspection/editing. Create a superuser first:
  ```bash
  python manage.py createsuperuser
  ```

## Running tests

```bash
source venv/bin/activate
python manage.py test chores
```
