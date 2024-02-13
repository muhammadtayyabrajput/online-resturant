from flask import Flask, render_template, request, make_response, session, redirect, jsonify
from models import user, contact, orders, orders_items
from SMDBHandler import SMDBHandler
from flask_restful import Api
from resources import routes


app = Flask(__name__)
app.secret_key = "bsjvhusdhg5565645"

# flask API instance creation
api=Api(app)

# initiaize routes
routes.initialize_routes(api)



# Home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin')
def signIn():
    return render_template("login.html")


@app.route('/Update')
def Update():
    email = session.get("email")
    if email is None:
        return jsonify({"error": "User not logged in."}), 401
    return render_template("Update.html")

@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/loginForm', methods=['POST'])
def loginForm():
    try:
        email = request.form["userEmail"]
        pwd = request.form["userPassword"]
        handler = SMDBHandler("localhost", "root", "mysql123", "web_project_food")
        login = handler.login(email, pwd)
        if login:
            session["email"] = email
            return redirect("/order")
        else:
            return render_template("login.html",error="Wrong credentials")

    except Exception as e:
        return render_template("login.html")


@app.route('/RegisterForm', methods=['POST'])
def RegisterForm():
    try:
        uname = request.form["userName"]
        pwd = request.form['userConfirmPassword']
        email = request.form['userEmail']
        phone = request.form['userPhone']
        address = request.form['userAddress']
        city = request.form['userCity']
        
        handler = SMDBHandler("localhost", "root", "mysql123", "web_project_food")
        # print(handler)
        user_obj = user(uname, email, pwd)
        # print("user ", user)
        contact_obj = contact(email, address, phone, city)
        # print("contact ", contact)

        userValidity = handler.validateUser(user_obj)
        if userValidity == False:
            flag_register = handler.registerUser(user_obj, contact_obj)
            
            if flag_register:
                return redirect("/signin")
            else:
                return redirect("/index")
        else:
            return render_template("register.html", userValidity=userValidity)

    except Exception as e:
        return render_template("index.html")


# About Us page
@app.route('/about')
def AboutUs():
    return render_template('about.html')


# index page
@app.route('/index')
def index1():
    return render_template('index.html')


# donate page
@app.route('/donate')
def donate():
    return render_template('donate.html')


# Order  page
@app.route('/order')
def order1():
    email = session.get("email")
    if email is None:
        return redirect('/signin')
    return render_template('order.html')


# Menu page
@app.route('/menu')
def menu():
    # items = MenuItem.query.all()
    return render_template('menu.html')


@app.route("/save_cart", methods=["POST"])
def save_cart():
    try:
        email = session.get("email")
        if email is None:
            return redirect("/signin") 
        data = request.json
        cart = data.get("cart", [])
        total_amount = 0
        # print(cart)
        # print("\n\n\n")
        # print(data)
        if cart:
            for item in cart:
                if item is not None:
                    Price = item['price']
                    total_amount += Price
            handler = SMDBHandler("localhost", "root", "mysql123", "web_project_food")
            # print("here1")
            order = orders(email, total_amount)
            # print("here2")
            handler.orderInfo(order)
            for item in cart:
                if item is not None:
                    # print("Name:", item['name'])
                    # print("Price:", item['price'])
                    # print("Quantity:", item['quantity'])
                    # print("--------------------")
                    Name = item['name']
                    Price = item['price']
                    Quantity = item['quantity']
                    # print("here3")
                    orders_item = orders_items(Name, Price, Quantity)
                    # print("here4")

                    handler.save_cart_info(orders_item)

                    # print("here5")

            return jsonify({"message": "Order placed successfully!"}), 200
        else:
            return jsonify({"message": "Cart is empty."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500









@app.route("/order_details")
def order_details():
    return render_template("order_details.html")

@app.route("/donateForm", methods=['POST'])
def donateForm():
    try:
        email = request.form["email"]
        name = request.form["name"]
        phone = request.form["phone"]
        amount = request.form["amount"]
        account = request.form["account"]
        handler = SMDBHandler("localhost", "root", "mysql123", "web_project_food")
        donate = handler.donate_ampunt(email, name,phone,amount,account)
        if donate:
            return render_template("donate.html",error="Donation success")
            # return render_template("index.html")
        else:
            return render_template("donate.html",error="Donation failed")
        
    except Exception as e:
        return render_template("donate.html",error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
