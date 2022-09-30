import pymongo
import datetime
from tabulate import tabulate

client = pymongo.MongoClient(
    "mongodb+srv://USERNAME:PASSWORD@cluster0.jthrb.mongodb.net/?retryWrites=true&w=majority"
)
db = client['ENTER_DB_NAME']  # connect to the overall database
collection = db['ENTER_COLLECTION_NAME']  # connect to the table (subcategory)

today = datetime.datetime.today().replace(microsecond=0)


def view_specific(choice): # used to return the updated entry from update_delete()
    results = collection.find_one({"_id": choice})
    return results


def new_entry(user): # daily and date-specific entries can be made here
    post_count = collection.count_documents({})

    if user == 2:
        other_date_str = input("Enter the date for this entry (yyyy-mm-dd): ") + 'T00:00:00+00:00'
        other_date = datetime.datetime.strptime(other_date_str, '%Y-%m-%dT%H:%M:%S%z')

    total_sales = float(input("Enter the TOTAL SALES for the day: "))
    credit = float(input("Enter CREDIT sales: "))
    delivery = float(input("Enter DELIVERY sales: "))
    cash = float(input("Enter CASH sales: "))
    total = credit + delivery + cash

    try:
        post = {"_id": post_count, "date": other_date, "total_sales": total_sales,
                "credit": credit, "delivery": delivery, "cash": cash, "total": total}
    except:
        post = {"_id": post_count, "date": today, "total_sales": total_sales,
                "credit": credit, "delivery": delivery, "cash": cash, "total": total}

    collection.insert_one(post)

    print("")
    return menu()


def search(): # allows the user to find entries in a given timeframe, gives the option to calculate totals at the end
    from_date = '2022-07-29' + 'T00:00:00+00:00'
    to_date = '2022-08-30' + 'T23:59:59+00:00'
    flag = 1
    while flag == 1:
        try:
            from_str = input("Enter the initial date to query from (yyyy-mm-dd): ") + 'T00:00:00+00:00'
            to_str = input("Enter the final date to query from (yyyy-mm-dd): ") + 'T23:59:59+00:00'

            from_date = datetime.datetime.strptime(from_str, '%Y-%m-%dT%H:%M:%S%z')
            to_date = datetime.datetime.strptime(to_str, '%Y-%m-%dT%H:%M:%S%z')

            flag = 2
        except:
            print("Invalid response(s), try again")

    results = collection.find({"date": {"$gte": from_date, "$lte": to_date}})

    col_names = ["ID", "Date", "Total Sales", "Credit", "Delivery", "Cash", "Total"]

    for i in results:
        data = [[i["_id"],
                 i["date"],
                 i["total_sales"],
                 i["credit"],
                 i["delivery"],
                 i["cash"],
                 i["total"]]]
        print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))

    user = 0
    while (user < 1) or (user > 2):
        try:
            user = int(input("\nWould you like to calculate the grand totals for each category? (1 = yes/2 = no): "))
        except:
            print("Invalid response, try again.\n")

    if user == 1:
        results = collection.find({"date": {"$gte": from_date, "$lte": to_date}})
        ts_total = 0
        cr_total = 0
        d_total = 0
        ca_total = 0
        t_total = 0
        for i in results:
            ts_total += float(i["total_sales"])
            cr_total += float(i["credit"])
            d_total += float(i["delivery"])
            ca_total += float(i["cash"])
            t_total += float(i["total"])
        print(f"'Total Sales' Total: {ts_total}\n"
              f"'Credit' Total: {cr_total}\n"
              f"'Delivery' Total: {d_total}\n"
              f"'Cash' Total: {ca_total}\n"
              f"'Total' Total: {t_total}\n")
    else:
        pass

    print("")
    return menu()


def view_all(): # finds all entries in the collection and prints using tabulate (generates a table)
    if collection.count_documents({}) == 0:
        print("Nothing to display\n")
        return menu()
    results = collection.find().sort("date", -1)
    col_names = ["ID", "Date", "Total Sales", "Credit", "Delivery", "Cash", "Total"]

    for i in results:
        data = [[i["_id"],
                 i["date"],
                 i["total_sales"],
                 i["credit"],
                 i["delivery"],
                 i["cash"],
                 i["total"]]]
        print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))

    user = 0
    while (user < 1) or (user > 2):
        try:
            user = int(input("\nWould you like to calculate the grand totals for each category? (1 = yes/2 = no): "))
        except:
            print("Invalid response, try again.\n")

    if user == 1:
        results = collection.find()
        ts_total = 0
        cr_total = 0
        d_total = 0
        ca_total = 0
        t_total = 0
        for i in results:
            ts_total += float(i["total_sales"])
            cr_total += float(i["credit"])
            d_total += float(i["delivery"])
            ca_total += float(i["cash"])
            t_total += float(i["total"])
        print(f"'Total Sales' Total: {ts_total}\n"
              f"'Credit' Total: {cr_total}\n"
              f"'Delivery' Total: {d_total}\n"
              f"'Cash' Total: {ca_total}\n"
              f"'Total' Total: {t_total}\n")
    else:
        pass

    print("")
    return menu()


