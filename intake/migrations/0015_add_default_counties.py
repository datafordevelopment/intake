# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class UpdateCounties:
    def __init__(self):
        self.apps = None
        self.schema_editor = None
        self.db_alias = None
        self.default_county_id = None

    def get_orgs(self):
        return self.model_manager_for('user_accounts', 'Organization')

    def get_counties(self):
        return self.model_manager_for('intake', 'County')

    def update_apps(self, apps, schema_editor):
        self.apps = apps
        self.schema_editor = schema_editor
        self.db_alias = schema_editor.connection.alias

    def model_manager_for(self, *args):
        model = self.apps.get_model(*args)
        return model.objects.using(self.db_alias)

    def update_or_create_objects(self, model, data):
        instances = data['instances']
        lookup_keys = data.get('lookup_keys', ['pk'])
        for instance_data in instances:
            atts = instance_data.copy()
            lookup_atts = {k: atts[k] for k in lookup_keys}
            atts.pop("pk", None)
            instance, created = model.update_or_create(
                **lookup_atts,
                defaults=atts)

    def load_counties(self):
        from intake.initial_data.counties import data
        from intake.constants import Counties
        self.update_or_create_objects(self.get_counties(), data)
        for obj in data['instances']:
            if obj['slug'] == Counties.SAN_FRANCISCO:
                self.default_county_id = obj['pk']

    def link_orgs_to_counties(self):
        from intake.initial_data.organizations import data
        self.update_or_create_objects(self.get_orgs(), data)

    def link_existing_submissions_to_sanfrancisco(self):
        Submissions = self.model_manager_for('intake', 'FormSubmission')
        for sub in Submissions.all():
            if not sub.counties.all():
                sub.counties.add(
                    self.default_county_id)

    def unlink_submissions_from_counties(self):
        Submissions = self.model_manager_for('intake', 'FormSubmission')
        for sub in Submissions.all():
            sub.counties.clear()

    def unlink_orgs_from_counties(self):
        for org in self.get_orgs().all():
            if org.county: 
                org.county = None
                org.save()

    def delete_counties(self):
        self.get_counties().all().delete()

    def forward(self, *args):
        self.update_apps(*args)
        self.load_counties()
        self.link_orgs_to_counties()
        self.link_existing_submissions_to_sanfrancisco()

    def reverse(self, *args):
        self.update_apps(*args)
        self.unlink_submissions_from_counties()
        self.unlink_orgs_from_counties()
        self.delete_counties()



county_migrator = UpdateCounties()


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0014_county_name'),
        ('user_accounts', '0006_add_county_model'),
    ]

    operations = [
        migrations.RunPython(county_migrator.forward, county_migrator.reverse)
    ]
