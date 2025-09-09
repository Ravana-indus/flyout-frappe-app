# Copyright (c) 2025, Ravana Industries Group and Contributors
# See license.txt

import frappe
from frappe.exceptions import MandatoryError
from frappe.tests import IntegrationTestCase

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class IntegrationTestAuditLog(IntegrationTestCase):
    """
    Integration tests for AuditLog.
    Use this class for testing interactions between multiple components.
    """

    def setUp(self):
        """Create a sample audit log entry for use in tests."""
        self.log = frappe.get_doc(
            {
                "doctype": "Audit Log",
                "action": "Create",
                "resource_type": "User",
                "resource_id": "USR-0001",
                "user_id": "test.user@example.com",
                "ip_address": "127.0.0.1",
                "user_agent": "pytest",
                "details": {"field": "value"},
            }
        ).insert()

    def tearDown(self):
        """Remove the sample audit log entry created for tests."""
        if self.log and frappe.db.exists("Audit Log", self.log.name):
            frappe.delete_doc("Audit Log", self.log.name)

    def test_creation_and_retrieval(self):
        """Ensure basic creation and retrieval works as expected."""
        doc = frappe.get_doc("Audit Log", self.log.name)
        self.assertEqual(doc.action, "Create")
        self.assertEqual(doc.resource_type, "User")
        self.assertEqual(doc.severity, "Info")
        self.assertEqual(doc.details, {"field": "value"})

    def test_update_severity(self):
        """Verify that updating a field persists to the database."""
        self.log.severity = "Warning"
        self.log.save()
        updated = frappe.get_doc("Audit Log", self.log.name)
        self.assertEqual(updated.severity, "Warning")

    def test_missing_required_fields(self):
        """Missing required fields should raise a validation error."""
        incomplete = frappe.get_doc({"doctype": "Audit Log", "resource_type": "User"})
        with self.assertRaises(MandatoryError):
            incomplete.insert()

