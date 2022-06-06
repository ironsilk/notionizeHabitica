# notionizeHabitica

Just a very simple Notion and Habitica wrapper i wrote in order to sync some tabits/tasks/goals between the two.

The Notion template can be found here: 
https://satisfying-plough-5e2.notion.site/1d5748d86c6e4324a26404cf5f7f693d?v=d7107daaab0d470aa98534436744e723

The script has mainly two functions:

- Runs once a minute (or any interval you want), compares the last_modified date of all database items
    and updates/creates/does nothing regarding the tasks present in Habitica. Once inserted, the Habitica
    task id will be migrated into Notion in the designated column.
- Collects all the challenges the user is part of and populates the options in the `ChallengeName` column
    in Notion. If the user populates that field, the new task will be assigned in that Challenge, else it
    will be just private to the user. 

Library has no error catching if you modify the template or populate with other kinds of data. Use at own
 risk, supplied as is. 

Wishlist:
- Backpopulate a statistics table in Notion with tasks completion history from Habitica.