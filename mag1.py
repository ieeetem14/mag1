import streamlit as st

# --- Dane początkowe (zostaną zresetowane przy każdej interakcji) ---
# Magazyn teraz przechowuje listę słowników z ilością (liczbą sztuk)
magazyn = [
    {"nazwa": "Krzesło biurowe", "ilosc": 3},
    {"nazwa": "Myszka laserowa", "ilosc": 1},
    {"nazwa": "Klawiatura mechaniczna", "ilosc": 2}
]

# --- Funkcje Logiki Biznesowej ---

def znajdz_towar_index(lista, nazwa):
    """Zwraca indeks towaru na liście lub -1, jeśli go nie ma."""
    for i, item in enumerate(lista):
        if item["nazwa"] == nazwa:
            return i
    return -1

def dodaj_lub_zwieksz(lista, nazwa_towaru):
    """Zwiększa ilość towaru lub dodaje go, jeśli nie istnieje. Zwraca NOWY stan listy."""
    if not nazwa_towaru:
        st.error("Wprowadź nazwę towaru.")
        return lista

    # Tworzymy kopię listy, aby operować na nowym stanie
    nowa_lista = [item.copy() for item in lista]
    index = znajdz_towar_index(nowa_lista, nazwa_towaru)

    if index != -1:
        # Towar znaleziony - zwiększamy ilość
        nowa_lista[index]["ilosc"] += 1
        st.success(f"Zwiększono ilość towaru **{nazwa_towaru}** do **{nowa_lista[index]['ilosc']}** sztuk (Operacja tymczasowa).")
    else:
        # Towar nie znaleziony - dodajemy nowy z ilością 1
        nowa_lista.append({"nazwa": nazwa_towaru, "ilosc": 1})
        st.success(f"Dodano nowy towar **{nazwa_towaru}** w ilości 1 sztuki (Operacja tymczasowa).")
        
    return nowa_lista

def zmniejsz_lub_usun(lista, nazwa_towaru):
    """Zmniejsza ilość towaru lub usuwa go, jeśli ilość spadnie do zera. Zwraca NOWY stan listy."""
    nowa_lista = [item.copy() for item in lista]
    index = znajdz_towar_index(nowa_lista, nazwa_towaru)

    if index != -1:
        ilosc = nowa_lista[index]["ilosc"]
        
        if ilosc > 1:
            # Zmniejszamy ilość
            nowa_lista[index]["ilosc"] -= 1
            st.success(f"Zmniejszono ilość towaru **{nazwa_towaru}** do **{nowa_lista[index]['ilosc']}** sztuk (Operacja tymczasowa).")
        else:
            # Usuwamy towar (ilosc == 1)
            del nowa_lista[index]
            st.success(f"Usunięto ostatnią sztukę towaru **{nazwa_towaru}** z magazynu (Operacja tymczasowa).")
    else:
        st.error(f"Towar **{nazwa_towaru}** nie został znaleziony w magazynie.")
        
    return nowa_lista

# --- Główna Funkcja Interfejsu Użytkownika ---

def main_app():
    
    st.set_page_config(page_title="Prosty System Magazynowy", layout="wide")
    st.title("📦 Prosty System Magazynowy")
    st.subheader("Aplikacja Streamlit") 

    # Użycie globalnej listy zdefiniowanej na początku skryptu
    global magazyn
    aktualny_magazyn = magazyn
    
    st.markdown("---")
    st.header("Aktualny Stan Magazynu")
    
    # Wyświetlenie listy z ilością
    if aktualny_magazyn:
        # Generowanie formatowania listy: Nazwa towaru: X sztuk
        warehouse_display = "\n".join([f"* **{item['nazwa']}**: {item['ilosc']} sztuk" for item in aktualny_magazyn])
        st.markdown(warehouse_display)
        
        total_unique_items = len(aktualny_magazyn)
        total_count = sum(item['ilosc'] for item in aktualny_magazyn)
        
        st.info(f"Liczba unikalnych pozycji: **{total_unique_items}** | Łączna liczba wszystkich sztuk: **{total_count}**")
    else:
        st.warning("Magazyn jest pusty!")

    st.markdown("---")
    
    col1, col2 = st.columns(2)

    with col1:
        st.header("➕ Dodaj / Zwiększ Ilość")
        new_item = st.text_input("Nazwa towaru do dodania / zwiększenia ilości:", key="add_input")
        
        if st.button("Dodaj / Zwiększ Ilość", type="primary"):
            nowy_stan = dodaj_lub_zwieksz(aktualny_magazyn, new_item.strip())
            
            # Nadpisanie globalnej listy i wymuszenie restartu, aby wyświetlić zmianę.
            # UWAGA: Stan zostanie utracony przy następnej interakcji!
            global magazyn
            magazyn = nowy_stan
            st.rerun() 
            
    with col2:
        st.header("➖ Zmniejsz / Usuń Towar")
        
        item_names = [item['nazwa'] for item in aktualny_magazyn if item['ilosc'] > 0]
        
        if item_names:
            item_to_remove = st.selectbox(
                "Wybierz towar do zmniejszenia/usunięcia:",
                options=item_names,
                key="remove_select"
            )
            if st.button("Zmniejsz Ilość / Usuń Towar", type="secondary"):
                nowy_stan = zmniejsz_lub_usun(aktualny_magazyn, item_to_remove)
                
                # Nadpisanie globalnej listy i wymuszenie restartu.
                global magazyn
                magazyn = nowy_stan
                st.rerun()
        else:
            st.info("Brak towarów w magazynie.")

# --- Uruchomienie Aplikacji ---
if __name__ == "__main__":
    main_app()
