"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request, url_for
import jinja2

import melons
import customers

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    if 'username' in session:
        print(f"Logged in as {session['username']}")
    else:
        print("You are not logged in")

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    # - loop over the cart dictionary, and for each melon id:
    #    - get the corresponding Melon object
    #    - compute the total cost for that type of melon
    #    - add this to the order total
    #    - add quantity and total cost as attributes on the Melon object
    #    - add the Melon object to the list created above
    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session


    if "cart" in session:
        melon_obj = []
        total_cost = 0
        for melon in session["cart"]:
            mel = melons.get_by_id(melon)
            num_melons = int(session["cart"][melon])
            melon_price = int(mel.price)
            melon_total = num_melons * melon_price
            mel.quantity = num_melons
            mel.total = melon_total
            melon_obj.append(mel)
            total_cost += melon_total
        

        return render_template("cart.html", total=total_cost, melons=melon_obj)
    
    return render_template("cart.html", total=None, melons=None)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    # - flash a success message
    # - redirect the user to the cart page

    
    if 'cart' in session:
        if melon_id in session["cart"]:
            session["cart"][melon_id] += 1
        else:
            session["cart"][melon_id] = 1
    else:
        session["cart"] = {}
        session["cart"][melon_id] = 1

    flash("Item has been added to your cart!")
    
    return show_shopping_cart()
    # return render_template("cart.html", cart=session["cart"])


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    user_email = request.form['email']
    user_password = hash(request.form['password'])
    print(user_password)
    try:
        if hash(customers.get_by_email(user_email).password) == user_password:
            session['email'] = user_email
            flash ("You are logged in!")
            return redirect(url_for('list_melons'))
        else:
            flash ("Incorrect Password")
            return redirect(url_for('show_login'))
    except KeyError:
        flash("Email doesn't exist")
        return redirect(url_for('show_login'))

@app.route('/logout')
def process_logout():
    session['email'] = ""
    flash("You have been logged out!")
    return redirect(url_for('list_melons'))



@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
