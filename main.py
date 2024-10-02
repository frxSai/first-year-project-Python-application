from firebase import firebase

url = 'https://ammunition-non.firebaseio.com/'
firebase = firebase.FirebaseApplication(url)

longrange = ["HDR", "RYTEC", "AX-50", "DRAGUNOV"]
shortrange = ["AN94", "ISO", "ASS VAL", "M4A1", "M16", "AK47"]
product_name = ["HDR", "RYTEC", "AX-50", "DRAGUNOV", "AN94", "ISO", "ASS VAL", "M4A1", "M16", "AK47"]
product_price = {"HDR": 4999,
                 "RYTEC": 1500,
                 "AX-50": 899,
                 "DRAGUNOV": 1500,
                 "AN94": 1000,
                 "ISO": 2200,
                 "ASS VAL": 1000,
                 "M4A1": 6000,
                 "M16": 4500,
                 "AK47": 1200}


def sale_menu():
    list_order = True
    p_name = product_name
    p_prize = product_price

    while list_order != False:
        print("-------Ammunition Vender:---------")
        print("-------Long Range Weapons:---------")
        print("1. HDR sniper rifle\t4999 $")
        print("2. RYTEC sniper rifle\t6000 $")
        print("3. AX-50 sniper rifle\t4500 $")
        print("4. DRAGUNOV sniper rifle\t1200 $")
        print("-------Short Range Weapons:---------")
        print("5. AN94 \t1250 $")
        print("6. ISO \t899 $")
        print("7. ASS VAL \t1500 $")
        print("8. M4A1 \t2200 $")
        print("9. M16 \t1000 $")
        print("10. AK47 \t1200 $")
        print("0. Main menu")
        print("-------End of list:-----------")

        dealer = int(input("Enter your order: "))
        if (dealer != 0):
            # name = input("Enter weapon name: ")
            item = int(input("Enter items: "))
            while (item <= 0):
                print("Incorrect amount of items")
                item = int(input("Enter items: "))
            range_of_weaps = 'long' if 1 <= dealer <= 4 else 'short'
            push_data(range_of_weaps, product_name[dealer - 1], item, product_price[product_name[dealer - 1]])
        else:
            list_order = False

def report_menu():
    list_order = True
    while list_order != False:
        print("-------Report menu:---------")
        print("1. Print transactions")
        print("2. Total sales")
        # print("4. Summary Items")
        print("0. Main menu")
        print("-------End menu:-----------")
        dealer = int(input("Enter menu: "))
        if (dealer == 1):
            show_tran()
        elif (dealer == 2):
            price = '{:,}'.format(show_tran(0))
            print("Total is ", price,'$.')
        # elif (menu==4):
        # summary_items()
        else:
            list_order = False

def main_menu():
    print("-------Main menu:---------")
    print("1. Firearm menu")
    print("2. Report menu")
    print("3. Clear DB")
    print("4. Exit")

def show_tran(printable = 1):
    long = (firebase.get('/long', None))
    short = firebase.get('/short', None)

    long_no = get_total('long')
    short_no = get_total('short')

    # for i in range(1,5):
    #     print(i) [1,4]
    # Espresso 20 items, total 800 B.
    items = 0
    total = 0

    # product_name = ["HDR", "RYTEC", "AX-50", "DRAGUNOV", "AN94", "ISO", "ASS VAL", "M4A1", "M16", "AK47"]
    total_product = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(1, long_no + 1):
        total_product[product_name.index(long[str(i)]['name'])] += long[str(i)]['amount']
    for i in range(1, short_no + 1):
        total_product[product_name.index(short[str(i)]['name'])] += short[str(i)]['amount']
    totalsale = 0
    position = 0
    for item in total_product:
        if item != 0:
            # price = '{:,}'.format(item * (product_price[product_name[position]])) #2.7

            value = item * (product_price[product_name[position]])  # 3.5 >>++
            price = f'{value:,}'  # 3.5 >>++
            if printable == 1:
                print(product_name[position], item, "items ,total", price, '$.')
            totalsale += value
        position += 1
    return totalsale

def get_total(type):  # Read total value
    trans_no = firebase.get('/' + type, 'key')
    return trans_no

def clear_db():
    trans_no = firebase.delete('/',None)
    if get_total('short') == None:
        result = initial_total('short', 0)
    if get_total('long') == None:
        result = initial_total('long', 0)

def initial_total(type, amount):
    result = firebase.put(type, 'key', amount)  # Initializing Amount of Transaction
    return result

def update_total(type, amount=0):  # update total transaction depends type

    trans = get_total(type)  # Check if exists value

    if trans == None:  # Not exists value
        result = initial_total(type, amount)
    else:
        trans_no = firebase.delete(type, 'key')
        result = firebase.put(type, 'key', amount)  # Put Amount of Transaction Short weapons

def push_data(type, weapons, amount, price):  # Push Data upto firebase

    # Calculation transaction number
    short_no = int(get_total('short'))
    long_no = int(get_total('long'))
    # print(short_no, long_no)

    # Last transaction suppose to be ?
    trans = short_no + 1 if type == 'short' else long_no + 1

    # Push up to firebase
    object = {
        'name': weapons,
        'amount': amount,
        'price': price,
        'total': price * amount,
    }
    update_total(type, trans)
    result = firebase.put(type, trans, object)

    return result

# tfl=tranforlong
# tfs=tranforshort

# print("Long Range Weapons",tfl)
# print("Short Range Weapons",tfs)

def main():
    _order = True
    if get_total('short') == None:
        result = initial_total('short', 0)
    if get_total('long') == None:
        result = initial_total('long', 0)

    while (_order != False):
        main_menu()
        sl = int(input("Enter order: "))
        if (sl == 1):
            sale_menu()
        elif (sl == 2):
            report_menu()
        elif (sl == 3):
            clear_db()
        else:
            print("Thank you")
            _order = False

    # print("\n",
    #       "Long Range Weapons", tfl, "\n",
    #       "Short Range Weapons", tfs)

if __name__ == "__main__":
    main()

long_range_HDR = \
    {
        'p_id': '001',
        "p_name": 'HDR',
        'piece': 1,
        'p_price': 4999,
        'totalpr': 4999
    }

# print("Long range",result1)
# print("Short Range",result2)
# print(result)
