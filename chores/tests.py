from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Chore, CompletionLog, Member


class MemberModelTests(TestCase):
    def test_str_returns_name(self):
        member = Member.objects.create(name="Alex")
        self.assertEqual(str(member), "Alex")

    def test_create_and_retrieve_member(self):
        Member.objects.create(name="Sam")
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.first().name, "Sam")


class ChoreModelTests(TestCase):
    def test_str_returns_title(self):
        chore = Chore.objects.create(title="Vacuum", due_date=date(2026, 9, 8))
        self.assertEqual(str(chore), "Vacuum")

    def test_create_chore_with_assigned_member(self):
        member = Member.objects.create(name="Alex")
        chore = Chore.objects.create(
            title="Trash",
            assigned_member=member,
            recurrence_days=3,
            due_date=date(2026, 9, 10),
        )
        self.assertEqual(chore.assigned_member, member)
        self.assertEqual(chore.recurrence_days, 3)

    def test_description_and_recurrence_days_are_optional(self):
        chore = Chore.objects.create(title="One-off task", due_date=date(2026, 9, 8))
        self.assertEqual(chore.description, "")
        self.assertIsNone(chore.recurrence_days)
        self.assertIsNone(chore.assigned_member)

    def test_deleting_member_unassigns_chore_instead_of_deleting_it(self):
        member = Member.objects.create(name="Sam")
        chore = Chore.objects.create(
            title="Dishes", assigned_member=member, due_date=date(2026, 9, 8)
        )
        member.delete()
        chore.refresh_from_db()
        self.assertIsNone(chore.assigned_member)

    def test_recurrence_days_of_zero_fails_validation(self):
        chore = Chore(title="Bad", due_date=date(2026, 9, 8), recurrence_days=0)
        with self.assertRaises(ValidationError):
            chore.full_clean()


class CompletionLogModelTests(TestCase):
    def test_str_includes_chore_title_and_timestamp(self):
        chore = Chore.objects.create(title="Vacuum", due_date=date(2026, 9, 8))
        log = CompletionLog.objects.create(chore=chore)
        self.assertIn("Vacuum", str(log))

    def test_deleting_chore_keeps_log_with_title_snapshot(self):
        chore = Chore.objects.create(title="Trash", due_date=date(2026, 9, 8))
        log = CompletionLog.objects.create(chore=chore)
        chore.delete()
        log.refresh_from_db()
        self.assertIsNone(log.chore)
        self.assertEqual(log.chore_title, "Trash")

    def test_deleting_member_keeps_log_but_unsets_completed_by(self):
        member = Member.objects.create(name="Sam")
        chore = Chore.objects.create(title="Dishes", due_date=date(2026, 9, 8))
        log = CompletionLog.objects.create(chore=chore, completed_by=member)
        member.delete()
        log.refresh_from_db()
        self.assertIsNone(log.completed_by)


