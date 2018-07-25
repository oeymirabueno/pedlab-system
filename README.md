# pedlab-system
Timesheet System for PedLab.

This Django Project uses the following versions:
* Django 1.11.10
* Python 2.7.15

The current System has the following complete functions:
* timesheet (in and out)
* viewing and printing records
* payment approval
* viewing and printing payments
* adding, editing, and deleting users
* admin access to Django admin site
* user restrictions

The following functions were attempted during the development but were not completed/successfully implemented:
* sending email confirmation for adding new users (Test Mail button in admin view was used to debug and test)
   * this is due to issues with smtp.gmail.com as an email host
   * other hosting servers were not tested out
* 'forgot password?' link on login page

The following functions are aimed for a second phase of development:
* deliverable uploading
* productivity monitoring
