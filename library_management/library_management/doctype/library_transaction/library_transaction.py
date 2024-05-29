import frappe
from frappe.model.document import Document

class LibraryTransaction(Document):
    def before_save(self):
        self.calc_delay_fine()

    def before_submit(self):
        if self.type == "Issue":
            # self.validate_issue()
            # self.validate_maximum_limit()
            self.validate_membership()
            self.validate_issued()
            self.update_article_list()
            # set the article status to be Issued
            for row in self.article_list:
                article = frappe.get_doc("Article", row.article)
                article.status = "Issued"
                article.save()

        elif self.type == "Return":
            self.validate_return()
            self.calc_delay_fine()
            damage_fine=int(self.damage_fine) if self.damage_fine else 0
            self.total_fine=self.delay_fine + damage_fine
            self.remove_articles()
            # set the article status to be Available
            for row in self.article_list:
                article = frappe.get_doc("Article", row.article)
                article.status = "Available"
                article.save()

    def update_article_list(self):
        # Fetch the Library Member document
        library_member = frappe.get_doc("Library Member", self.library_member)

    # Iterate through article_list and add issued articles to Article List
        if self.type == "Issue":
            for row in self.article_list:
                article = frappe.get_doc("Article", row.article)
                library_member.append("article_list", {
                    "article": article.name,
                    # "issue_date": self.date,
                    # "due_date": self.due_date  # Ensure these fields exist in your doctype
                    })

        # Save the updated Library Member document
        library_member.save()


    def remove_articles(self):
    # Fetch the Library Member document
        library_member = frappe.get_doc("Library Member", self.library_member)

    # Check if the document was found
        if library_member:
            articles_found = False
        # Create a list of articles to remove
            articles_to_remove = [row.article for row in self.article_list]

        # Iterate through the "Article List" child table entries
            article_list = library_member.get("article_list")
            for article_entry in list(article_list):
                if article_entry.article in articles_to_remove:
                # Remove the article entry from the "Article List" child table
                    article_list.remove(article_entry)
                    articles_found = True

            if articles_found:
            # Save the updated Library Member document
                library_member.save()
                frappe.msgprint("Articles returned successfully.")
            else:
                frappe.msgprint("Articles not found in the library member's article list.")
        else:
            frappe.throw("Library Member not found")


    # def validate_issue(self):
    #     self.validate_membership()
    #     for row in self.article_list:
    #         article = frappe.get_doc("Article", row.article)
    #         # article cannot be issued if it is already issued
    #         if article.status == "Issued":
    #             frappe.throw("Article is already issued by another member")

    def validate_return(self):
        for row in self.article_list:
            article = frappe.get_doc("Article", row.article)
            # article cannot be returned if it is not issued first
            if article.status == "Available":
                frappe.throw("Article cannot be returned without being issued first")

    # def validate_maximum_limit(self):
    # # Fetch the maximum number of articles allowed from Library Settings
    #     max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
    #
    # # Count the number of issued transactions for the library member
    #     count = frappe.db.count(
    #         "Library Transaction",
    #         filters={
    #             "library_member": self.library_member,
    #             "type": "Issue",
    #             "docstatus": 1
    #         }
    #     )
    #
    # # If the count exceeds or equals the maximum, throw an exception
    #     if count >= max_articles:
    #         frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        # check if a valid membership exist for this library member
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "from_date": ("<=", self.date),
                "to_date": (">=", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")

    def validate_issued(self):
        # Validate membership
        self.validate_membership()
        # issued_count=[]
        # for row in self.article_list:
        #     issued_count.append(len(row.article))
        library_member = frappe.get_doc("Library Member", self.library_member)
        # Get the count of articles in the article_list child table
        issued_articles_count = len(library_member.article_list)
        print(issued_articles_count)


        # Check maximum number of issued articles
        issued_articles = frappe.db.get_single_value('Library Settings', 'max_articles')

        # # Find the count of issued articles for the member
        # issued_count = frappe.db.count('Library Transaction', {
        #     'library_member': self.library_member,
        #     'type': 'Issue',
        #     'docstatus': 1
        # })

        print(issued_articles_count, issued_articles)

        if issued_articles_count  >= issued_articles:
            frappe.throw('The member has already reached the maximum number of issued articles')

        # Check if the article is already issued
        for row in self.article_list:
            article = frappe.get_doc('Article', row.article)
            if article.status == 'Issued':
                frappe.throw('Article is already issued by another member')

    def calc_delay_fine(self):
        print("here")
        for row in self.article_list:
            valid_delayfine = frappe.db.exists(
                "Library Transaction",
                {
                    "library_member": self.library_member,
                    "article": row.article,
                    "docstatus": 1,
                    "type": "Issue",
                }
            )
            print(valid_delayfine, self.library_member, row.article)

            if valid_delayfine:
                print("Entering calc_delay_fine", self.library_member, row.article)
                # issued_doc = frappe.get_last_doc("Library Transaction", filters={"library_member": self.library_member, "article": row.article, "docstatus": 1, "type": "Issue"})
                # issued_date = issued_doc.date
                issued_date = frappe.db.get_value("Library Transaction", {"library_member": self.library_member, "article": row.article, "docstatus": 1, "type": "Issue"}, "date")
                loan_period = frappe.db.get_single_value('Library Settings', 'loan_period')
                actual_duration = frappe.utils.date_diff(self.date, issued_date)
                print(f"Issued Date: {issued_date}, Actual Duration: {actual_duration}, Loan Period: {loan_period}")

                if actual_duration > loan_period:
                    single_day_fine = frappe.db.get_single_value('Library Settings', 'single_day_fine')
                    self.delay_fine = single_day_fine * (actual_duration - loan_period)
                    print(f"Delay Fine Calculated: {self.delay_fine}")
                else:
                    self.delay_fine=0
                    print("No delay fine as actual duration is within the loan period")
            else:
                self.delay_fine=0
                print("No valid transaction found for delay fine")

    @frappe.whitelist()
    def custom_article_query(doctype, txt, searchfield, start, page_len, filters):
        # available_articles = frappe.get_all('Article',filters={'status': 'Available'})
        # return available_articles
        return None
