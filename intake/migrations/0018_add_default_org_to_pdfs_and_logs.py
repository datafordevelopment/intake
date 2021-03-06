# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-12 23:03
from __future__ import unicode_literals

from django.db import migrations


def add_sf_to_pdfs_and_logs(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Organization = apps.get_model('user_accounts', 'Organization')
    san_francisco_pub_def = Organization.objects.using(db_alias).filter(
        name="San Francisco Public Defender").first()
    FillablePDF = apps.get_model('intake', 'FillablePDF')
    pdfs = FillablePDF.objects.using(db_alias).all()
    for pdf in pdfs:
        if not pdf.organization:
            pdf.organization = san_francisco_pub_def
            pdf.save()
    ApplicationLogEntry = apps.get_model('intake', 'ApplicationLogEntry')
    logs = ApplicationLogEntry.objects.using(db_alias).filter(
        event_type__in=[1, 2, 3])
    for log in logs:
        if not log.organization:
            log.organization = san_francisco_pub_def
            log.save()


def remove_sf_from_pdfs_and_logs(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Organization = apps.get_model('user_accounts', 'Organization')
    san_francisco_pub_def = Organization.objects.using(db_alias).filter(
        name="San Francisco Public Defender").first()
    FillablePDF = apps.get_model('intake', 'FillablePDF')
    pdfs = FillablePDF.objects.using(db_alias).all()
    for pdf in pdfs:
        if pdf.organization == san_francisco_pub_def:
            pdf.organization = None
            pdf.save()
    ApplicationLogEntry = apps.get_model('intake', 'ApplicationLogEntry')
    logs = ApplicationLogEntry.objects.using(db_alias).filter(
        event_type__in=[1, 2, 3])
    for log in logs:
        if log.organization == san_francisco_pub_def:
            log.organization = None
            log.save()


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0017_fillablepdf_organization'),
        ('user_accounts', '0007_add_profiles_related_name_to_organization'),
    ]

    operations = [
        migrations.RunPython(add_sf_to_pdfs_and_logs, remove_sf_from_pdfs_and_logs)
    ]
