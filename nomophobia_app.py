import streamlit as st
# Page config
st.set_page_config(
    page_title="استبيان فردي",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)
from streamlit_cookies_manager import EncryptedCookieManager
import mysql.connector
cook = EncryptedCookieManager(prefix="nomophobia_app" , password="fghhhjfjfhjvhfgc")
mydb = mysql.connector.connect(
  host="sql7.freesqldatabase.com",
  user="sql7774384",
  password="3MKZzQs8DY" , 
  database="sql7774384" , 
    charset ="utf8mb4" 
)
mycursor = mydb.cursor()
# Custom CSS to support RTL (Right-to-Left) for Arabic
st.markdown("""
<style>
    body {
        direction: rtl;
    }
    .stRadio > div {
        flex-direction: row-reverse;
    }
    .stButton button {
        float: right;
    }
    h1, h2, h3, h4, h5, h6, p, div {
        text-align: right;
    }
    .css-1kyxreq {
        justify-content: flex-end;
    }
    .stMarkdown {
        text-align: right;
    }
    @media only screen and (max-width: 500px) {
    .stRadio > div { 
        flex-direction: column;
        align-items: flex-start;
        }
    }

</style>
""", unsafe_allow_html=True)
if not cook.ready():
    st.spinner()
    st.stop()
print(cook.get("visited"))
if cook.get("visited") == 'true': 
    st.error("الرجاء تحديث الصفحة")
    st.stop()
# تعريف الأسئلة
questions = [
    "أشعر بالضيق عندما لا أتمكن من الوصول إلى المعلومات عبر هاتفي",
    "أشعر بعدم الراحة إذا لم أتمكن من التواصل مع عائلتي وأصدقائي فورًا",
    "أشعر بالقلق إذا نفدت بطارية هاتفي",
    "أبدأ في التوتر عندما لا أستطيع معرفة آخر الأخبار عبر الإنترنت من خلال الهاتف",
    "أشعر بالانزعاج إذا كنت غير قادر على استخدام هاتفي عند الحاجة",
    "أشعر بالقلق عندما لا أتمكن من التحقق من الرسائل أو الإشعارات",
    "أتوتر إذا فقدت الاتصال بالإنترنت عبر الهاتف",
    "أشعر بالذعر إذا لم أتمكن من إيجاد هاتفي",
    "أشعر بالوحدة عندما لا أكون قادرًا على استخدام هاتفي",
    "أشعر بأنني خارج الحياة الاجتماعية عندما لا أستطيع استخدام الهاتف" , 
    "أشعر بالقلق إذا لم أتمكن من البقاء على اتصال دائم عبر الهاتف",
    "أشعر بالتوتر عندما أضطر للابتعاد عن هاتفي لفترة طويلة",
    "أشعر بالخوف من فقدان صوري وملفاتي في الهاتف",
    "أشعر بالقلق عند التفكير في أن هاتفي قد يُفقد أو يُسرق",
    "أشعر أنني أعتمد على الهاتف للبقاء على تواصل مع العالم",
    "أجد صعوبة في التركيز عندما لا يكون هاتفي بجانبي",
    "أتحقق من هاتفي باستمرار حتى بدون وجود إشعارات",
    "أشعر بالعجز عندما لا أستطيع استخدام هاتفي أثناء التنقل",
    "أشعر بعدم الأمان بدون هاتفي",
    "أجد صعوبة في قضاء وقت فراغي دون الهاتف" , 
    "هل ترى نفسك تعاني من النوموفوبيا "
]

# مقياس الإجابة
likert_options = {
    "لا أوافق بشدة": 1,
    "لا أوافق": 2,
    "محايد": 3,
    "أوافق": 4,
    "أوافق بشدة": 5
}
likert_options_2 = {
    "لا": 1,
    "ربما": 2,
    "نعم": 3
}
# عنوان التطبيق
st.title("📱 دراسة ميدانية")


# إنشاء علامات تبويب للاستبيان والبيانات
tab1 = st.tabs(["اسبيان الفردي"])

with tab1[0]:
    st.subheader("استبيان الفردي")
    
    
    # جمع الإجابات
    responses = {}
    total_score = 0
    reponse_21 = None
    with st.form("nomophobia_form"):
        st.subheader("الأسئلة:")
        
        for i, question in enumerate(questions[:-1], 1):
            st.write(f"{i}. {question}")
            response = st.radio(
                f"إجابتك على السؤال {i}:", 
                options=list(likert_options.keys()), 
                key=f"q{i}",
                horizontal=True,
                label_visibility="collapsed"
            )
            responses[question] = response
            total_score += likert_options[response]
        st.write(f"{21}. {questions[-1]}")
        response = st.radio(
            "21إجابتك على السؤال:", 
            options=list(likert_options_2.keys()), 
            key="q21",
            horizontal=True,
            label_visibility="collapsed"
        )
        responses[questions[-1]] = response
        reponse_21 = likert_options_2[response]
        submitted = st.form_submit_button("احسب النتيجة")
    if submitted :
        try : 
            result =  None
            if ( total_score >= 20 and total_score <= 39) : 
                result = "نتيجة منخفضة"
            elif total_score >= 40 and total_score <= 59:
                result = "نتيجة متوسطة"
            elif total_score >= 60 and total_score <= 79:
                result = "نتيجة عالية"
            elif total_score >= 80 and total_score <= 100 :
                result = "نتيجة عالية جدا"
                
            sql = "INSERT INTO scores (score) VALUES (%s)"
            val = (result , ) 
            mycursor.execute(sql, val)
            
            

            reponse_21=responses[questions[-1]]
        
            sql = "INSERT INTO question (answer) VALUES (%s)"
            val = (reponse_21 , ) 
            mycursor.execute(sql, val)
        
            mydb.commit()
            
            cook["visited"] = "true" 
            cook.save()
            st.success("تم الحفظ بنجاح")
            st.rerun()
        except Exception as ex :
            st.error("حدث خطأ أثناء الحفظ" + str(ex) )
