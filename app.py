import streamlit as st
from menu import menu, extras, toppings, sauces

st.set_page_config(page_title="Kirkwood Deli Chatbot", layout="wide")
st.title("🥪 Kirkwood Deli Sandwich Order App")
st.markdown("Welcome! Select a sandwich, remove ingredients you don’t want, add extras, and build your perfect order.")

if "cart" not in st.session_state:
    st.session_state.cart = []

# Sandwich selector
selected_item = st.selectbox("Choose a sandwich:", list(menu.keys()))
details = menu[selected_item]

# Handle price and options
if "options" in details:
    option = st.selectbox(f"Select option for {selected_item}:", list(details["options"].keys()))
    base_price = details["options"][option]
else:
    option = None
    base_price = details.get("price", 0.0)

# Get default ingredients
default_ingredients = details.get("ingredients", [])

# Remove ingredients multiselect
remove_ingredients = st.multiselect("Remove ingredients you don't want:", default_ingredients)

# Extras selection in expander (only toppings and sauces)
with st.expander("➕ Add extras (toppings and sauces)"):
    add_toppings = st.multiselect("Add toppings ($0.50 each):", toppings)
    add_sauces = st.multiselect("Add sauces ($1.99 each):", sauces)
    add_large_bowl = st.checkbox("Add Large Sauce Bowl ($6.99)")

# Calculate price breakdown
price_breakdown = []
total_price = base_price
price_breakdown.append(f"Base price: ${base_price:.2f}")

if len(add_toppings) > 0:
    toppings_cost = len(add_toppings) * extras["Toppings (each)"]
    total_price += toppings_cost
    price_breakdown.append(f"Toppings ({len(add_toppings)} × ${extras['Toppings (each)']:.2f}): ${toppings_cost:.2f}")

if len(add_sauces) > 0:
    sauces_cost = len(add_sauces) * extras["Extra Sauce"]
    total_price += sauces_cost
    price_breakdown.append(f"Sauces ({len(add_sauces)} × ${extras['Extra Sauce']:.2f}): ${sauces_cost:.2f}")

if add_large_bowl:
    total_price += extras["Large Sauce Bowl"]
    price_breakdown.append(f"Large Sauce Bowl: ${extras['Large Sauce Bowl']:.2f}")

price_breakdown.append(f"**Total: ${total_price:.2f}**")

# Add to cart button
if st.button(f"Add {selected_item} to cart (${total_price:.2f})"):
    st.session_state.cart.append({
        "item": selected_item,
        "option": option,
        "price": total_price,
        "removed": remove_ingredients,
        "added_toppings": add_toppings,
        "added_sauces": add_sauces,
        "large_bowl": add_large_bowl,
        "price_breakdown": price_breakdown
    })
    st.success(f"{selected_item} added to cart!")

st.markdown("---")

# Show Cart
st.subheader("🛒 Your Cart")

if st.session_state.cart:
    grand_total = 0
    for i, order in enumerate(st.session_state.cart, 1):
        st.markdown(f"**{i}. {order['item']}** - ${order['price']:.2f}")
        if order["option"]:
            st.write(f"*Option:* {order['option']}")

        # Removed ingredients list vertically
        if order["removed"]:
            st.markdown("**Removed ingredients:**")
            for ing in order["removed"]:
                st.write(f"- {ing}")

        # Added toppings vertically
        if order["added_toppings"]:
            st.markdown("**Added toppings:**")
            for top in order["added_toppings"]:
                st.write(f"+ {top}")

        # Added sauces vertically
        if order["added_sauces"]:
            st.markdown("**Added sauces:**")
            for sau in order["added_sauces"]:
                st.write(f"+ {sau}")

        if order["large_bowl"]:
            st.markdown("+ Large Sauce Bowl")

        # Show price breakdown vertically
        st.markdown("**Price breakdown:**")
        for line in order["price_breakdown"]:
            st.write(line)

        st.markdown("---")
        grand_total += order["price"]

    st.markdown(f"### 🧾 Grand Total: ${grand_total:.2f}")
else:
    st.info("Your cart is empty")
