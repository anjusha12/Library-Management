// Copyright (c) 2024, anjusha and contributors
// For license information, please see license.txt

frappe.query_reports["Articles Report"] = {
	"filters": [
		    {
            "fieldname": "article_name",
            "label": __("ID"),
            "fieldtype": "Link",
						"options":"Article",
            "width": 250
        },
		    {
            "fieldname": "author",
            "label": __("Author"),
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "publisher",
            "label": __("Publisher"),
            "fieldtype": "Data",
            "width": 250
        },
		    {
            "fieldname": "isbn",
            "label": __("ISBN"),
            "fieldtype": "Data",
            "width": 250
        }
	]
};
