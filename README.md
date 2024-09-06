# Sales-Database
### Enter and store information related to sales to quickly access through a database using pymongo

# Overview
![image](https://github.com/user-attachments/assets/cb7ca33e-ab8c-4101-9175-19750965e57e)

# Description
The databse connects to a MongoDB cluter. The daily entries are tailored to sales information. Each entry includes "Total Sales", "Credit", "Delivery", "Cash", and an automatically calculated *true* "Total" which adds the previous details for comparing the expected "Total Sales".

This database is to help transfer pencil-paper accounting to something more streamlined. The main program features 7 key functions: 
1. New Daily Entry (A habitual entry done per day)
2. Specific Entry (If entries had not been completed prior)
3. Search (Search a date range which prints all entries found between)
4. View All (Prints all entries in the database, good for relatively small clusters)
5. Update/Delete Entries (If an entry is incorrect, fix or delete it)
6. Backup Entries to New File (Every month the program prompts an automatic backup to a text file)
7. Exit Program (Disconnects client)

To connect to your personal cluster on MongoDB, follow their documentation: 
https://www.mongodb.com/resources/languages/pymongo-tutorial?msockid=35f0ce4bafa961870f7ddce3ae03602c

From my program, lines 5-9 need to be changed. The username, password, cluster name (2 spots), database name, and table (subcategory name).

# Technologies
I used the following to create this program:
- Python
- PyMongo
- Tabulate
- MongoDB

# Learnings
I built this during my managerial position at Subway. I saw how the other managers/franchisees kept track of sales through pencil-paper methods. I thought it was time for some modernization, so I decided to make a quick database which would just take sales information per day. I kept thinking of new features, like editing and backing up to a text file, so I continued building upon this program.

## "Why didn't I just use an Excel sheet?"
It's very easy to make a Excel sheet for the sales information per day. And Excel does have methods for some automation. However, a database is useful for a number of reasons over Excel. In my mind, this database is able to handle a lot more information without making it all look too bloated. In Excel, millions of rows worth of sales information is like a wall, and having to navigate to that position may slow down productivity. With this database, multiple users can have access and conduct complex queries efficiently.

Overall, it was a very enjoyable learning experience which gave me some insight into database production and management.

# Authorship

I developed this project myself and took feedback from supervisors. You can check out more of my work in my portfolio:

### [Visit my portfolio](https://portfolio-ompatel.netlify.app/)
