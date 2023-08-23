from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *
import os
from streamlit_option_menu import option_menu
from dbtransactions import TransactionFetcher
from dbinventory import InventoryFetcher
import keys


os.environ['OPENAI_API_KEY']=keys.OPENAI_KEY
st.subheader("Chatbot")

selected = option_menu(
    menu_title=None,
    options=["General", "User Specific", "Inventory"],
    default_index=0,
    orientation="horizontal",
)

if selected == "General":
    st.title(f"{selected}")
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    if 'buffer_memory' not in st.session_state:
                st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


    # system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
    # and if the answer is not contained within the text below, say 'I don't know'""")

    system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question by only using the information given to you in the query and no inputs from your side, 
    and if the answer is not contained within the text below, say 'I don't know'""")


    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

    prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

    conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)




    # container for chat history
    response_container = st.container()
    # container for text box


    # Create a button to open the pop-up box
    if st.button("Open Pop-up Box"):
        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = True
        else:
            st.session_state.show_popup = not st.session_state.show_popup

    # Display the pop-up box if the toggle is True
    if st.session_state.get('show_popup', False):
        with st.form("popup_form"):
            st.subheader("Pop-up Box")
            mail = st.text_input("Mail")
            query = st.text_input("Query")
            submit_button = st.form_submit_button("Submit")
            if submit_button:
                # Process the submitted data
                # Add your logic here
                st.success(f"Submitted: Mail - {mail}, Query - {query}")
                send_mail(mail, query)
                # add_QA_DB(query, "", mail, answered=False)
                st.session_state.show_popup = False  # Close the pop-up box after submitting

    textcontainer = st.container()



    with textcontainer:
        query = st.text_input("Query: ", key="input")
        if query:
            with st.spinner("typing..."):
                # conversation_string = get_conversation_string()
                # st.code(conversation_string)
                # refined_query = query_refiner(conversation_string, query)
                # st.subheader("Refined Query:")
                # st.write(query)
                
                context = find_match(query)
                
                # print(context)  
                response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
            
            st.session_state.requests.append(query)
            st.session_state.responses.append(response) 
            # if(response != "I don't know"):
            #     add_QA_DB(query, response, "")
            # else:
            #     add_QA_DB_NoAns(query)
            
    with response_container:
        if st.session_state['responses']:

            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

def show_chat(customer_id, name, context2):
    # context2 =  transaction_fetcher.authenticate_doctor(customer_id, name)
    print(context2)
    
    # Display the chat interface here
    st.title(f"{selected}")
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    llm2 = ChatOpenAI(model_name="gpt-3.5-turbo")

    if 'buffer_memory' not in st.session_state:
                st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


    # system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
    # and if the answer is not contained within the text below, say 'I don't know'""")

    system_msg_template2 = SystemMessagePromptTemplate.from_template(template="""Answer the question by only using the information given to you in the query and no inputs from your side, 
    and if the answer is not contained within the text below, say 'I don't know'""")


    human_msg_template2 = HumanMessagePromptTemplate.from_template(template="{input}")

    prompt_template2 = ChatPromptTemplate.from_messages([system_msg_template2, MessagesPlaceholder(variable_name="history"), human_msg_template2])

    conversation2 = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template2, llm=llm2, verbose=True)




    # container for chat history
    response_container2 = st.container()
    # container for text box


    # Create a button to open the pop-up box
    if st.button("Open Pop-up Box"):
        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = True
        else:
            st.session_state.show_popup = not st.session_state.show_popup

    # Display the pop-up box if the toggle is True
    if st.session_state.get('show_popup', False):
        with st.form("popup_form"):
            st.subheader("Pop-up Box")
            mail = st.text_input("Mail")
            query = st.text_input("Query")
            submit_button = st.form_submit_button("Submit")
            if submit_button:
                # Process the submitted data
                # Add your logic here
                st.success(f"Submitted: Mail - {mail}, Query - {query}")
                send_mail(mail, query)
                # add_QA_DB(query, "", mail, answered=False)
                st.session_state.show_popup = False  # Close the pop-up box after submitting

    textcontainer2 = st.container()



    with textcontainer2:
        query2 = st.text_input("Query: ", key="input")
        if query2:
            with st.spinner("typing..."):
                # conversation_string = get_conversation_string()
                # st.code(conversation_string)
                # refined_query = query_refiner(conversation_string, query)
                # st.subheader("Refined Query:")
                # st.write(query)
                
                # context = find_match(query)

                
                # print(context)  
                response2 = conversation2.predict(input=f"Context:\n {context2} \n\n Query:\n{query2}")
            
            st.session_state.requests.append(query2)
            st.session_state.responses.append(response2) 
            # if(response != "I don't know"):
            #     add_QA_DB(query, response, "")
            # else:
            #     add_QA_DB_NoAns(query)
            
    with response_container2:
        if st.session_state['responses']:

            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')
    st.write("Chat interface will be displayed here.")

    