def update_delete(): # allows the user to edit any entries they have made
    user_id = -1
    while (user_id < 0) or (user_id > collection.count_documents({})):
        try:
            user_id = int(input("\nEnter the '_id' value for the entry you would like to modify: "))
        except:
            print("Invalid response, try again.\n")

    user = 0
    while (user < 1) or (user > 6):
        try:
            user = int(input("\nWhat would you like change? (1-6):\n"
                             "1. Date\n"
                             "2. Total Sales/Total\n"
                             "3. Credit\n"
                             "4. Delivery\n"
                             "5. Cash\n"
                             "6. Delete Entry\n"
                             "Enter response here: "))
        except:
            print("Invalid response, try again.\n")

    if user == 1:
        other_date_str = input("\nEnter the new date for this entry (yyyy-mm-dd): ") + 'T00:00:00+00:00'
        other_date = datetime.datetime.strptime(other_date_str, '%Y-%m-%dT%H:%M:%S%z')

        collection.update_one(
            {"_id": user_id},
            {"$set": {"date": other_date}}
        )
        print(f"\nSuccessfully modified entry, changed to:\n{view_specific(user_id)}\n")
    elif user == 2:
        new = float(input("\nEnter the new value for TOTAL SALES/TOTAL: "))
        collection.update_one(
            {"_id": user_id},
            {"$set": {"total_sales": new, "total": new}}
        )
        print(f"\nSuccessfully modified entry, changed to:\n{view_specific(user_id)}\n")
    elif user == 3:
        new = float(input("\nEnter the new value for CREDIT: "))
        collection.update_one(
            {"_id": user_id},
            {"$set": {"credit": new}}
        )
        print(f"\nSuccessfully modified entry, changed to:\n{view_specific(user_id)}\n")
    elif user == 4:
        new = float(input("\nEnter the new value for DELIVERY: "))
        collection.update_one(
            {"_id": user_id},
            {"$set": {"delivery": new}}
        )
        print(f"\nSuccessfully modified entry, changed to:\n{view_specific(user_id)}\n")
    elif user == 5:
        new = float(input("\nEnter the new value for CASH: "))
        collection.update_one(
            {"_id": user_id},
            {"$set": {"cash": new}}
        )
        print(f"\nSuccessfully modified entry, changed to:\n{view_specific(user_id)}\n")
    else:
        ask = 0
        while (ask < 1) or (ask > 2):
            try:
                ask = int(input("\nAre you sure you want to delete this entry? (1 for yes, 2 for no): "))
            except:
                print("Invalid response, try again.\n")
        if ask == 1:
            collection.delete_one({"_id": user_id})
            print(f"\nSuccessfully deleted entry with ID: {user_id}\n")
        else:
            pass

    return menu()

def backup(): # creates a new file (or overwrites an existing one) with entries using the user-specified timeframe
    from_date = '2022-07-29' + 'T00:00:00+00:00'
    to_date = '2022-08-30' + 'T23:59:59+00:00'
    file_name = ""
    file_from = ""
    file_to = ""
    flag = 1
    while flag == 1:
        try:
            file_from = input("Enter the initial date to query from (yyyy-mm-dd): ")
            from_str = file_from + 'T00:00:00+00:00'
            file_to = input("Enter the final date to query from (yyyy-mm-dd): ")
            to_str = file_to + 'T23:59:59+00:00'

            from_date = datetime.datetime.strptime(from_str, '%Y-%m-%dT%H:%M:%S%z')
            to_date = datetime.datetime.strptime(to_str, '%Y-%m-%dT%H:%M:%S%z')

            flag = 2
        except:
            print("Invalid response(s), try again")

    results = collection.find({"date": {"$gte": from_date, "$lte": to_date}})
    col_names = ["ID", "Date", "Total Sales", "Credit", "Delivery", "Cash", "Total"]

    file_name = file_from + "_to_" + file_to
    file = open(file_name, "w")
    for i in results:
        data = [[i["_id"],
                 i["date"],
                 i["total_sales"],
                 i["credit"],
                 i["delivery"],
                 i["cash"],
                 i["total"]]]
        file.write(tabulate(data, headers=col_names))
        file.write("\n\n")
    file.close()

    print("")
    return menu()


def menu(): # user interface to select options
    print("1. New Daily Entry\n2. Specific Entry (not today)\n3. Search\n4. View All\n"
          "5. Update/Delete Entries\n6. Backup Entries to New File\n7. Exit Program")
    if collection.count_documents({}) % 31 == 0:
        print("\n\n\nNOTE: It is highly recommended to backup data to a separate file."
              "\nPlease enter \"6\" when prompted.")

    user = 0
    while (user < 1) or (user > 7):
        try:
            user = int(input("\nChoose options 1-7: "))
        except:
            print("Invalid response, try again.\n")

    if user == 1:
        new_entry(user)
    elif user == 2:
        new_entry(user)
    elif user == 3:
        search()
    elif user == 4:
        view_all()
    elif user == 5:
        update_delete()
    elif user == 6:
        backup()
    else:
        exit()


menu()
