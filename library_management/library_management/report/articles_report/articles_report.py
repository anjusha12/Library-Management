# Copyright (c) 2024, anjusha and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe import _
def execute(filters=None):
    columns, data= get_columns(filters), get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [
        {
            "fieldname": "article_name",
            "label": _("ID"),
            "fieldtype": "Data",
            "width": 250
        },
		{
            "fieldname": "author",
            "label": _("Author"),
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "publisher",
            "label": _("Publisher"),
            "fieldtype": "Data",
            "width": 250
        },
		 {
            "fieldname": "isbn",
            "label": _("ISBN"),
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "image",
            "label": _("Image"),
            "fieldtype": "Data",
            "width": 250
        },
        # {
        #     "fieldname": "price",
        #     "label": "Total Issues",
        #     "fieldtype": "Data",
        #     "width": 100
        # },
        # {
        #     "fieldname": "description",
        #     "label": "Description",
        #     "fieldtype": "Text Editor",
        #     "width": 100
        # },
        # # {
        #     "fieldname": "status",
        #     "label": "Current Status",
        #     "fieldtype": "Select",
        #     "width": 100
        # }
    ]
    return columns
def get_data(filters):
    filter_dict = {}

    if filters.name:
        filter_dict["article_name"] = filters.article_name

    if filters.author:
        filter_dict["author"] = ["like", f"%{filters.author}%"]

    if filters.publisher:
        filter_dict["publisher"] = ["like", f"%{filters.publisher}%"]

    if filters.isbn:
        filter_dict["isbn"] = ["like", f"%{filters.isbn}%"]

    if filters.status:
        filter_dict["status"] = ["like", f"%{filters.status}%"]

    if filters.get('image'):
        filter_dict["image"] = ["like", f"%{filters.image}%"]
	# if filters.get('price'):
    #     filter_dict["image"] = ["like", f"%{filters.price}%"]

    article_list = frappe.db.get_all("Article", filters=filter_dict, fields=["article_name", "author", "publisher", "isbn", "status", "image"])

    # for article in article_list:
    #     article['issued_transaction'] = frappe.db.count("Library Transaction", filters={"article": article['article_name'], 'docstatus': 1, 'type': "Issue"})
    #     article['returned_transaction'] = frappe.db.count("Library Transaction", filters={"article": article['article_name'], 'docstatus': 1, 'type': "Return"})
    #     article['current_status'] = "Issued" if article['status'] == "Issued" else "Available"

    return article_list

# def get_report_summary(filters):
#     available_book = frappe.db.count("Article", filters={"status": "Available"})
#     issued_book = frappe.db.count("Article", filters={"status": "Issued"})
#     transactions_on_issue = frappe.db.count("Library Transaction", filters={"type": "Issue"})
#     transactions_on_return = frappe.db.count("Library Transaction", filters={"type": "Return"})
#
#     return [
#         {
#             "value": available_book,
#             "label": _("Available Books"),
#             "indicator": "Blue",
#             "datatype": "Data"
#         },
#         {
#             "value": issued_book,
#             "label": _("Issued Books"),
#             "indicator": "Blue",
#             "datatype": "Data"
#         },
#         {
#             "value": transactions_on_issue,
#             "label": _("Transactions on Issue"),
#             "indicator": "Red",
#             "datatype": "Data"
#         },
#         {
#             "value": transactions_on_return,
#             "label": _("Transactions on Return"),
#             "indicator": "Red",
#             "datatype": "Data"
#         }
#     ]
