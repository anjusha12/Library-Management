
frappe.ui.form.on('Library Transaction', {
    refresh: function(frm) {
        frm.add_custom_button(' Fine', () => {
          d = new frappe.ui.Dialog({
              title: 'Pay Fine',
              fields: [
                  {
                      label: 'Amount',
                      fieldname: 'amount',
                      fieldtype: 'Currency'
                  },
                  {
                      label: 'Date',
                      fieldname: 'date',
                      fieldtype: 'Date'
                  }

              ],
              size: 'small',
              primary_action_label: 'Paid',
              primary_action(values) {
                  console.log(values);
                  d.hide();
              }
          });

          d.show();

        })
        frm.set_query('article', () => {
          return {
            filters: {
              status: 'Available'
        }
    }
})
        // frm.set_query('article', () => {
        //             return {
        //               query: 'ibrary_management.library_management.doctype.library_transaction.library_transaction.custom_article_query'
        //        }
        //   })

      },


});
