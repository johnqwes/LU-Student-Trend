import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import pickle
from sklearn.linear_model import LinearRegression
import plotly.express as px
import os
import io
import base64
import pyrebase
import time

st.set_page_config(page_title="LU Student Trend", page_icon=":bar_chart:", layout="wide")

DATA_FILE = 'data.csv'
MODEL_FILE = 'linear_regression_model.pkl'

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def save_data(data):
    data.to_csv(DATA_FILE, index=False)

# Function to load and save data
def load_data():
    return pd.read_csv(DATA_FILE)

img = get_img_as_base64("green.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://scontent.fmnl30-2.fna.fbcdn.net/v/t1.15752-9/386888887_1808215622946295_7167277091580316419_n.png?_nc_cat=110&ccb=1-7&_nc_sid=8cd0a2&_nc_eui2=AeEktddWvYozZUVM82TXQDjB4v6ietPoZo_i_qJ60-hmj7OkSVeDoCP8o8vjxQRLM38cHCxa2jRqHq-98d_FljM4&_nc_ohc=5oGrhUn9VyEAX-pDzkq&_nc_ht=scontent.fmnl30-2.fna&oh=03_AdStqDQO54DcdfqAuMilRX16-ww-uJTWQIA1jcVNjwIZhg&oe=659E462F");
background-size: cover;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# Firebase initialization
firebaseConfig = {
    "apiKey": "AIzaSyCM-2QTRJPaDaPZnXRR5aSqkZRAIPFLaQg",
    "authDomain": "streamlit-cde99.firebaseapp.com",
    "databaseURL": "https://streamlit-cde99.firebaseio.com",
    "projectId": "streamlit-cde99",
    "storageBucket": "streamlit-cde99.appspot.com",
    "messagingSenderId": "651067602910",
    "appId": "1:651067602910:web:b98e16ab9aa07fd4000f4f",
    "measurementId": "G-XEQM0PYDYZ",
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Function to authenticate user
def authenticate(email, password):
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        return login
    except Exception as e:
        error_message = str(e)
        if "INVALID_PASSWORD" in error_message:
            st.toast("Invalid password. Please check your password.")
            time.sleep(2)
        elif "INVALID_EMAIL" in error_message:
            st.toast("Invalid email address. Please check your email.")
            time.sleep(2)
        else:
            st.toast("Please make sure if your email is correct")
            time.sleep(2)
        return None
    
# Function to send a password reset email
def send_password_reset_email(email):
    if not email:
        st.toast("Please, input email.")
        time.sleep(2)
        return

    try:
        auth.send_password_reset_email(email)
        st.toast("Password reset email sent.")
        time.sleep(2)
    except Exception as e:
        error_message = str(e)
        if "INVALID_EMAIL" in error_message:
            st.toast("Invalid email address. Please check your email.")
            time.sleep(2)
        elif "MISSING_EMAIL" in error_message:
            st.toast("Missing email address. Please enter your email.")
            time.sleep(2)
        else:
            st.toast(f"Error sending password reset email: {e}")
            time.sleep(2)


# Function to logout user
def logout():
    # Clear user info from session state
    st.session_state.user = None

# Streamlit app content
def main():

    # Create a session state object
     if 'user' not in st.session_state:
        st.session_state.user = None

     if st.session_state.user is None:
        st.markdown("<h1 style=' color: #545454;'>LOGIN</h1>", unsafe_allow_html=True)

        st.markdown(
        """
        <style>
        .st-emotion-cache-q8sbsg p {
            color: black;
        }
        .st-emotion-cache-16idsys p{
            color: #545454;
        }
        button.st-emotion-cache-hc3laj.ef3psqc12 {
            background-color: #2ECC71;
            position: relative;
            border: 1px solid black;
            margin: 0;
            color: #fff;
            display: inline-block;
            text-decoration: none;
            text-align: center;
        }
        .st-b2 {
        background-color: white;
        }
            button.st-emotion-cache-13ejsyy.ef3psqc12{
            background-color: #2f9e36;
            color: #fff;
            transition: 0.2s;
            height: 2.5rem;
        }
        div.st-emotion-cache-1wmy9hl.e1f1d6gn0{
            width: 325px;
            height: 400px;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            margin: 20px;
            padding: 10px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            left: 30px;
            border: 3px solid #73AD21;
            border-radius: 2rem;
            margin-top: 90px;
        }
        .st-bo{
            width: 300px;
        }
        .st-emotion-cache-10trblm{
            font-size: 25px;
            text-align: center;
            margin-right: 20px;
        }
        .st-emotion-cache-1vbkxwb p{
            font-size: 12px;
            text-align: center;
        }
        button.st-emotion-cache-7ym5gk.ef3psqc12{
           
            height: 1px;
        }
        .st-gw{
            height: auto;
            width: 300px;
        }
        .st-h9{
            
        }
        </style>
        """,
        unsafe_allow_html=True
    )

        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")

        login_button_clicked = st.button("Login", key="login_button")
        reset_button_clicked = st.button("Forgot Password", key="reset_button")

        if login_button_clicked:
            if email and password:
                user = authenticate(email, password)
                if user:
                    st.session_state.user = user
                    st.toast("Login successful.")
                    time.sleep(1)
            else:
                st.toast("Please enter both email and password.")
                time.sleep(2)
        if reset_button_clicked:
            send_password_reset_email(email)

     else:

        with open('style.css') as f:
         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        # Create tabs
        st.sidebar.header("✅ WELCOME TO LU STUDENT TREND")
        st.sidebar.header("")
        
        tabs = st.sidebar.radio("SELECT TAB:", ["📊 Dashboard", ":chart_with_upwards_trend: Enrollment", ":chart_with_downwards_trend: Dropout", "🎓 Graduate", "🆕 Add new data"])

        data = pd.read_csv('data.csv')
        data = data.dropna()

        if tabs == "📊 Dashboard":
                
                st.markdown("<h1 style='color: #E97451;'>📊 Student Trend Dashboard</h1>", unsafe_allow_html=True)
                st.markdown("")   

                fl = st.file_uploader(" UPLOAD A FILE", type=["csv"])

                if fl is not None:
                    # Read the contents of the uploaded file as bytes
                    file_contents = fl.getvalue()

                    # Decode bytes to string assuming it's a CSV file (change encoding if necessary)
                    stringio = io.StringIO(file_contents.decode("ISO-8859-1"))

                    # Use Pandas to read the string as a CSV
                    df = pd.read_csv(stringio)
                    st.write(df)  # Display the DataFrame in Streamlit
                else:
                    df = pd.read_csv("visual_data.csv", encoding="ISO-8859-1")

                col1, col2 = st.columns((2))

                st.header("⭐ Choose your filter: ")
                # Create for Program
                program = st.multiselect("Select Program:", df["Program"].unique())
                if not program:
                    df2 = df.copy()
                else:
                    df2 = df[df["Program"].isin(program)]

                # Create for Year
                year = st.multiselect("Select School Year:", df2["Year"].unique())
                if not year:
                    df3 = df2.copy()
                else:
                    df3 = df2[df2["Year"].isin(year)]

                # Filter the data based on Region, State and City

                if not program:
                    filtered_df = df
                elif not year:
                    filtered_df = df[df["Program"].isin(program)]
                elif not program:
                    filtered_df = df[df["Year"].isin(year)]
                elif year:
                    filtered_df = df3[df["Year"].isin(year)]
                elif program:
                    filtered_df = df3[df["Program"].isin(program)]
                elif program and year:
                    filtered_df = df3[df["Program"].isin(program) & df3["Year"].isin(year)]
                else:
                    filtered_df = df3[df3["Program"].isin(program) & df3["Year"].isin(year)]

                program_df = filtered_df.groupby(by = ["Program"], as_index = False)["Enrollees"].sum()

                # Generate a bar chart for enrollment
                st.markdown("<h2 style='color: #E97451;'>📈 Enrollees</h2>", unsafe_allow_html=True)
                fig_enrollment = px.bar(
                    program_df,
                    x="Program",
                    y="Enrollees",
                    text=['{:,.0f}'.format(x) for x in program_df["Enrollees"]],
                    template="plotly_dark",
                    labels={"Enrollees": "Number of Enrollees"},
                    color="Enrollees",
                    color_continuous_scale=px.colors.sequential.Viridis,
                )

                fig_enrollment.update_traces(textposition='outside')
                fig_enrollment.update_layout(
                    xaxis_title='Program',
                    yaxis_title='Number of Enrollees',
                    showlegend=False,
                    plot_bgcolor='#FFF',
                    paper_bgcolor='#fff',
                    height=500,
                )
                st.plotly_chart(fig_enrollment, use_container_width=True)

                # Expander for Enrollment data
                with st.expander("Enrollment Data"):
                    st.write(program_df.style.background_gradient(cmap="Blues"))
                    csv_enrollment = program_df.to_csv(index=False).encode('utf-8')
                    st.download_button('Download Enrollment Data', data=csv_enrollment, file_name="Enrollment_Data.csv", mime="text/csv")

                # Generate a pie chart for dropout distribution
                st.markdown("<h2 style=' color: #E97451;'>📉 Dropout</h2>", unsafe_allow_html=True)
                fig_dropout = px.pie(
                    filtered_df,
                    values="Dropout",
                    names="Program",
                    hole=0.5,
                    template="plotly_dark",
                )

                fig_dropout.update_traces(textposition='outside', textinfo='percent+label')
                fig_dropout.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    plot_bgcolor='#FFf',
                    paper_bgcolor='#fff',
                    height=500,
                )

                st.plotly_chart(fig_dropout, use_container_width=True)

                # Expander for Dropout data
                with st.expander("Dropout Data"):
                    region = filtered_df.groupby(by="Program", as_index=False)["Dropout"].sum()
                    st.write(region.style.background_gradient(cmap="Oranges"))
                    csv_dropout = region.to_csv(index=False).encode('utf-8')
                    st.download_button('Download Dropout Data', data=csv_dropout, file_name="Dropout_Data.csv", mime="text/csv")
                # Download orginal DataSet
                csv = df.to_csv(index = False).encode('utf-8')
                st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")

        
        with open('stacked_model.pkl', 'rb') as file:
            stacked_model = pickle.load(file)

        if tabs == ":chart_with_upwards_trend: Enrollment":

                st.markdown("<h1 style='color: #E97451;'>📈 Enrollment Prediction</h1>", unsafe_allow_html=True)
                st.markdown("")

                data = pd.read_csv("data.csv", encoding="ISO-8859-1")

                fl = st.file_uploader("UPLOAD A FILE", type=["csv"])

                if fl is not None:
                    # Check if the uploaded file is a CSV
                    if fl.type == 'text/csv':
                        # Read the contents of the uploaded file as bytes
                        file_contents = fl.getvalue()

                        # Decode bytes to string assuming it's a CSV file (change encoding if necessary)
                        stringio = io.StringIO(file_contents.decode("ISO-8859-1"))

                        # Use Pandas to read the string as a CSV
                        uploaded_data = pd.read_csv(stringio)
                        st.write(uploaded_data)  # Display the uploaded DataFrame in Streamlit

                        # Check if the uploaded CSV has the required columns for predictions
                        required_columns = ['School Year', 'Program ID', 'Number of Enrollees']  # Adjust column names as needed
                        if all(col in uploaded_data.columns for col in required_columns):
                            # Check column data types for numeric columns
                            numeric_columns = ['School Year', 'Program ID', 'Number of Enrollees']  # Adjust numeric column names
                            correct_data_types = all(uploaded_data[col].dtype in ['int64', 'float64'] for col in numeric_columns)
                            
                            if correct_data_types:
                                data = uploaded_data  # Update 'data' if columns and data types match the required structure
                            else:
                                st.warning("⚠️ Please upload a CSV file with numeric columns for predictions.")
                        else:
                            st.warning("⚠️ Please upload a valid file format")



                st.sidebar.header("⭐ Predict Enrollees")

                with st.expander("VIEW DEFAULT DATA"):
                    st.write(data)  # Display the default data when the expander is expanded

                sy_input = st.sidebar.number_input("Enter the year: ", step=1)
                id_input = st.sidebar.selectbox("Select Program ID: ", data['Program ID'].unique())

                fig = go.Figure()
                prediction_text = ""
                original_text = ""
                show_recommendation_button = False

                if sy_input != 0 and id_input != 0:
                    user_data = [[sy_input, id_input]]
                    predictions = stacked_model.predict(user_data)

                    filtered_data = data[data['Program ID'] == id_input]

                    if len(filtered_data) > 0:
                        fig.add_trace(go.Scatter(
                            x=filtered_data['School Year'],
                            y=filtered_data['Number of Enrollees'],
                            mode='markers',
                            name='Original Data',
                            marker=dict(color='#FF5733', size=12, line=dict(color='#000000', width=0.5)),
                            opacity=0.8,
                            showlegend=True
                        ))

                        original_value = None

                        if sy_input in filtered_data['School Year'].values:
                            original_value = filtered_data[filtered_data['School Year'] == sy_input]
                            fig.add_trace(go.Scatter(
                                x=[sy_input],
                                y=[original_value['Number of Enrollees'].values[0]],
                                mode='markers',
                                name='Original Value',
                                marker=dict(color='#C70039', size=16, symbol='diamond', line=dict(color='#000000', width=1.5)),
                            ))

                        fig.add_trace(go.Scatter(
                            x=[sy_input],
                            y=[predictions[0]],
                            mode='markers',
                            name='Predicted Value',
                            marker=dict(color='#4CAF50', size=16, symbol='star', line=dict(color='#000000', width=1.5)),
                        ))

                        # Adding a trend line based on historical data if enough data points are available
                        if len(filtered_data) > 1:
                            x = filtered_data['School Year'].values.reshape(-1, 1)
                            y = filtered_data['Number of Enrollees'].values
                            model = LinearRegression().fit(x, y)
                            trend_line = model.predict(x)
                            fig.add_trace(go.Scatter(
                                x=filtered_data['School Year'],
                                y=trend_line,
                                mode='lines',
                                name='Trend Line',
                                line=dict(color='#00FFFF', width=3),
                            ))

                        fig.update_layout(
                            title_text='Enrollees Prediction',
                            title_font=dict(size=28, family='Arial, sans-serif', color='#333333'),
                            title_x=0.33,  # Centers the title horizontally
                            title_y=0.95,  # Adjusts the vertical position of the title
                            xaxis=dict(title='School Year', tickfont=dict(size=14, color='#333333')),
                            yaxis=dict(title='Number of Enrollees', tickfont=dict(size=14, color='#333333')),
                            showlegend=True,
                            legend=dict(
                                x=0,
                                y=1,
                                traceorder="normal",
                                font=dict(family="Arial, sans-serif", size=14, color="#333333"),
                                bgcolor="#f7f7f7",
                                bordercolor="#333333",
                                borderwidth=1
                            ),
                            hovermode='closest',
                            plot_bgcolor='#f0f0f0',  # Background color of the plot
                            paper_bgcolor='#ffffff',  # Background color of the paper/plot area
                            width=860,  # Adjust the width of the plot
                            height=600,  # Adjust the height of the plot
                            margin=dict(l=80, r=80, t=100, b=80),  # Adjust margins for better display
                            transition={'duration': 1000}  # Add smooth transition/animation
                        )
                        prediction_text = f"**Predicted Value:** {round(predictions[0])}"
                        if original_value is not None:
                            original_text = f"**Original Value:** {original_value['Number of Enrollees'].values[0]}"

                        styled_prediction_text = f"<font color='black' size='+5'>{prediction_text}</font>"
                        styled_original_text = f"<font color='black' size='+5'>{original_text}</font>"

                        st.markdown(styled_prediction_text, unsafe_allow_html=True)
                        st.markdown(styled_original_text, unsafe_allow_html=True)

                        # Checking for significant growth to show recommendation button
                        if original_value is None and predictions[0] > 0.5 * filtered_data['Number of Enrollees'].max():
                            show_recommendation_button = True

                st.plotly_chart(fig)

                if show_recommendation_button:
                    col1, col2, col3 = st.columns([1, 6, 1])
                    with col2:
                        if st.button('📝 Show Recommendation', key="recommendation_button", help="Click to see recommendations"):
                            st.markdown("""
                                <div style='color: white;'>
                                    <div style='background-color: #023020; padding: 10px; border-radius: 5px;'>
                                        <strong>✰ Marketing Strategies:</strong> Invest in effective marketing strategies to reach potential students, leveraging social media, digital marketing, and targeted advertising.<br>
                                        <strong>✰ Enhance Programs:</strong> Continuously develop and enhance academic programs, ensuring they are aligned with industry needs and offer unique value.<br>
                                        <strong>✰ Scholarships and Financial Aid:</strong> Increase scholarship opportunities and financial aid packages to attract a diverse pool of students.<br>
                                        <strong>✰ Partnerships and Collaborations:</strong> Forge partnerships with industries, community organizations, and schools to create pipelines and opportunities for enrollment.<br>
                                        <strong>✰ Online Presence:</strong> Expand online education offerings and improve the quality and accessibility of online learning programs.<br>
                                        <strong>✰ Student Support Services:</strong> Enhance student support services like counseling, mentorship programs, and career services to improve student experience and retention.<br>
                                        <strong>✰ Facilities and Campus Life:</strong> Invest in modern facilities, technology, and campus life to attract and retain students.
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

        with open('stacked_model_drop.pkl', 'rb') as file:
            stacked_model = pickle.load(file)

            if tabs == ":chart_with_downwards_trend: Dropout":

                    st.markdown("<h1 style='color: #E97451;'>📉 Dropout Prediction</h1>", unsafe_allow_html=True)
                    st.markdown("")   

                    data = pd.read_csv("data.csv", encoding="ISO-8859-1")

                    fl = st.file_uploader("UPLOAD A FILE", type=["csv"])

                    if fl is not None:
                        # Check if the uploaded file is a CSV
                        if fl.type == 'text/csv':
                            # Read the contents of the uploaded file as bytes
                            file_contents = fl.getvalue()

                            # Decode bytes to string assuming it's a CSV file (change encoding if necessary)
                            stringio = io.StringIO(file_contents.decode("ISO-8859-1"))

                            # Use Pandas to read the string as a CSV
                            uploaded_data = pd.read_csv(stringio)
                            st.write(uploaded_data)  # Display the uploaded DataFrame in Streamlit

                            # Check if the uploaded CSV has the required columns for predictions
                            required_columns = ['School Year', 'Program ID', 'Number of Enrollees']  # Adjust column names as needed
                            if all(col in uploaded_data.columns for col in required_columns):
                                # Check column data types for numeric columns
                                numeric_columns = ['School Year', 'Program ID', 'Number of Enrollees']  # Adjust numeric column names
                                correct_data_types = all(uploaded_data[col].dtype in ['int64', 'float64'] for col in numeric_columns)
                                
                                if correct_data_types:
                                    data = uploaded_data  # Update 'data' if columns and data types match the required structure
                                else:
                                    st.warning("⚠️ Please upload a CSV file with numeric columns for predictions.")
                            else:
                                st.warning("⚠️ Please upload a valid file format")

                    st.sidebar.header("⭐ Predict Dropout")

                    with st.expander("VIEW DEFAULT DATA"):
                     st.write(data)  # Display the default data when the expander is expanded
        
                    sy_input = st.sidebar.number_input("Enter the year: ", step=1)
                    id_input = st.sidebar.selectbox("Select Program ID: ", data['Program ID'].unique())

                    fig = go.Figure()
                    prediction_text = ""
                    original_text = ""
                    show_recommendation_button = False

                    if sy_input != 0 and id_input != 0:
                        user_data = [[sy_input, id_input]]
                        predictions = stacked_model.predict(user_data)

                        filtered_data = data[data['Program ID'] == id_input]

                        if len(filtered_data) > 0:
                            fig.add_trace(go.Scatter(
                                x=filtered_data['School Year'],
                                y=filtered_data['Number of Dropout'],
                                mode='markers',
                                name='Original Data',
                                marker=dict(color='#FF5733', size=12, line=dict(color='#000000', width=0.5)),
                                opacity=0.8,
                                showlegend=True
                            ))

                            original_value = None

                            if sy_input in filtered_data['School Year'].values:
                                original_value = filtered_data[filtered_data['School Year'] == sy_input]
                                fig.add_trace(go.Scatter(
                                    x=[sy_input],
                                    y=[original_value['Number of Dropout'].values[0]],
                                    mode='markers',
                                    name='Original Value',
                                    marker=dict(color='#C70039', size=16, symbol='diamond', line=dict(color='#000000', width=1.5)),
                                ))

                            fig.add_trace(go.Scatter(
                                x=[sy_input],
                                y=[predictions[0]],
                                mode='markers',
                                name='Predicted Value',
                                marker=dict(color='#4CAF50', size=16, symbol='star', line=dict(color='#000000', width=1.5)),
                            ))

                            # Adding a trend line based on historical data if enough data points are available
                            if len(filtered_data) > 1:
                                x = filtered_data['School Year'].values.reshape(-1, 1)
                                y = filtered_data['Number of Dropout'].values
                                model = LinearRegression().fit(x, y)
                                trend_line = model.predict(x)
                                fig.add_trace(go.Scatter(
                                    x=filtered_data['School Year'],
                                    y=trend_line,
                                    mode='lines',
                                    name='Trend Line',
                                    line=dict(color='#00FFFF', width=3),
                                ))

                            fig.update_layout(
                                title_text='Dropout Prediction',
                                title_font=dict(size=28, family='Arial, sans-serif', color='#333333'),
                                title_x=0.33,  # Centers the title horizontally
                                title_y=0.95,  # Adjusts the vertical position of the title
                                xaxis=dict(title='School Year', tickfont=dict(size=14, color='#333333')),
                                yaxis=dict(title='Number of Dropout', tickfont=dict(size=14, color='#333333')),
                                showlegend=True,
                                legend=dict(
                                    x=0,
                                    y=1,
                                    traceorder="normal",
                                    font=dict(family="Arial, sans-serif", size=14, color="#333333"),
                                    bgcolor="#f7f7f7",
                                    bordercolor="#333333",
                                    borderwidth=1
                                ),
                                hovermode='closest',
                                plot_bgcolor='#f0f0f0',  # Background color of the plot
                                paper_bgcolor='#ffffff',  # Background color of the paper/plot area
                                width=860,  # Adjust the width of the plot
                                height=600,  # Adjust the height of the plot
                                margin=dict(l=80, r=80, t=100, b=80),  # Adjust margins for better display
                                transition={'duration': 1000}  # Add smooth transition/animation
                            )
                            prediction_text = f"**Predicted Value:** {round(predictions[0])}"
                            if original_value is not None:
                                original_text = f"**Original Value:** {original_value['Number of Dropout'].values[0]}"

                            styled_prediction_text = f"<font color='black' size='+5'>{prediction_text}</font>"
                            styled_original_text = f"<font color='black' size='+5'>{original_text}</font>"

                            st.markdown(styled_prediction_text, unsafe_allow_html=True)
                            st.markdown(styled_original_text, unsafe_allow_html=True)

                            # Checking for significant growth to show recommendation button
                            if original_value is None and predictions[0] > 0.5 * filtered_data['Number of Dropout'].max():
                                show_recommendation_button = True

                    st.plotly_chart(fig)

                    if show_recommendation_button:
                        col1, col2, col3 = st.columns([1, 6, 1])
                        with col2:
                            if st.button('📝 Show Recommendation', key="recommendation_button", help="Click to see recommendations"):
                                st.markdown("""
                                    <div style='color: white;'>
                                        <div style='background-color: #023020; padding: 10px; border-radius: 5px;'>
                                            <strong>✰ School Culture & Environment:</strong> Cultivate a positive and inclusive school environment while forming community partnerships.<br>
                                            <strong>✰ Technology & Resources:</strong> Ensure access to technology and provide career-focused education programs.<br>
                                            <strong>✰ Continuous Monitoring & Evaluation:</strong> Continuously monitor dropout rates and evaluate interventions' effectiveness.<br>
                                            <strong>✰ Policy & Funding:</strong> Advocate for policy changes and allocate resources to dropout prevention initiatives.<br>
                                            <strong>✰ Collaboration & Professional Development:</strong> Provide teacher training and encourage interdisciplinary collaboration.<br>
                                            <strong>✰ Student Support Services:</strong> Enhance student support services like counseling, mentorship programs, and career services to improve student experience and retention.<br>
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)

        with open('stacked_model_grad.pkl', 'rb') as file:
            stacked_model = pickle.load(file)

            if tabs == "🎓 Graduate":

                    st.markdown("<h1 style='color: #E97451;'>🎓 Graduate Prediction</h1>", unsafe_allow_html=True)
                    st.markdown("")

                    data = pd.read_csv("data.csv", encoding="ISO-8859-1")
                    fl = st.file_uploader("UPLOAD A FILE", type=["csv"])

                    if fl is not None:
                        # Check if the uploaded file is a CSV
                        if fl.type == 'text/csv':
                            # Read the contents of the uploaded file as bytes
                            file_contents = fl.getvalue()

                            # Decode bytes to string assuming it's a CSV file (change encoding if necessary)
                            stringio = io.StringIO(file_contents.decode("ISO-8859-1"))

                            # Use Pandas to read the string as a CSV
                            uploaded_data = pd.read_csv(stringio)
                            st.write(uploaded_data)  # Display the uploaded DataFrame in Streamlit

                            # Check if the uploaded CSV has the required columns for predictions
                            required_columns = ['School Year', 'Program ID', 'Number of Enrollees']  # Adjust column names as needed
                            if all(col in uploaded_data.columns for col in required_columns):
                                # Check column data types for numeric columns
                                numeric_columns = ['School Year', 'Program ID', 'Number of Enrollees']  # Adjust numeric column names
                                correct_data_types = all(uploaded_data[col].dtype in ['int64', 'float64'] for col in numeric_columns)
                                
                                if correct_data_types:
                                    data = uploaded_data  # Update 'data' if columns and data types match the required structure
                                else:
                                    st.warning("⚠️ Please upload a CSV file with numeric columns for predictions.")
                            else:
                                st.warning("⚠️ Please upload a valid file format")

                    st.sidebar.header("⭐ Predict Graduate")

                    with st.expander("VIEW DEFAULT DATA"):
                     st.write(data)  # Display the default data when the expander is expanded
        
                    sy_input = st.sidebar.number_input("Enter the year: ", step=1)
                    id_input = st.sidebar.selectbox("Select Program ID: ", data['Program ID'].unique())
                    en_input = st.sidebar.number_input("Enter no. of Enrollees: ", step=1)

                    fig = go.Figure()
                    prediction_text = ""
                    original_text = ""
                    show_recommendation_button = False

                    if sy_input != 0 and id_input != 0:
                        user_data = [[sy_input, id_input, en_input]]
                        predictions = stacked_model.predict(user_data)

                        filtered_data = data[data['Program ID'] == id_input]

                        if len(filtered_data) > 0:
                            fig.add_trace(go.Scatter(
                                x=filtered_data['School Year'],
                                y=filtered_data['Number of Graduates'],
                                mode='markers',
                                name='Original Data',
                                marker=dict(color='#FF5733', size=12, line=dict(color='#000000', width=0.5)),
                                opacity=0.8,
                                showlegend=True
                            ))

                            original_value = None

                            if sy_input in filtered_data['School Year'].values:
                                original_value = filtered_data[filtered_data['School Year'] == sy_input]
                                fig.add_trace(go.Scatter(
                                    x=[sy_input],
                                    y=[original_value['Number of Graduates'].values[0]],
                                    mode='markers',
                                    name='Original Value',
                                    marker=dict(color='#C70039', size=16, symbol='diamond', line=dict(color='#000000', width=1.5)),
                                ))

                            fig.add_trace(go.Scatter(
                                x=[sy_input],
                                y=[predictions[0]],
                                mode='markers',
                                name='Predicted Value',
                                marker=dict(color='#4CAF50', size=16, symbol='star', line=dict(color='#000000', width=1.5)),
                            ))

                            # Adding a trend line based on historical data if enough data points are available
                            if len(filtered_data) > 1:
                                x = filtered_data['School Year'].values.reshape(-1, 1)
                                y = filtered_data['Number of Graduates'].values
                                model = LinearRegression().fit(x, y)
                                trend_line = model.predict(x)
                                fig.add_trace(go.Scatter(
                                    x=filtered_data['School Year'],
                                    y=trend_line,
                                    mode='lines',
                                    name='Trend Line',
                                    line=dict(color='#00FFFF', width=3),
                                ))

                            fig.update_layout(
                                title_text='Graduate Prediction',
                                title_font=dict(size=28, family='Arial, sans-serif', color='#333333'),
                                title_x=0.33,  # Centers the title horizontally
                                title_y=0.95,  # Adjusts the vertical position of the title
                                xaxis=dict(title='School Year', tickfont=dict(size=14, color='#333333')),
                                yaxis=dict(title='Number of Graduates', tickfont=dict(size=14, color='#333333')),
                                showlegend=True,
                                legend=dict(
                                    x=0,
                                    y=1,
                                    traceorder="normal",
                                    font=dict(family="Arial, sans-serif", size=14, color="#333333"),
                                    bgcolor="#f7f7f7",
                                    bordercolor="#333333",
                                    borderwidth=1
                                ),
                                hovermode='closest',
                                plot_bgcolor='#f0f0f0',  # Background color of the plot
                                paper_bgcolor='#ffffff',  # Background color of the paper/plot area
                                width=860,  # Adjust the width of the plot
                                height=600,  # Adjust the height of the plot
                                margin=dict(l=80, r=80, t=100, b=80),  # Adjust margins for better display
                                transition={'duration': 1000}  # Add smooth transition/animation
                            )
                            prediction_text = f"**Predicted Value:** {round(predictions[0])}"
                            if original_value is not None:
                                original_text = f"**Original Value:** {original_value['Number of Graduates'].values[0]}"

                            styled_prediction_text = f"<font color='black' size='+5'>{prediction_text}</font>"
                            styled_original_text = f"<font color='black' size='+5'>{original_text}</font>"

                            st.markdown(styled_prediction_text, unsafe_allow_html=True)
                            st.markdown(styled_original_text, unsafe_allow_html=True)

                            # Checking for significant growth to show recommendation button
                            if original_value is None and predictions[0] > 0.5 * filtered_data['Number of Graduates'].max():
                                show_recommendation_button = True

                    st.plotly_chart(fig)

                    if show_recommendation_button:
                        col1, col2, col3 = st.columns([1, 6, 1])
                        with col2:
                            if st.button('📝 Show Recommendation', key="recommendation_button", help="Click to see recommendations"):
                                st.markdown("""
                                    <div style='color: white;'>
                                        <div style='background-color: #023020; padding: 10px; border-radius: 5px;'>
                                            <strong>✰ Marketing Strategies:</strong> Invest in effective marketing strategies to reach potential students, leveraging social media, digital marketing, and targeted advertising.<br>
                                            <strong>✰ Enhance Programs:</strong> Continuously develop and enhance academic programs, ensuring they are aligned with industry needs and offer unique value.<br>
                                            <strong>✰ Scholarships and Financial Aid:</strong> Increase scholarship opportunities and financial aid packages to attract a diverse pool of students.<br>
                                            <strong>✰ Partnerships and Collaborations:</strong> Forge partnerships with industries, community organizations, and schools to create pipelines and opportunities for enrollment.<br>
                                            <strong>✰ Online Presence:</strong> Expand online education offerings and improve the quality and accessibility of online learning programs.<br>
                                            <strong>✰ Student Support Services:</strong> Enhance student support services like counseling, mentorship programs, and career services to improve student experience and retention.<br>
                                            <strong>✰ Facilities and Campus Life:</strong> Invest in modern facilities, technology, and campus life to attract and retain students.
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)

            if tabs == "🆕 Add new data":
                    

                    st.markdown("<h1 style='color: #E97451;'>🆕 Add New Program Details</h1>", unsafe_allow_html=True)
                    st.markdown("")

                    operation = ""

       
                    operation = st.selectbox("Select Operation", ["Add New Program", "Add New Data", "Edit Data", "Delete"])

                    if operation == "Add New Program":
                        st.subheader("Add New Program")
                        new_program_name = st.text_input("Enter Program Name", key="program_name")
                        new_enrollees = st.number_input("Enter Number of Enrollees", min_value=0, step=1, key="enrollees")
                            
                        if st.button("Add Program"):
                            new_program_id = data['Program ID'].max() + 1
                            new_year = data['School Year'].max()
                            # Assuming default values for dropouts and graduates for a new program
                            new_dropout = 0
                            new_graduates = 0
                            new_row = {'School Year': new_year, 'Program ID': new_program_id,
                                        'Program Name': new_program_name, 'Number of Enrollees': new_enrollees,
                                            'Number of Dropout': new_dropout, 'Number of Graduates': new_graduates}
                            data = data.append(new_row, ignore_index=True)
                            save_data(data)

                                # Check if data was added before showing the success message
                            if len(data) > 0:
                                st.success("New program added successfully!")
                            else:
                                st.warning("No data added. Please fill in the required fields.")

                    if operation == "Add New Data":
                        st.subheader("Add New Data")
                        program_id = st.selectbox("Select Program ID", data['Program ID'].unique())
                        selected_program = data[data['Program ID'] == program_id]['Program Name'].values[0]  # Get the program name for the selected ID
                        new_year = st.number_input("Enter School Year", min_value=int(data['School Year'].max() + 1), step=1, key="new_year")
                        new_enrollees = st.number_input("Enter Number of Enrollees", min_value=0, step=1, key="new_enrollees")
                        new_dropout = st.number_input("Enter Number of Dropout", min_value=0, step=1, key="new_dropout")
                        new_graduates = st.number_input("Enter Number of Graduates", min_value=0, step=1, key="new_graduates")
                        if st.button("Save"):
                            new_row = {'School Year': new_year, 'Program ID': program_id,
                                        'Program Name': selected_program,  # Add the selected program name here
                                        'Number of Enrollees': new_enrollees, 'Number of Dropout': new_dropout,
                                        'Number of Graduates': new_graduates}
                            data = data.append(new_row, ignore_index=True)
                            save_data(data)
                            st.success("New data added successfully!")

                    
                    if operation == "Edit Data":
                        st.subheader("Edit Data")
                        
                        # Allow users to select the program and school year to edit
                        program_id_to_edit = st.selectbox("Select Program ID to Edit", data['Program ID'].unique())
                        selected_data = data[data['Program ID'] == program_id_to_edit]
                        
                        if not selected_data.empty:
                            selected_year_to_edit = st.selectbox("Select School Year to Edit", selected_data['School Year'].unique())
                            selected_year_data = selected_data[selected_data['School Year'] == selected_year_to_edit]

                            if not selected_year_data.empty:
                                # Display the existing data for editing
                                st.write("Existing Data:")
                                st.write(selected_year_data)

                                # Allow editing the fields
                                new_enrollees = st.number_input("Enter New Number of Enrollees", min_value=0, step=1, key="edit_enrollees")
                                new_dropout = st.number_input("Enter New Number of Dropout", min_value=0, step=1, key="edit_dropout")
                                new_graduates = st.number_input("Enter New Number of Graduates", min_value=0, step=1, key="edit_graduates")

                                if st.button("Update Data"):
                                    # Update the selected data with the new values
                                    data.loc[(data['Program ID'] == program_id_to_edit) & (data['School Year'] == selected_year_to_edit), 'Number of Enrollees'] = new_enrollees
                                    data.loc[(data['Program ID'] == program_id_to_edit) & (data['School Year'] == selected_year_to_edit), 'Number of Dropout'] = new_dropout
                                    data.loc[(data['Program ID'] == program_id_to_edit) & (data['School Year'] == selected_year_to_edit), 'Number of Graduates'] = new_graduates
                                    save_data(data)
                                    st.success("Data updated successfully!")

                            else:
                                st.warning("No data found for the selected School Year.")
                        else:
                            st.warning("No data found for the selected Program ID.")

                    
                    if operation == "Delete":
                        st.subheader("Delete Data")

                        # Create a drop-down selectbox for Program ID
                        program_id_options = data['Program ID'].unique()
                        selected_program_id = st.selectbox("Select Program ID to Delete", program_id_options)

                        year_to_delete = st.number_input("Enter School Year to Delete", min_value=int(data['School Year'].min()), step=1, key="delete_year")

                        if st.button("Confirm Deletion", key="delete_button"):
                            # Check if data exists for the specified program ID and school year
                            # This line filters the data based on the conditions
                            if ((data['Program ID'] == selected_program_id) & (data['School Year'] == year_to_delete)).any():
                                # Remove data for the specified program ID and school year
                                data = data[~((data['Program ID'] == selected_program_id) & (data['School Year'] == year_to_delete))]
                                # Assuming you have a function like save_data(data) to save the DataFrame
                                save_data(data)
                                st.success("Data deleted successfully!")
                            else:
                                st.warning("No data found for the specified Program ID and School Year.")


                

        if st.sidebar.button("Logout", on_click=logout):
            logout()  # Call the logout function to clear session state

if __name__ == "__main__":
    main()