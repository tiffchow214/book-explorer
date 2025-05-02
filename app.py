import streamlit as st
import pandas as pd
import plotly.express as px  # Using Plotly for emoji support

# Load your data
df = pd.read_csv("books.csv", encoding="utf-8-sig")

# Data source
st.markdown("🔗 **Data scraped from:** [books.toscrape.com](http://books.toscrape.com)")

# Page title
st.title("📚 Book Explorer")
st.markdown("Welcome to Tiff's first Streamlit app! 💫")

# Emoji rating map
emoji_map = {
    "One": "⭐",
    "Two": "⭐⭐",
    "Three": "⭐⭐⭐",
    "Four": "⭐⭐⭐⭐",
    "Five": "⭐⭐⭐⭐⭐"
}

# Label for charts (emojis)
chart_label_map = {
    "One": "1⭐",
    "Two": "2⭐",
    "Three": "3⭐",
    "Four": "4⭐",
    "Five": "5⭐"
}

# Filters in order
rating_order = ["One", "Two", "Three", "Four", "Five"]
available_ratings = [r for r in rating_order if r in df["rating"].unique()]
rating_filter = st.selectbox("📊 Filter by rating:", ["All"] + available_ratings)
price_sort = st.radio("💸 Sort by price:", ["Low to High", "High to Low"])

# Filtered copy
filtered_df = df.copy()
if rating_filter != "All":
    filtered_df = filtered_df[filtered_df["rating"] == rating_filter]

# Convert price to float
filtered_df["price"] = (
    filtered_df["price"]
    .str.strip()
    .replace(r"[^\d\.]", "", regex=True)
    .astype(float)
)

# Apply emojis to rating column
filtered_df["rating"] = filtered_df["rating"].map(emoji_map)

# Sort by price
filtered_df = filtered_df.sort_values(by="price", ascending=(price_sort == "Low to High"))

# 📊 Book Ratings Chart
st.subheader("📊 Book Ratings Distribution")
chart_type = st.selectbox("📊 Choose chart type:", ["Bar", "Pie"])

# Count and relabel for chart
rating_counts = df["rating"].value_counts().reindex(rating_order)
rating_counts.index = rating_counts.index.map(chart_label_map)

# Chart rendering using Plotly
chart_df = pd.DataFrame({
    "Rating": rating_counts.index,
    "Count": rating_counts.values
})

if chart_type == "Bar":
    fig = px.bar(chart_df, x="Rating", y="Count", text="Count", color="Rating")
    fig.update_layout(showlegend=False, xaxis_title="Rating", yaxis_title="Number of Books")
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = px.pie(chart_df, values="Count", names="Rating", hole=0.3)
    fig.update_traces(textinfo="label+percent")
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# Display filtered books
st.write(f"### Showing {len(filtered_df)} books:")
st.dataframe(filtered_df.reset_index(drop=True))

# Raw data section
with st.expander("📂 See raw data"):
    st.dataframe(df.reset_index(drop=True))

# Download button
st.download_button(
    label="📥 Download full dataset as CSV",
    data=df.to_csv(index=False),
    file_name='books_raw.csv',
    mime='text/csv'
)

