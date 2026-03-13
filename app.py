import streamlit as st
import streamlit.components.v1 as components
from data import flowers, bouquets
from chatbot import flower_chatbot
import datetime

st.set_page_config(page_title="Petal Paradise Flower Shop", layout="wide")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Home"

# sidebar navigation
page = st.sidebar.selectbox(
    "Navigate",
    ["Home", "Single Flowers", "Bouquets", "Cart", "Checkout", "Chatbot"],
    index=["Home", "Single Flowers", "Bouquets", "Cart", "Checkout", "Chatbot"].index(st.session_state.page)
)

# Add background image for home page
if page == "Home":
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("./images/background.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .stApp header {
            background-color: rgba(255, 255, 255, 0.8) !important;
        }
        .stApp .main {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            margin: 20px;
            padding: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.title("🌸 Petal Paradise Flower Shop")

# cart - now stores items with quantities
if "cart" not in st.session_state:
    st.session_state.cart = []  # Will store dicts: {"name": item_name, "quantity": qty, "price": price}

# order info for checkout
if "order_info" not in st.session_state:
    st.session_state.order_info = {}

# SEARCH
search = st.text_input("🔍 Search Flowers")

# HOME
if page == "Home":

    st.header("Welcome to Petal Paradise 💐")
    st.write("Find the perfect flowers for every occasion.")

# SINGLE FLOWERS
elif page == "Single Flowers":

    st.header("🌷 Single Flowers")

    cols = st.columns(3)

    for i, flower in enumerate(flowers):

        if search.lower() in flower["name"].lower():

            with cols[i % 3]:

                st.image(flower["image"])

                st.subheader(flower["name"])

                st.write(flower["description"])

                st.write("**Meaning:**", flower["meaning"])

                st.write("💲", flower["price"])

                if st.button("Add to Cart", key=flower["name"]):
                    # Check if item already in cart
                    item_in_cart = False
                    for item in st.session_state.cart:
                        if item["name"] == flower["name"]:
                            item["quantity"] += 1
                            item_in_cart = True
                            break
                    
                    if not item_in_cart:
                        st.session_state.cart.append({
                            "name": flower["name"],
                            "quantity": 1,
                            "price": flower["price"],
                            "type": "flower"
                        })
                    
                    st.success(f"Added {flower['name']} to cart!")

# BOUQUETS
elif page == "Bouquets":

    st.header("💐 Bouquets")

    cols = st.columns(2)

    for i, bouquet in enumerate(bouquets):

        with cols[i % 2]:

            st.image(bouquet["image"])

            st.subheader(bouquet["name"])

            st.write(bouquet["description"])

            st.write("**Meaning:**", bouquet["meaning"])

            st.write("💲", bouquet["price"])

            if st.button("Add to Cart", key=bouquet["name"]):
                # Check if item already in cart
                item_in_cart = False
                for item in st.session_state.cart:
                    if item["name"] == bouquet["name"]:
                        item["quantity"] += 1
                        item_in_cart = True
                        break
                
                if not item_in_cart:
                    st.session_state.cart.append({
                        "name": bouquet["name"],
                        "quantity": 1,
                        "price": bouquet["price"],
                        "type": "bouquet"
                    })
                
                st.success(f"Added {bouquet['name']} to cart!")

# CART
elif page == "Cart":

    st.header("🛒 Shopping Cart")

    if not st.session_state.cart:
        st.write("Your cart is empty. Add some beautiful flowers! 🌸")
    else:
        # Display cart items
        st.subheader("Your Items:")
        
        total_cost = 0
        
        for i, item in enumerate(st.session_state.cart):
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**{item['name']}**")
            
            with col2:
                # Quantity controls
                if st.button("➖", key=f"minus_{i}"):
                    if item["quantity"] > 1:
                        item["quantity"] -= 1
                    else:
                        st.session_state.cart.pop(i)
                        st.rerun()
            
            with col3:
                st.write(f"**{item['quantity']}**")
            
            with col4:
                if st.button("➕", key=f"plus_{i}"):
                    item["quantity"] += 1
            
            with col5:
                item_total = item["price"] * item["quantity"]
                st.write(f"${item_total}")
                total_cost += item_total
        
        st.divider()
        st.subheader(f"**Total: ${total_cost}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Cart", type="secondary"):
                st.session_state.cart = []
                st.success("Cart cleared!")
                st.rerun()
        
        with col2:
            if st.button("✅ Proceed to Checkout", type="primary"):
                st.session_state.page = "Checkout"
                st.rerun()

# CHECKOUT
elif page == "Checkout":

    st.header("📋 Checkout")

    if not st.session_state.cart:
        st.warning("Your cart is empty. Please add items before checkout.")
        if st.button("← Back to Shopping"):
            st.session_state.page = "Single Flowers"
            st.rerun()
    else:
        # Calculate total
        total_cost = sum(item["price"] * item["quantity"] for item in st.session_state.cart)
        
        # Order Summary
        st.subheader("📄 Order Summary")
        for item in st.session_state.cart:
            st.write(f"- {item['name']} x{item['quantity']} = ${item['price'] * item['quantity']}")
        st.write(f"**Total: ${total_cost}**")
        
        st.divider()
        
        # Checkout Form
        st.subheader("📝 Delivery Information")
        
        with st.form("checkout_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name *", placeholder="Enter your full name")
                phone = st.text_input("Phone Number *", placeholder="Enter your phone number")
            
            with col2:
                delivery_address = st.text_area("Delivery Address *", placeholder="Enter complete delivery address")
                delivery_date = st.date_input("Delivery Date *", min_value=datetime.date.today())
            
            message = st.text_area("Message for Recipient (Optional)", placeholder="Add a personal message...")
            
            special_notes = st.text_area("Special Delivery Notes (Optional)", placeholder="Any special delivery instructions...")
            
            submitted = st.form_submit_button("🎉 Place Order", type="primary")
            
            if submitted:
                if not full_name or not phone or not delivery_address:
                    st.error("Please fill in all required fields marked with *")
                else:
                    # Store order info
                    st.session_state.order_info = {
                        "full_name": full_name,
                        "phone": phone,
                        "delivery_address": delivery_address,
                        "delivery_date": delivery_date.strftime("%Y-%m-%d"),
                        "message": message,
                        "special_notes": special_notes,
                        "items": st.session_state.cart.copy(),
                        "total": total_cost
                    }
                    
                    # Clear cart
                    st.session_state.cart = []
                    
                    # Switch to confirmation page
                    st.session_state.page = "Order Confirmation"
                    st.rerun()

# ORDER CONFIRMATION
elif page == "Order Confirmation":

    if not st.session_state.order_info:
        st.warning("No order information found. Please start shopping!")
        if st.button("← Back to Home"):
            st.session_state.page = "Home"
            st.rerun()
    else:
        st.header("🎉 Order Confirmed!")
        
        st.success("Thank you for your order! Your flowers will be delivered as requested.")
        
        # Order Details
        st.subheader("📋 Order Details")
        
        order = st.session_state.order_info
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Customer Information:**")
            st.write(f"Name: {order['full_name']}")
            st.write(f"Phone: {order['phone']}")
        
        with col2:
            st.write("**Delivery Information:**")
            st.write(f"Address: {order['delivery_address']}")
            st.write(f"Date: {order['delivery_date']}")
            if order['message']:
                st.write(f"Message: {order['message']}")
            if order['special_notes']:
                st.write(f"Special Notes: {order['special_notes']}")
        
        st.divider()
        
        st.subheader("🛍️ Order Summary")
        for item in order['items']:
            st.write(f"- {item['name']} x{item['quantity']} = ${item['price'] * item['quantity']}")
        
        st.write(f"**Total: ${order['total']}**")
        
        st.divider()
        
        if st.button("🏠 Back to Shopping", type="primary"):
            st.session_state.order_info = {}
            st.session_state.page = "Home"
            st.rerun()

# CHATBOT
elif page == "Chatbot":

    st.header("🌸 FloraBot - Flower Assistant")

    # Embed the n8n chat widget directly into the app
    components.iframe("https://krithi2509.app.n8n.cloud/webhook/3ee79fd6-553f-4c04-9417-78ff604a4125/chat", height=600)