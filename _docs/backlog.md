# Backlog — Household Chore Tracker

Derived from [`plan.md`](./plan.md). Ordered so each item is buildable/testable on top of the previous ones.

## Epic 1: Project Setup
- [x] Install Django, create virtualenv, pin `requirements.txt`
- [x] Create `choretracker` project and `chores` app
- [x] Configure SQLite (default), run initial migrations
- [x] Verify dev server runs

## Epic 2: Data Model
- [x] `Member` model: `name`
- [x] `Chore` model: `title`, `description` (optional), `assigned_member` (FK → Member), `recurrence_days`, `due_date`
- [x] `CompletionLog` model (optional/history): `chore` (FK), `completed_by` (FK → Member), `completed_at`
- [x] Register models in `admin.py` for quick data entry/inspection
- [x] Create and run migrations

## Epic 3: Member Management
- [x] List members
- [x] Add member (name only)
- [x] Edit member
- [x] Delete member
- [x] Basic templates (no auth required)

## Epic 4: Chore CRUD
- [x] Add chore (title, description, assigned member, recurrence rule, due date)
- [x] Edit chore
- [x] Delete chore
- [x] Chore list view — homepage, shows all chores with due dates
- [x] Filter/sort chore list by member and/or due date

## Epic 5: Recurrence Logic
- [x] Define supported recurrence rules (e.g. daily, weekly, every N days) — via `recurrence_days` integer
- [x] "Mark complete" action on a chore
- [x] On completion: compute next due date from recurrence rule, update chore (or create next occurrence)
- [x] Log completion to `CompletionLog` for history

## Epic 6: UI Polish
- [x] Base template/layout shared across pages
- [x] Minimal styling (readable list, forms)
- [x] Empty states (no members yet, no chores yet)

## Epic 7: Testing
- [x] Model tests: recurrence date calculation
- [x] View tests: CRUD for members and chores
- [x] View tests: mark-complete flow generates correct next occurrence

## Out of Scope (explicitly excluded per plan.md)
- Authentication / login
- Points, streaks, or rewards
- Automatic rotation of chores between members
- Notifications/reminders
- "Due today / overdue" dashboard view
