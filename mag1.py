import streamlit as st

# --- Dane początkowe (zostaną zresetowane przy każdej interakcji) ---
# Uwaga: Ta lista jest inicjalizowana przy każdym przeładowaniu strony/interakcji.
magazyn = ["Krzesło biurowe", "Myszka laserowa", "Klawiatura mechaniczna"]

# --- Funkcje Logiki Biznesowej ---

def dodaj_i_wyswietl(lista, nazwa_towaru):
    """Próbuje dodać towar i zwraca zaktualizowaną listę oraz status operacji."""
    if nazwa_towaru and nazwa_towaru not in lista:
        # Zwróć NOWĄ listę z dodanym elementem
        nowa_lista = lista + [nazwa_towaru]
        st.success(f"Dodano: **{nazwa_towaru}** (tymczasowo).")
        return nowa_lista
    elif nazwa_towaru in lista:
        st.warning(f"Towar **{nazwa_towaru}** już znajduje się na liście.")
        return lista
    else:
        st.error("Wprowadź nazwę towaru do dodania.")
        return lista

def usun_i_wyswietl(lista, nazwa_towaru):
    """Próbuje usunąć towar i zwraca zaktualizowaną listę oraz status operacji."""
    if nazwa_towaru in lista:
        # Utwórz NOWĄ listę bez usuniętego elementu
        nowa_lista = [item for item in lista if item != nazwa_towaru]
        st.success(f"Usunięto: **{nazwa_towaru}** (tymczasowo).")
        return nowa_lista
    else:
        st.error(f"Towar **{nazwa_towaru}** nie został znaleziony w magazynie.")
        return lista

# --- Główna Funkcja Interfejsu Użytkownika ---

def main_no_session_state():
    
    st.set_page_config(page_title="Magazyn Bez Session State", layout="wide")
    st.title("📦 System Magazynowy (Bez Session State)")
    st.subheader("⚠️ Stan nie jest zapamiętywany pomiędzy interakcjami")

    # Użycie globalnej listy zdefiniowanej na początku skryptu
    global magazyn
    
    st.markdown("---")
    st.header("Aktualny Stan Magazynu")
    
    # Wyświetlenie listy
    if magazyn:
        warehouse_list = "\n".join([f"* {item}" for item in magazyn])
        st.markdown(warehouse_list)
        st.info(f"Całkowita liczba pozycji: **{len(magazyn)}**")
    else:
        st.warning("Magazyn jest pusty!")

    st.markdown("---")
    
    col1, col2 = st.columns(2)

    with col1:
        st.header("➕ Dodaj Towar")
        new_item = st.text_input("Nazwa nowego towaru:")
        
        # Kluczowa zmiana: Operacja jest wykonywana i wynik jest ignorowany w następnej interakcji
        if st.button("Dodaj do Magazynu", type="primary"):
            # Ponieważ nie używamy session_state, zmiana nastąpi tylko raz w tej konkretnej rundzie
            # i zostanie utracona przy następnym kliknięciu.
            nowy_magazyn = dodaj_i_wyswietl(magazyn, new_item.strip())
            # Zauważ: Streamlit w następnym uruchomieniu skryptu (po kliknięciu) 
            # znowu wczyta globalną listę 'magazyn' z jej początkową wartością!
            
    with col2:
        st.header("➖ Usuń Towar")
        
        # Wybór towaru z listy
        if magazyn:
            item_to_remove = st.selectbox(
                "Wybierz towar do usunięcia:",
                options=magazyn
            )
            if st.button("Usuń z Magazynu", type="secondary"):
                # Ponownie, wynik tej operacji nie zostanie zapamiętany
                nowy_magazyn = usun_i_wyswietl(magazyn, item_to_remove)

# --- Uruchomienie Aplikacji ---
if __name__ == "__main__":
    main_no_session_state()
