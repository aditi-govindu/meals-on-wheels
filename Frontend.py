# importing modules
import streamlit as st
import urllib.request
from PIL import Image
import os
import pickle as pkl
import webbrowser
import numpy as np
from time import sleep
from stqdm import stqdm
import random
import mysql.connector as connector

# Connect to local database
conx = connector.connect(user='<your_username>', password = '<your_password>', host = 'localhost',database = 'mealsonwheels')
mycursor = conx.cursor(buffered=True)

# Variables used
order_no = 122
user_email = ''
kitchen_id = 1

# Display tables in database
mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x)

# Display on home page website
st.title('Meals on Wheels')
st.subheader('Where train journeys meet the perfect meal partner!')
st.write('Hello, *Passengers!* :train:')

# Generate a list of pages to go to on the side
next = st.sidebar.button('Page Navigation')

pages = ['Homepage','Customer login','Place order', 'Track order', 
         'Payment','Feedback','Logout']

next_clicked = 0
user_count = 1

choice = st.sidebar.radio("go to",('Homepage','Customer login',
                                   'Place order', 'Track order', 'Payment',
                                   'Feedback', 'Logout'), index=next_clicked)

if os.path.isfile('next.p'):
    next_clicked = pkl.load(open('next.p', 'rb'))
    # check if you are at the end of the list of pages
    if next_clicked == len(pages):
        next_clicked = 0 # go back to the beginning i.e. homepage
else:
    next_clicked = 0 #the start

pkl.dump(pages.index(choice), open('next.p', 'wb'))

# next button and increment our index tracker (next_clicked)
if next:
    #increment value to get to the next page
    next_clicked = next_clicked +1

    # check if you are at the end of the list of pages again
    if next_clicked == len(pages):
        next_clicked = 0 # go back to the beginning i.e. homepage


# Display data on each page
if choice == 'Homepage':
  st.subheader('Developed by: Aditi, Ankit, Pranav and Reuben for MIT-WPU')
  # Display an image for website from Google
  urllib.request.urlretrieve('https://i1.wp.com/www.opindia.com/wp-content/uploads/2019/07/IRCTC-ecatering.jpg?fit=849%2C477&ssl=1', "homepage.png")
  image = Image.open("homepage.png")
  st.image(image, use_column_width=True)

elif choice == 'Customer login':
  # Ask user to enter personal details
  st.write('Customer login')
  # User details cannot be null
  user_name = st.text_input("Enter your first name: ")
  user_email = st.text_input("Enter your email id: ")
  if not user_email:
    st.warning('Please enter your email id')
  user_phone = st.number_input("Enter your registered phone no: ")
  if not user_phone:
    st.warning('Please enter your phone number')
  user_train = st.number_input("Enter your train PRN no: ")
  if not user_train:
    st.warning('Please enter valid train number number')
  # Insert user entered values in database
  sql = "INSERT INTO passenger (Email_ID, Name, Train_PRN, Phone, order_id) VALUES (%s, %s, %s, %s, %s)"
  val = (user_email, user_name, user_train, user_phone, order_no)
  mycursor.execute(sql, val)
  # Update order_no
  conx.commit()
  print(mycursor.rowcount, "record inserted.")
  order_no += 1 
  st.title('Details successfully added! Proceed to place order')

  # 2 buttons to go to 
  button1 = st.button('Place order')
  st.write('Start ordering food by clicking **Place order** in sidebar :green_salad:')
  button2 = st.button('Track order')
  st.write('Start tracking your food by clicking **Track order** in sidebar :stopwatch:')
  if button1:
    st.write('Start ordering food by clicking **Place order** in sidebar :green_salad:')
  if button2:
    st.write('Start tracking your food by clicking **Track order** in sidebar :stopwatch:')
    
