import streamlit as st
import pandas as pd
import psycopg2
import time
import random


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

conn.autocommit = True

sql = """select * from qst1"""
cursor = conn.cursor()
cursor.execute(sql)
df=pd.DataFrame(cursor.fetchall(),columns=['Username',	'Nome',	'Cognome',	'Livello_sodisfazione',	'q1',	'q2',	'q3',	'q4',	'q5',	'time'])



questions = {
  "1": "2+2=?",
  "2": "√81=?",
  "3": "Quale non è un colore?",
  "4": "la mela ad frutta è come pizza ad?",
  "5": "chi è la mamma di fratello della sorella di tua madre?",
  "6": "1, 4, 9, ?",
  "7": "1, 4, 5, 9, ?",
  "8": "2, 3, 5, 7, 11, ?",
  "9": "quale è il capitale di Italia?",
  "10": "se giusto è sbaglio è sbaglio è sbaglio, che cosa è giusto?"
}



def check_password():
    """Returns `True` if the user had a correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            #del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if "t0" not in st.session_state:
    st.session_state["t0"] = time.time()
if "st" not in st.session_state:
    st.session_state["st"]= True
if "usercheck" not in st.session_state:
    st.session_state['usercheck']=False
if "rn" not in st.session_state:
    st.session_state["rn"] = random.sample(range(1, 10), 5)

if check_password():
    @st.cache(allow_output_mutation=True)
    def get_data():
        return []
    Username=st.text_input("Username:")
    if st.button("check"):
        if Username in df['Username'].to_list():
            st.session_state['usercheck']=False
            st.write('l\'esame gia registrato 😊.')
        elif Username not in st.secrets['passwords'].keys():
            st.write('😕 User not known')
        else:
            st.session_state['usercheck']=True
            st.session_state['st']=True
    if st.session_state['usercheck']==True:
        if st.session_state["st"]==True:
            Nome = st.text_input("Nome:")
            Cognome = st.text_input("Cognome:")
            sodisfazione = st.slider("Sodisfazione", 0, 100)
            Qa=st.text_input(questions[str(st.session_state["rn"][0])])
            Qb=st.text_input(questions[str(st.session_state["rn"][1])])
            Qc=st.text_input(questions[str(st.session_state["rn"][2])])
            Qd=st.text_input(questions[str(st.session_state["rn"][3])])
            Qe=st.text_input(questions[str(st.session_state["rn"][4])])
            if st.button("Submit"):
                get_data().append({"Username":Username,"Nome": Nome,"Cognome":Cognome, "Livello_sodisfazione": sodisfazione, "q1": Qa, "q2": Qb, "q3": Qc, "q4": Qd, "q5": Qe, "time":time.time()-st.session_state["t0"]})
                A=pd.DataFrame(get_data())
                st.write(A)
            st.write('Se Lei è sicuro da chiudere l\'esamae, premi conferma')
            if st.button("Confirm"):
                L=len(pd.DataFrame(get_data()))
                dx=df.append(pd.DataFrame(get_data()).loc[L-1,:],ignore_index=True)
                #st.write(dx)
                sql = """INSERT INTO qst1 (Username, Nome, Cognome,Livello_sodisfazione, q1, q2,q3 ,q4 ,q5 , time) VALUES (dx["Username”].loc[-1],dx[“Nome”].loc[-1],dx[“Cognome”].loc[-1],dx[“Livello_sodisfazione”].loc[-1],dx[“q1”].loc[-1],dx[“q2”].loc[-1],dx[“q3”].loc[-1],dx[“q4”].loc[-1],dx[“q5”].loc[-1],dx[“time"].loc[-1])"""
                cursor = conn.cursor()
                cursor.execute(sql)
                st.title('la sua esame è finito 😊.')
                st.title("Grazie per la collaborazione! 😍")
                st.session_state["st"]=False
        else:
            st.title('l\'esame gia registrato 😊.')
