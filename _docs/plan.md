# Household Chore Tracker — Specification

## Overview
A local web app for tracking shared household chores. Only one person (the user) operates the app, but chores are tracked per household member.

## Stack
- **Backend**: Django
- **Database**: SQLite
- **Interface**: Local web app (no auth/login)

## Scope

### Household Members
- Simple CRUD (create, edit, delete)
- Fields: name only
- No accounts, no passwords — just a name picker used when assigning/completing chores

### Chores
- Fields:
  - Title
  - Description (optional)
  - Assigned member
  - Recurrence rule (e.g. daily, weekly, every N days)
  - Due date
- Full CRUD (add/edit/delete)

### Recurrence
- Chores support recurring schedules (e.g. "vacuum every Monday", "trash every 3 days")
- Marking a chore complete automatically generates the next occurrence based on its recurrence rule

### Views
- **Full chore list**: shows all chores with due dates visible; filterable/sortable by member or date
- **Add/edit/delete chore** form
- **Mark complete** action on each chore

## Explicitly Out of Scope
- Authentication / login
- Points, streaks, or rewards system
- Automatic rotation of chores between members
- Notifications/reminders
- "Due today / overdue" dashboard — homepage is just the full chore list

## Data Model (tentative)
- **Member**: id, name
- **Chore**: id, title, description, assigned_member (FK → Member), recurrence_rule, due_date
- **CompletionLog** (optional, for history): id, chore (FK), completed_by (FK → Member), completed_at
