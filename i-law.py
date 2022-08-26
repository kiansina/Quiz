#CREATE TABLE qst
# (Username TEXT PRIMARY KEY, Nome TEXT, Cognome TEXT,
#  Livello_sodisfazione integer NOT NULL, q1 varchar(1), q2 varchar(1),
#  q3 varchar(1),q4 varchar(1),q5 varchar(1), time varchar(6), first_time varchar(10));



#INSERT INTO qst2 (Username, Nome, Cognome,Livello_sodisfazione, q1, q2,q3 ,q4 ,q5 , time) VALUES('ssin','sin','sin','100','sin','sin','sin','sin','sin','120');




import streamlit as st
import pandas as pd
import psycopg2
import time
import random
from PIL import Image

img=Image.open('lo.jfif')
st.set_page_config(page_title="Questionnaire", page_icon=img)

hide_menu_style= """
          <style>
          #MainMenu {visibility: hidden; }
          footer {visibility: hidden;}
          </style>
          """

st.markdown(hide_menu_style, unsafe_allow_html=True)
# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

conn.autocommit = True

sql = """select * from qst"""
cursor = conn.cursor()
cursor.execute(sql)
df=pd.DataFrame(cursor.fetchall(),columns=['Username',	'Nome',	'Cognome',	'Livello_sodisfazione',	'q1',	'q2',	'q3',	'q4',	'q5',	'time', 'first_time'])



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

