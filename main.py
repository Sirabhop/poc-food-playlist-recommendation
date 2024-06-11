import streamlit as st
import pandas as pd

from src.recommend import recommender, topHit_emoji

st.set_page_config(
    page_title="poc-food-recommendation",
    page_icon="🍔",
    layout="wide"
)

st.title('🍔 Robinhood Food Recommendation')
st.markdown('POC **Multi-Modal Encoder** for Restaurant Recommendation')

rec_engine = recommender()

# Initialize Session State
if 'df_shop' not in st.session_state:
    df_shop = pd.read_csv("./data/shop_meta_data.csv", usecols=['shop_id', 'shop_photo', 'shop_category', 'shop_name'])
    df_shop['favorite'] = False
    df_shop['shop_photo'] = df_shop['shop_photo'].apply(lambda x: f"{st.secrets['BASE_URL']}{x}")
    st.session_state.df_shop = df_shop  # Store in session state


with st.form("favorite_section"):
    st.header("Select your favorite restuarant:")
    edited_df = st.data_editor(
        st.session_state.df_shop,  # Use the session state data
        column_config={
            "favorite": st.column_config.CheckboxColumn(
                "Your Fav?",
                help="Select your favorite restuarant",
                default=False,
            ),
            "shop_photo": st.column_config.ImageColumn(
                "Restaurant Image"
            ),
        },
        disabled=["shop_id"],
        hide_index=True,
        use_container_width=True
    )

    if st.form_submit_button("Update"):
        st.session_state.df_shop = edited_df  # Update session state
        
        dish_bubble = rec_engine.get_dish_bubble(df = st.session_state.df_shop)

        st.header("Dish Bubble:")
        row = st.columns(10)

        for i, col in enumerate(row):
              tile = col.container(height=140)
              tile.title(topHit_emoji[dish_bubble[i]])
              tile.markdown(dish_bubble[i])
              
        
        st.header("Playlist:")
        recommended_shop = rec_engine.get_playlist(df = st.session_state.df_shop, k=10)
        playlist_df = st.data_editor(
            df_shop.loc[df_shop.shop_id.isin(recommended_shop), ['shop_photo', 'shop_name']],
            column_config={
                "shop_photo": st.column_config.ImageColumn(
                        "Restaurant Image"
                ),
                "shop_name": st.column_config.TextColumn(
                    "Restaurant Name",
                
            ),
            },
            hide_index=True,

            
        )
