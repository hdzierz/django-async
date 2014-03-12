"""
    Tests for the flush queue management command.
"""
from django.test import TestCase
from django.core import management

from async.api import schedule
from async.models import Job, Group


def do_job():
    pass


class TestFlushQueue(TestCase):
    def setUp(self):
        self.group = Group.objects.create(reference='1of2')
        self.j1 = schedule(do_job, group=self.group)
        self.j2 = schedule(do_job, group=self.group)

    def test_0of2(self):
        management.call_command('flush_queue', which=0, outof=2)
        j1 = Job.objects.get(pk=self.j1.pk)
        j2 = Job.objects.get(pk=self.j2.pk)
        if ( j1.pk %2 ):
            self.assertIsNone(j1.executed)
            self.assertIsNotNone(j2.executed)
        else:
            self.assertIsNotNone(j1.executed)
            self.assertIsNone(j2.executed)

    def test_1of2(self):
        management.call_command('flush_queue', which=1, outof=2)
        j1 = Job.objects.get(pk=self.j1.pk)
        j2 = Job.objects.get(pk=self.j2.pk)
        if ( j1.pk %2 ):
            self.assertIsNotNone(j1.executed)
            self.assertIsNone(j2.executed)
        else:
            self.assertIsNone(j1.executed)
            self.assertIsNotNone(j2.executed)

    def test_2of2(self):
        management.call_command('flush_queue', which=2, outof=2)
        j1 = Job.objects.get(pk=self.j1.pk)
        j2 = Job.objects.get(pk=self.j2.pk)
        if ( j1.pk %2 ):
            self.assertIsNone(j1.executed)
            self.assertIsNotNone(j2.executed)
        else:
            self.assertIsNotNone(j1.executed)
            self.assertIsNone(j2.executed)
