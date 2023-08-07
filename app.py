import streamlit as st

APP_TITLE = 'Electricity Generation in Canada'
APP_SUB_TITLE = 'Source: Stats Canada'

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)


if __name__ == '__main__':
    main()