import streamlit as st
import facebook
import requests
import pandas as pd

# Remplacez ces valeurs par les vôtres
#ACCESS_TOKEN = ''
#PAGE_ID = ''

def get_facebook_posts(access_token, page_id):
    graph = facebook.GraphAPI(access_token)
    
    try:
        # Tentative d'accès aux publications
        posts = graph.get_connections(id=page_id, connection_name='posts', fields='message,full_picture')
    except facebook.GraphAPIError as e:
        st.error(f"GraphAPIError: {e}")
        return []

    posts_data = []

    while True:
        try:
            # Traiter les publications
            for post in posts.get('data', []):
                post_id = post.get('id')
                message = post.get('message', '')
                image_url = post.get('full_picture', '') if 'full_picture' in post else ''
                
                posts_data.append({
                    'Post ID': post_id,
                    'Message': message,
                    'Image URL': image_url
                })
                
            # Pagination
            if 'paging' in posts and 'next' in posts['paging']:
                posts = requests.get(posts['paging']['next']).json()
            else:
                break
        except KeyError:
            break

    return posts_data

def main():
    st.title('Extraction des Publications Facebook')

    st.write("Jeton d'accès et ID de la page sont codés en dur.")
    
    # Utilisation des valeurs codées en dur
    access_token = ACCESS_TOKEN
    page_id = PAGE_ID

    if st.button('Extraire les Publications'):
        if access_token and page_id:
            posts_data = get_facebook_posts(access_token, page_id)
            
            if posts_data:
                df = pd.DataFrame(posts_data)

                st.subheader('Publications récupérées')
                st.write(df)

                st.subheader('Images des Publications')
                for index, row in df.iterrows():
                    if row['Image URL']:
                        st.image(row['Image URL'], caption=row['Message'], use_column_width=True)
                    else:
                        st.write(f"Pas d'image pour le post avec ID {row['Post ID']}.")
                
                df.to_csv('facebook_posts.csv', index=False)
                st.success("Les données ont été sauvegardées dans 'facebook_posts.csv'")
            else:
                st.warning("Aucun post trouvé ou erreur lors de l'extraction des données. Vérifiez le jeton d'accès, l'ID de la page et les permissions.")
        else:
            st.warning("Le jeton d'accès ou l'ID de la page sont incorrects.")

if __name__ == "__main__":
    main()
