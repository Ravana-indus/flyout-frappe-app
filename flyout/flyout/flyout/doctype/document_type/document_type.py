# Copyright (c) 2025, Ravana Industries Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint

ALLOWED_CATEGORIES = ("Identity", "Educational", "Financial", "Medical", "Legal", "Other")


class DocumentType(Document):
    """Defines a type of document that may be requested for a service.

    Validates the uniqueness of document names, allowed categories and
    positive validity periods.
    """

    def validate(self):
        """Validate document fields before saving."""
        self._validate_document_name()
        self._validate_category()
        self._validate_validity_period()

    def _validate_document_name(self):
        self.document_name = (self.document_name or "").strip()
        if not self.document_name:
            frappe.throw(_("Document Name is required"))

        if frappe.db.exists(
            "Document Type",
            {"document_name": self.document_name, "name": ("!=", self.name)},
        ):
            frappe.throw(_("Document Type with this name already exists"))

    def _validate_category(self):
        if self.category and self.category not in ALLOWED_CATEGORIES:
            frappe.throw(_("Invalid Category: {0}").format(self.category))

    def _validate_validity_period(self):
        if self.validity_period:
            if cint(self.validity_period) <= 0:
                frappe.throw(_("Validity Period must be a positive number of days"))