choices = {
"1": [("4","T"),("8","F"),("0","F")],
"2": [("9","T"),("6","F"),("8","F")],
"3": [("Cielo","T"),("Rosa","F"),("Viola","F")],
"4": [("Cibo","T"),("Pasta","F"),("Coffee","F")],
"5": [("Nonna","T"),("Zia","F"),("Cugina","F")],
"6": [("16","T"),("12","F"),("18","F")],
"7": [("14","T"),("16","F"),("18","F")],
"8": [("13","T"),("16","F"),("14","F")],
"9": [("Roma","T"),("Milano","F"),("Torino","F")],
"10": [("Nulla","T"),("Tutto","F"),("Sbaglio","F")],
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
        return True , st.session_state["username"]

#if "t0" not in st.session_state:
#    st.session_state["t0"] = time.time()
if "st" not in st.session_state:
    st.session_state["st"]= True
if "usercheck" not in st.session_state:
    st.session_state['usercheck']=False
if "rn" not in st.session_state:
    st.session_state["rn"] = random.sample(range(1, 10), 5)
if "first_time" not in st.session_state:
    st.session_state['first_time']={}

if 'ch0' not in st.session_state:
    for i in range(0,len(st.session_state["rn"])):
        st.session_state["ch{}".format(i)]=random.sample(choices[str(st.session_state["rn"][i])],k=len(choices[str(st.session_state["rn"][i])]))                  #random.sample(choices[str(st.session_state["rn"][i])],k=len(choices[str(st.session_state["rn"][i])]))
        st.session_state["cho{}".format(i)]=[x[0] for x in st.session_state["ch{}".format(i)]]
        st.session_state["che{}".format(i)]=[x[1] for x in st.session_state["ch{}".format(i)]]


@st.experimental_singleton
def tim_first():
    if st.session_state["username"] not in st.session_state['first_time'].keys():
        st.session_state['first_time']['{}'.format(st.session_state["username"])]=time.time()
    return st.session_state["first_time"]





def tim():
    st.session_state["t0"] = time.time()
    return st.session_state["t0"]

@st.cache(allow_output_mutation=True)
def get_data():
    return []



if check_password():
    kos,st.session_state["username"]=check_password()
    DFST=get_data()
    st.title('Benvenuto al Bordo Gentile {} 🚀'.format(st.session_state["username"]))
    st.title('Controlla lo stato della sua esame per favore')
    if st.button("check"):
        if st.session_state["username"] in df['Username'].to_list():
            st.session_state['usercheck']=False
            st.write('l\'esame gia registrato 😊.')
        elif st.session_state["username"] not in st.secrets['passwords'].keys():
            st.write('😕 User not known')
        else:
            st.write('L\'esame è iniziato, ricorda che ha 5 minuti. Dopo 5 minuti ancora si può registerare l\'esame, pero non si può superare')
            st.write('prepara il suo tempo')
            st.session_state['usercheck']=True
            st.session_state['st']=True
            st.session_state["t0"]=tim()
            st.session_state["first_time"]=tim_first()
    if st.session_state['usercheck']==True:
        if st.session_state["st"]==True:
            Nome = st.text_input("Nome:")
            Cognome = st.text_input("Cognome:")
            sodisfazione = st.slider("Sodisfazione", 0, 100)
            Qa=st.radio("1)    "+questions[str(st.session_state["rn"][0])],st.session_state["cho0"],horizontal=False)
            Qb=st.radio("2)    "+questions[str(st.session_state["rn"][1])],st.session_state["cho1"],horizontal=False)
            Qc=st.radio("3)    "+questions[str(st.session_state["rn"][2])],st.session_state["cho2"],horizontal=False)
            Qd=st.radio("4)    "+questions[str(st.session_state["rn"][3])],st.session_state["cho3"],horizontal=False)
            Qe=st.radio("5)    "+questions[str(st.session_state["rn"][4])],st.session_state["cho4"],horizontal=False)
            if st.button("Submit"):
                DFST=pd.DataFrame({"Username":st.session_state["username"],"Nome": Nome,"Cognome":Cognome, "Livello_sodisfazione": sodisfazione, "q1": Qa, "q2": Qb, "q3": Qc, "q4": Qd, "q5": Qe, "time":time.time()-st.session_state["t0"]},index=[0])
                st.session_state["B"]=pd.DataFrame({"Username":st.session_state["username"],"Nome": Nome,"Cognome":Cognome, "Livello_sodisfazione": sodisfazione, "q1": st.session_state["che0"][st.session_state["cho0"].index(Qa)], "q2": st.session_state["che1"][st.session_state["cho1"].index(Qb)], "q3": st.session_state["che2"][st.session_state["cho2"].index(Qc)], "q4": st.session_state["che3"][st.session_state["cho3"].index(Qd)], "q5": st.session_state["che4"][st.session_state["cho4"].index(Qe)], "time":(time.time()-st.session_state["t0"])//60, "first_time":(time.time()-st.session_state["first_time"]['{}'.format(st.session_state["username"])])//60},index=[0])
                st.write(DFST)
            st.title('Se Lei è sicuro da chiudere l\'esamae, premi conferma')
            if st.button("Confirm"):
                #L=len(pd.DataFrame(get_data()))
                #dx=df.append(st.session_state["B"].iloc[-1,:],ignore_index=True)
                #sql = """INSERT INTO qst (Username, Nome, Cognome,Livello_sodisfazione, q1, q2,q3 ,q4 ,q5 , time) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format("Username".loc[-1],"Nome".loc[-1],"Cognome".loc[-1], "Livello sodisfazione".loc[-1], "q1".loc[-1], "q2".loc[-1], "q3".loc[-1], "q4".loc[-1], "q5".loc[-1], "time".loc[-1])
                sql = """INSERT INTO qst (Username, Nome, Cognome,Livello_sodisfazione, q1, q2,q3 ,q4 ,q5 , time, first_time) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format (st.session_state["B"].loc[0,"Username"] ,st.session_state["B"].loc[0,"Nome"] , st.session_state["B"].loc[0,"Cognome"] ,st.session_state["B"].loc[0,"Livello_sodisfazione"] , st.session_state["B"].loc[0,"q1"] , st.session_state["B"].loc[0,"q2"] ,st.session_state["B"].loc[0,"q3"] ,st.session_state["B"].loc[0,"q4"] ,st.session_state["B"].loc[0,"q5"]  ,st.session_state["B"].loc[0,"time"], st.session_state["B"].loc[0,"first_time"])
                #sql = """INSERT INTO qst2 (Username, Nome, Cognome,Livello_sodisfazione, q1, q2,q3 ,q4 ,q5 , time) VALUES ('{}','{}')""".format (dx["grade"].iloc[-1],dx["number"].iloc[-1])

                cursor = conn.cursor()
                cursor.execute(sql)
                st.title('la sua esame è finito 😊.')
                st.title("Grazie per la collaborazione! 😍")
                st.session_state["st"]=False
        else:
            st.title('l\'esame gia registrato 😊.')