class MemberViewTests(TestCase):
    def test_list_shows_all_members(self):
        Member.objects.create(name="Alex")
        Member.objects.create(name="Sam")
        response = self.client.get(reverse("chores:member_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alex")
        self.assertContains(response, "Sam")

    def test_add_member_with_valid_data(self):
        response = self.client.post(reverse("chores:member_add"), {"name": "Jordan"})
        self.assertRedirects(response, reverse("chores:member_list"))
        self.assertTrue(Member.objects.filter(name="Jordan").exists())

    def test_add_member_with_blank_name_is_not_saved(self):
        response = self.client.post(reverse("chores:member_add"), {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Member.objects.count(), 0)

    def test_edit_member_persists_change(self):
        member = Member.objects.create(name="Alex")
        response = self.client.post(
            reverse("chores:member_edit", args=[member.pk]), {"name": "Alexandra"}
        )
        self.assertRedirects(response, reverse("chores:member_list"))
        member.refresh_from_db()
        self.assertEqual(member.name, "Alexandra")

    def test_delete_member_removes_it(self):
        member = Member.objects.create(name="Alex")
        response = self.client.post(reverse("chores:member_delete", args=[member.pk]))
        self.assertRedirects(response, reverse("chores:member_list"))
        self.assertFalse(Member.objects.filter(pk=member.pk).exists())

    def test_delete_confirmation_page_does_not_delete_on_get(self):
        member = Member.objects.create(name="Alex")
        response = self.client.get(reverse("chores:member_delete", args=[member.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Member.objects.filter(pk=member.pk).exists())

    def test_delete_confirmation_warns_about_assigned_chores(self):
        member = Member.objects.create(name="Alex")
        Chore.objects.create(title="Vacuum", assigned_member=member, due_date=date(2026, 9, 8))
        response = self.client.get(reverse("chores:member_delete", args=[member.pk]))
        self.assertContains(response, "assigned to 1 chore")


class ChoreViewTests(TestCase):
    def test_list_shows_all_chores_with_due_dates(self):
        Chore.objects.create(title="Vacuum", due_date=date(2026, 9, 8))
        Chore.objects.create(title="Trash", due_date=date(2026, 9, 10))
        response = self.client.get(reverse("chores:chore_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vacuum")
        self.assertContains(response, "Trash")

    def test_add_chore_with_valid_data(self):
        member = Member.objects.create(name="Alex")
        response = self.client.post(
            reverse("chores:chore_add"),
            {
                "title": "Dishes",
                "description": "",
                "assigned_member": member.pk,
                "recurrence_days": 1,
                "due_date": "2026-09-08",
            },
        )
        self.assertRedirects(response, reverse("chores:chore_list"))
        chore = Chore.objects.get(title="Dishes")
        self.assertEqual(chore.assigned_member, member)
        self.assertEqual(chore.recurrence_days, 1)

    def test_add_chore_missing_due_date_is_not_saved(self):
        response = self.client.post(reverse("chores:chore_add"), {"title": "Dishes"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Chore.objects.count(), 0)

    def test_add_chore_with_recurrence_days_zero_is_not_saved(self):
        response = self.client.post(
            reverse("chores:chore_add"),
            {"title": "Dishes", "recurrence_days": 0, "due_date": "2026-09-08"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Chore.objects.count(), 0)

    def test_edit_chore_persists_change(self):
        chore = Chore.objects.create(title="Vacuum", due_date=date(2026, 9, 8))
        response = self.client.post(
            reverse("chores:chore_edit", args=[chore.pk]),
            {
                "title": "Vacuum living room",
                "description": "",
                "assigned_member": "",
                "recurrence_days": "",
                "due_date": "2026-09-09",
            },
        )
        self.assertRedirects(response, reverse("chores:chore_list"))
        chore.refresh_from_db()
        self.assertEqual(chore.title, "Vacuum living room")
        self.assertEqual(chore.due_date, date(2026, 9, 9))

    def test_delete_chore_removes_it(self):
        chore = Chore.objects.create(title="Vacuum", due_date=date(2026, 9, 8))
        response = self.client.post(reverse("chores:chore_delete", args=[chore.pk]))
        self.assertRedirects(response, reverse("chores:chore_list"))
        self.assertFalse(Chore.objects.filter(pk=chore.pk).exists())

    def test_filter_by_member_returns_only_their_chores(self):
        alex = Member.objects.create(name="Alex")
        sam = Member.objects.create(name="Sam")
        Chore.objects.create(title="Vacuum", assigned_member=alex, due_date=date(2026, 9, 8))
        Chore.objects.create(title="Trash", assigned_member=sam, due_date=date(2026, 9, 9))

        response = self.client.get(reverse("chores:chore_list"), {"member": alex.pk})

        self.assertContains(response, "Vacuum")
        self.assertNotContains(response, "Trash")

    def test_sort_by_due_date_orders_ascending(self):
        Chore.objects.create(title="Later", due_date=date(2026, 9, 15))
        Chore.objects.create(title="Sooner", due_date=date(2026, 9, 8))

        response = self.client.get(reverse("chores:chore_list"), {"sort": "due_date"})

        titles = [c.title for c in response.context["chores"]]
        self.assertEqual(titles, ["Sooner", "Later"])

    def test_sort_by_member_orders_alphabetically(self):
        alex = Member.objects.create(name="Alex")
        sam = Member.objects.create(name="Sam")
        Chore.objects.create(title="Trash", assigned_member=sam, due_date=date(2026, 9, 8))
        Chore.objects.create(title="Vacuum", assigned_member=alex, due_date=date(2026, 9, 8))

        response = self.client.get(reverse("chores:chore_list"), {"sort": "member"})

        titles = [c.title for c in response.context["chores"]]
        self.assertEqual(titles, ["Vacuum", "Trash"])


class ChoreCompleteViewTests(TestCase):
    def test_completing_recurring_chore_advances_due_date_by_recurrence_days(self):
        chore = Chore.objects.create(
            title="Vacuum", due_date=date(2026, 9, 8), recurrence_days=7
        )
        response = self.client.post(reverse("chores:chore_complete", args=[chore.pk]))
        self.assertRedirects(response, reverse("chores:chore_list"))
        chore.refresh_from_db()
        self.assertEqual(chore.due_date, date(2026, 9, 15))

    def test_completing_recurring_chore_keeps_it_in_the_list(self):
        chore = Chore.objects.create(
            title="Vacuum", due_date=date(2026, 9, 8), recurrence_days=1
        )
        self.client.post(reverse("chores:chore_complete", args=[chore.pk]))
        self.assertTrue(Chore.objects.filter(pk=chore.pk).exists())

    def test_completing_one_off_chore_removes_it(self):
        chore = Chore.objects.create(title="Fix faucet", due_date=date(2026, 9, 8))
        response = self.client.post(reverse("chores:chore_complete", args=[chore.pk]))
        self.assertRedirects(response, reverse("chores:chore_list"))
        self.assertFalse(Chore.objects.filter(pk=chore.pk).exists())

    def test_completing_chore_logs_completion_with_assigned_member(self):
        member = Member.objects.create(name="Alex")
        chore = Chore.objects.create(
            title="Dishes", due_date=date(2026, 9, 8), assigned_member=member
        )
        self.client.post(reverse("chores:chore_complete", args=[chore.pk]))
        log = CompletionLog.objects.get(chore_title="Dishes")
        self.assertEqual(log.completed_by, member)

    def test_completing_one_off_chore_preserves_log_after_deletion(self):
        chore = Chore.objects.create(title="Fix faucet", due_date=date(2026, 9, 8))
        self.client.post(reverse("chores:chore_complete", args=[chore.pk]))
        log = CompletionLog.objects.get(chore_title="Fix faucet")
        self.assertIsNone(log.chore)

    def test_complete_requires_post(self):
        chore = Chore.objects.create(title="Vacuum", due_date=date(2026, 9, 8))
        response = self.client.get(reverse("chores:chore_complete", args=[chore.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Chore.objects.filter(pk=chore.pk).exists())