elif choice == 'Place order':
    st.write('What do you feel like eating today?')

    caption = ['Vegetarian', 'Non vegetarian', 'Vegan']
    food_imgs = ['https://i.pinimg.com/originals/a2/bb/d5/a2bbd55e26b31e5157b770d5e5292c0d.jpg',
                 'https://images.hindustantimes.com/rf/image_size_640x362/HT/p2/2017/10/07/Pictures/_df6cfee8-ab4b-11e7-8fa9-3a95f17ae4d1.jpg',
                 'https://cdn-prod.medicalnewstoday.com/content/images/articles/324/324343/plant-meal.jpg'
                 ]

    idx = 0 
    for _ in range(len(food_imgs)-1): 
        cols = st.columns(3) 
        
        if idx < len(food_imgs):
          urllib.request.urlretrieve(food_imgs[0], "veg.png")
          image = Image.open("veg.png")
          cols[0].image(image, width=150, caption=caption[idx])
        idx+=1
        
        if idx < len(food_imgs):
          urllib.request.urlretrieve(food_imgs[1], "nonveg.png")
          image = Image.open("nonveg.png")
          cols[1].image(image, width=150, caption=caption[idx])
        idx+=1

        if idx < len(food_imgs):
          urllib.request.urlretrieve(food_imgs[2], "vegan.png")
          image = Image.open("vegan.png")
          cols[2].image(image, width=150, caption=caption[idx])
          idx+=1 

        else:
            break

    option = st.selectbox('Choice of meal: ', ('Veg', 'Non veg', 'vegan'))
    user_count = st.number_input('Meals', min_value=1, max_value=100, step=1)
    # Display list of veg hotels in database
    if option == 'Veg':
      mycursor.execute("SELECT type, name FROM kitchen WHERE type = 'VEG'")
      myresult = mycursor.fetchall()
      hotel = st.text_input('Chose a restuarant: ')
      for x in myresult:
        st.write(x)
      user_cost = 120
    elif option == 'Non veg':
      mycursor.execute("SELECT type, name FROM kitchen WHERE type = 'NON VEG'")
      myresult = mycursor.fetchall()
      hotel = st.text_input('Chose a restuarant: ')
      for x in myresult:
        st.write(x)
      user_cost = 150
    else:
      mycursor.execute("SELECT type, name FROM kitchen WHERE type = 'VEGAN'")
      myresult = mycursor.fetchall()
      hotel = st.text_input('Chose a restuarant: ')
      for x in myresult:
        st.write(x)
      user_cost = 160

    sql = "SELECT kitchen_ID FROM kitchen WHERE name = '%Kitchen%'" 
    mycursor.execute(sql)
    kitchen_id =  mycursor.fetchone()
    st.write('You chose kitchen id:',kitchen_id)
    #track_list = np.array([17, 18, 19, 23, 34, 56, 45, 99, 102, 34, 55, 65, 90, 100, 20])
    track_id = random.randint(20,100)
    sql2 = "INSERT INTO delivery (Tracking_ID, D_Name, Pass_Email, D_Phone, ETA, Station) VALUES (%s, %s, %s, %s, %s, %s)"
    val2 = (track_id , 'vignesh', user_email,  958324647, '2021-10-11 13:26:16', 'nashik')
    mycursor.execute(sql2, val2)
    # Insert user entered values in meal and delivery databases
    sql1 = "INSERT INTO meal (Meal_ID, Special_req, M_Type, Cost, Quantity, K_ID, Track_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val1 = (order_no, 'NULL', option, user_cost, user_count, kitchen_id, track_id)
    mycursor.execute(sql1, val1)
    conx.commit()
    st.write('You selected:',user_count, option, 'meals')
    # Display tracking order
    button3 = st.button('Done')
    if button3:
      sql = "SELECT tracking_id FROM delivery WHERE pass_email = (%s)"
      mycursor.execute(sql, user_email)
      order_no =  mycursor.fetchall()
      st.write('Tracking order no is: ',order_no)
      st.write('Proceed to **Payment** in sidebar :money:')

elif choice == 'Track order':
    st.subheader('Track order')
    order_id = st.text_input('Enter tracking order no: ')
    #sleep(5)
    # Display status of delivery
    for _ in stqdm(range(5)):
      sleep(0.5)
    st.title('Order will be delivered soon!')

elif choice == 'Payment':
    st.subheader('Payment')
    # Select cost from payment table
    sql = "SELECT amount FROM payment WHERE k_info = '101'"
    mycursor.execute(sql)
    cost =  mycursor.fetchone()
    option = st.selectbox('Payment mode: ', ('UPI', 'Cash on delivery', 'Card'))
    st.write('You chose: ',option)
    # Redirect user to requisite URL for UPI payment
    if option == 'UPI':
      if st.button('BHIM'):
        link = '[BHIM](https://www.bhimupi.org.in/)'
        st.markdown(link, unsafe_allow_html=True)
      if st.button('Gpay'):
        link = '[GPay](https://pay.google.com/)'
        st.markdown(link, unsafe_allow_html=True)
      if st.button('PayTM'):
        link = '[PayTM](https://paytm.com/)'
        st.markdown(link, unsafe_allow_html=True)
      if st.button('PhonePe'):
        link = '[PhonePe](https://www.phonepe.com/)'
        st.markdown(link, unsafe_allow_html=True)
      if st.button('PayPal'):
        link = '[PayPal](https://www.paypal.com/in/home)'
        st.markdown(link, unsafe_allow_html=True)
      if st.button('RazorPay'):
        link = '[RazorPay](https://razorpay.com/)'
        st.markdown(link, unsafe_allow_html=True)
    elif option == 'Cash on delivery':
      # Fetch name of delivery person from delivery database
      sql = "SELECT d_name, d_phone FROM delivery WHERE tracking_id = 64"
      mycursor.execute(sql)
      delivered_by =  mycursor.fetchall()
      st.title('Cash on delivery')
      st.write('Please pay exact change to: ',delivered_by[0])
    elif option == 'Card':
      option_card = st.selectbox('Bank: ', ('ICICI', 'HDFC', 'SBI'))
      if option_card == 'ICICI':
        link = '[ICICI](https://www.icicibank.com/)'
        st.markdown(link, unsafe_allow_html=True)
      if option_card == 'HDFC':
        link = '[HDFC](https://www.hdfcbank.com/)'
        st.markdown(link, unsafe_allow_html=True)
      if option_card == 'SBI':
        link = '[SBI](https://www.onlinesbi.com/)'
        st.markdown(link, unsafe_allow_html=True)
    else:
      st.write(option, ' not available at present. Inconvenience caused regretted')

elif choice == 'Feedback':
  # Update payment by inserting user entered value in payment table
  st.subheader('Rate your experience with us today!')
  slide1 = st.slider('How satisified were you with delivery?')
  slide2 = st.slider('How tasty was your meal?')
  slide3 = st.slider('Rate our GUI')
  button4 = st.button('Done')
  score = (slide1 + slide2 + slide3)/3
  sql2 = "UPDATE payment SET feedback (%s) WHERE k_info = (%s)"
  val2 = (sql2, score, kitchen_id)
  conx.commit()
  if button4:
    st.write("Feedback submitted. Thank you!")
    st.write('Proceed to **Logout** in sidebar')

elif choice == 'Logout':
  st.header('Thank you for using our service')
  # Display an image for website from Google
  st.markdown("![Thank you!](https://media.giphy.com/media/L0owGTy0mQ4L5PVmUo/giphy.gif)", unsafe_allow_html=True)

# Close MySQL connection
conx.close()