if selected == "User Specific":
    db_params = {
        'dbname': 'appointments',
        'user': 'postgres',
        'password': 'password',
        'host': 'localhost'
    }

    transaction_fetcher = TransactionFetcher(db_params)
    st.title(f"{selected}")
    st.title("User Authentication")

    customer_id = st.text_input("Enter customer ID:")
    name = st.text_input("Enter name:")
    # last_name = st.text_input("Enter last name:")
    submit_button = st.button("Authenticate")
    # Initialize session_state if it doesn't exist
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if submit_button:
        # Perform authentication logic here
        # authenticated = transaction_fetcher.authenticate_doctor(customer_id, name)
        authenticated = transaction_fetcher.authenticate_doctor(customer_id, name)
        st.session_state.authenticated = authenticated

    if st.session_state.authenticated:
        st.success("Authentication successful! You can now access the chat.")
        # st.session_state.authenticated = transaction_fetcher.getAppointments(name)
        show_chat(customer_id, name, st.session_state.authenticated)






    
if selected == "Inventory": 
    db_params2 = {
        'dbname': 'medicines',
        'user': 'postgres',
        'password': 'password',
        'host': 'localhost'
    }

    inventory_fetcher = InventoryFetcher(db_params2)
    context2 = inventory_fetcher.fetch_stock()
    
    # Display the chat interface here
    st.title(f"{selected}")
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    llm2 = ChatOpenAI(model_name="gpt-3.5-turbo")

    if 'buffer_memory' not in st.session_state:
                st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


    # system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
    # and if the answer is not contained within the text below, say 'I don't know'""")

    system_msg_template2 = SystemMessagePromptTemplate.from_template(template="""Answer the question by only using the information given to you in the query and no inputs from your side, 
    and if the answer is not contained within the text below, say 'I don't know'""")


    human_msg_template2 = HumanMessagePromptTemplate.from_template(template="{input}")
    

    prompt_template2 = ChatPromptTemplate.from_messages([system_msg_template2, MessagesPlaceholder(variable_name="history"), human_msg_template2])

    conversation2 = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template2, llm=llm2, verbose=True)




    # container for chat history
    response_container2 = st.container()
    # container for text box


    # Create a button to open the pop-up box
    if st.button("Open Pop-up Box"):
        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = True
        else:
            st.session_state.show_popup = not st.session_state.show_popup

    # Display the pop-up box if the toggle is True
    if st.session_state.get('show_popup', False):
        with st.form("popup_form"):
            st.subheader("Pop-up Box")
            mail = st.text_input("Mail")
            query = st.text_input("Query")
            submit_button = st.form_submit_button("Submit")
            if submit_button:
                # Process the submitted data
                # Add your logic here
                st.success(f"Submitted: Mail - {mail}, Query - {query}")
                send_mail(mail, query)
                # add_QA_DB(query, "", mail, answered=False)
                st.session_state.show_popup = False  # Close the pop-up box after submitting

    textcontainer2 = st.container()



    with textcontainer2:
        query2 = st.text_input("Query: ", key="input")
        if query2:
            with st.spinner("typing..."):
                # conversation_string = get_conversation_string()
                # st.code(conversation_string)
                # refined_query = query_refiner(conversation_string, query)
                # st.subheader("Refined Query:")
                # st.write(query)
                
                # context = find_match(query)

                
                # print(context)  
                print(context2)
                response2 = conversation2.predict(input=f"Context:\n {context2} \n\n Query:\n{query2}")
            
            st.session_state.requests.append(query2)
            st.session_state.responses.append(response2) 
            # if(response != "I don't know"):
            #     add_QA_DB(query, response, "")
            # else:
            #     add_QA_DB_NoAns(query)
            
    with response_container2:
        if st.session_state['responses']:

            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')
    st.write("Chat interface will be displayed here.")
    st.title(f"{selected}")

