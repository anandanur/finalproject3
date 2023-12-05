import streamlit as st
from sqlalchemy import text


conn = st.connection("postgresql", type="sql", 
                     url="postgresql://anandanurd13:liuoJI0dh8CQ@ep-bitter-credit-99134373.us-east-2.aws.neon.tech/fp3")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS orders (id serial, customer_name text, email text, phone_number text, \
                  address text, product_name text, quantity int, order_date date, order_status text, \
                  tracking_number text, estimated_arrival_date date);')
    session.execute(query)

st.header('SIMPLE SHOP DATA MANAGEMENT')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM orders ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO ORDERS (customer_name, email, phone_number, address, product_name,order_status) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'', '5':'', '6':'', '7':'', '8':None, '9':'', '10':'', '11':None})
            session.commit()

    data = conn.query('SELECT * FROM orders ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        customer_name_lama = result["customer_name"]
        email_lama = result["email"]
        phone_number_lama = result["phone_number"]
        address_lama = result["address"]
        product_name_lama = result["product_name"]
        quantity_lama = result["quantity"]
        order_date_lama = result["order_date"]
        order_status_lama = result["order_status"]
        tracking_number_lama= result ["tracking_number"]
        estimated_arrival_date_lama = result ["estimated_arrival_date"]

        with st.expander(f'a.n. {customer_name_lama}'):
            with st.form(f'data-{id}'):
                customer_name_baru = st.text_input("customer_name",customer_name_lama)
                email_baru = st.text_input("email", email_lama)
                phone_number_baru = st.text_input("phone_number", phone_number_lama)
                address_baru = st.text_input("address", address_lama)
                product_name_baru = st.text_input("product_name", product_name_lama)
                quantity_baru = st.text_input("quantity", quantity_lama)
                order_date_baru = st.date_input("order_date", order_date_lama)
                order_status_baru = st.text_input("order_status", order_status_lama)
                tracking_number_baru = st.text_input("tracking_number", tracking_number_lama)
                estimated_arrival_date_baru = st.date_input ("estimated_arrival_date", estimated_arrival_date_lama)
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE orders \
                                          SET customer_name=:1, email=:2, phone_number=:3, address=:4, \
                                          product_name=:5, quantity=:6, order_date=:7, order_status=:8 \
                                          tracking_number=:9,estimated_arrival_date=:10\
                                          WHERE id=:11;')
                            session.execute(query, {'1':customer_name_baru, '2':email_baru, '3':phone_number_baru, '4':address_baru, 
                                                    '5':product_name_baru, '6':quantity_baru, '7':order_date_baru, '8':order_status_baru, 
                                                    '9':tracking_number_baru, '10':estimated_arrival_date_baru, '11':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM orders WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()