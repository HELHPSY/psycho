import streamlit as st
import streamlit_cookies_manager as cookies
# Page config
st.set_page_config(
    page_title="مقياس النوموفوبيا",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)
cookies = cookies.EncryptedCookieManager(
    # This prefix will get added to all your cookie names.
    # This way you can run your app on Streamlit Cloud without cookie name clashes with other apps.
    prefix="ktosiek/streamlit-cookies-manager/",
    # You should really setup a long COOKIES_PASSWORD secret if you're running on Streamlit Cloud.
    password='hsxhswshvshdwvvdh',
)
if not cookies.ready():
    # Wait for the component to load and send us current cookies.
    st.stop()
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
cook.load()
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
            file1=open("RESULT.csv" , "a")
            file2 = open("RESULT_2.csv" , "a")
            result =  None
            if ( total_score >= 20 and total_score <= 39) : 
                result = "نتيجة منخفضة"
            elif total_score >= 40 and total_score <= 59:
                result = "نتيجة متوسطة"
            elif total_score >= 60 and total_score <= 79:
                result = "نتيجة عالية"
            elif total_score >= 80 and total_score <= 100 :
                result = "نتيجة عالية جدا"
            file1.write(f"{result}\n")




            reponse_21=responses[questions[-1]]
            file2.write(f"{reponse_21}\n")

            
            cook.set("visited" , "true")
            cook.save()
            st.success("تم الحفظ بنجاح")
            st.stop()

            file1.close()  
            file2.close()
        except FileNotFoundError:
            st.error("حدث خطأ أثناء الحفظ")
