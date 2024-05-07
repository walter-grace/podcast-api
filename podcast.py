import streamlit as st
import requests
import csv
import base64

def search_podcasts(query):
    url = "https://listennotes.p.rapidapi.com/api/v1/typeahead"
    querystring = {"q": query, "safe_mode": "1", "show_genres": "1", "show_podcasts": "1"}
    headers = {
        "X-RapidAPI-Key": "5a7c97415bmsh6e460ae309db745p1a9ac3jsnc27ca9fad319",
        "X-RapidAPI-Host": "listennotes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def create_csv(podcasts):
    filename = "podcast_results.csv"
    fieldnames = ["Title", "Publisher", "Thumbnail URL", "Podcast Link"]

    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for podcast in podcasts:
            podcast_url = f"https://www.listennotes.com/podcasts/{podcast['id']}/"
            writer.writerow({
                "Title": podcast["title_original"],
                "Publisher": podcast["publisher_original"],
                "Thumbnail URL": podcast["thumbnail"],
                "Podcast Link": podcast_url
            })

    return filename

def download_csv(filename):
    with open(filename, "r") as file:
        csv_data = file.read()

    b64 = base64.b64encode(csv_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    return href

def main():
    st.title("Podcast Search")
    st.write("Enter a subject to search for relevant podcasts:")

    query = st.text_input("Search query")

    if st.button("Search"):
        results = search_podcasts(query)

        if "podcasts" in results:
            podcasts = results["podcasts"]

            if len(podcasts) > 0:
                st.subheader("Search Results")
                for podcast in podcasts:
                    st.write(f"**Title:** {podcast['title_original']}")
                    st.write(f"**Publisher:** {podcast['publisher_original']}")
                    st.image(podcast['thumbnail'], width=200)

                    podcast_url = f"https://www.listennotes.com/podcasts/{podcast['id']}/"
                    st.write(f"Link: [{podcast_url}]({podcast_url})")

                    st.write("---")

                csv_filename = create_csv(podcasts)
                download_link = download_csv(csv_filename)
                st.markdown(download_link, unsafe_allow_html=True)
            else:
                st.write("No podcasts found for the given subject.")
        else:
            st.write("No results found.")

if __name__ == "__main__":
    main()