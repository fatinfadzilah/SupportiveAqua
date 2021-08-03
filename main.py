from flask import Flask, jsonify, render_template, request
from tables import data
from menu import food, beverage, status
from datetime import datetime, timedelta

app = Flask(__name__)

def get_current_dt_string():
    current_dt = datetime.utcnow() + timedelta(hours=8)
    return current_dt.strftime("%d %B %Y, %H:%M:%S")


@app.route("/tables", endpoint='funct1')
def tables():
    return jsonify(data)


@app.route("/menufood", endpoint='funct2')
def menufood():
    return jsonify(food)


@app.route("/menudrink", endpoint='funct3')
def menudrink():
    return jsonify(beverage)


@app.route("/")
def mainpage():
    return render_template("tables.html", tables=data)


@app.route("/api/table/<table_id>")
def get_table_info(table_id):
    resp = jsonify(data[table_id])
    resp.status_code = 200
    return resp


@app.route("/order/<table_id>", methods=["GET", "POST"])
def order(table_id):
    if request.method == "POST":
        new_order = request.form

        data[table_id]["food"]["itemfood"] = []
        data[table_id]["food"]["qfood"] = []
        data[table_id]["drinks"]["itemdrink"] = []
        data[table_id]["drinks"]["qdrink"] = []

        for key, quantity in new_order.items():
            if len(quantity) > 0:
                if key[0] == 'f':
                    f = int(key[1:])
                    order_food = food[f]
                    data[table_id]["food"]["itemfood"].append(order_food)
                    data[table_id]["food"]["qfood"].append(int(quantity))

                elif key[0] == 'd':
                    d = int(key[1:])
                    order_drink = beverage[d]
                    data[table_id]["drinks"]["itemdrink"].append(order_drink)
                    data[table_id]["drinks"]["qdrink"].append(int(quantity))

        # Update status to 'Ordered'
        data[table_id]["status"] = "Ordered"

        # Update time ordered
        data[table_id]["time"] = get_current_dt_string()
        return render_template("orderSuccessful.html", table_id=table_id)

    if data[table_id]["status"] == 'Available':
        return render_template("menu.html", table_id=table_id)


@app.route("/api/table/<table_id>/status/<status_id>", methods=["PUT"])
def update_table_status(table_id, status_id):
    status_id = int(status_id)
    data[table_id]["status"] = status[status_id]
    data[table_id]["time"] = get_current_dt_string()
    return f"Updated Table {table_id} status to {status[status_id]}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)
