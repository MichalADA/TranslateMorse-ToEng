#!/usr/bin/env python3
"""
Główny plik uruchamiający translator kodu Morse'a z interfejsem graficznym
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
import time
import platform

# Importuj moduły projektu bezpośrednio z lokalnych plików
from morse_utils import text_to_morse, morse_to_text
from morse_sound import play_morse_with_simple_beep

class MorseTranslatorApp:
    """Główna klasa aplikacji translatora kodu Morse'a z GUI"""
    
    def __init__(self, root):
        """
        Inicjalizuje aplikację z interfejsem graficznym
        
        Args:
            root (tk.Tk): Główne okno aplikacji
        """
        self.root = root
        self.root.title("Translator Kodu Morse'a")
        self.root.geometry("600x450")
        self.root.minsize(500, 400)
        
        # Tworzenie interfejsu
        self.create_widgets()
        
        # Status odtwarzacza dźwięku
        self.is_playing = False
        
    def create_widgets(self):
        """Tworzy wszystkie widgety dla interfejsu użytkownika"""
        # Górna ramka z tytułem
        frame_header = ttk.Frame(self.root, padding="10")
        frame_header.pack(fill=tk.X)
        
        ttk.Label(
            frame_header, 
            text="Translator Kodu Morse'a", 
            font=("Arial", 16, "bold")
        ).pack()
        
        # Ramka z wyborem trybu
        frame_mode = ttk.Frame(self.root, padding="10")
        frame_mode.pack(fill=tk.X)
        
        self.mode_var = tk.StringVar(value="text_to_morse")
        ttk.Radiobutton(
            frame_mode, 
            text="Tekst → Kod Morse'a", 
            variable=self.mode_var, 
            value="text_to_morse",
            command=self.update_mode
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(
            frame_mode, 
            text="Kod Morse'a → Tekst", 
            variable=self.mode_var, 
            value="morse_to_text",
            command=self.update_mode
        ).pack(side=tk.LEFT)
        
        # Ramka z obszarami tekstowymi
        frame_text = ttk.Frame(self.root, padding="10")
        frame_text.pack(fill=tk.BOTH, expand=True)
        
        # Lewa kolumna - wprowadzanie tekstu
        frame_input = ttk.LabelFrame(frame_text, text="Wprowadź tekst", padding="5")
        frame_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.input_text = scrolledtext.ScrolledText(frame_input, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Prawa kolumna - wyjście
        frame_output = ttk.LabelFrame(frame_text, text="Wynik", padding="5")
        frame_output.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(frame_output, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Dolna ramka z przyciskami
        frame_buttons = ttk.Frame(self.root, padding="10")
        frame_buttons.pack(fill=tk.X)
        
        ttk.Button(
            frame_buttons, 
            text="Tłumacz", 
            command=self.translate
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.play_button = ttk.Button(
            frame_buttons, 
            text="Odtwórz dźwięk", 
            command=self.play_sound
        )
        self.play_button.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            frame_buttons, 
            text="Wyczyść", 
            command=self.clear_fields
        ).pack(side=tk.LEFT)
        
        # Informacja o statusie
        self.status_var = tk.StringVar(value="Gotowy")
        ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        ).pack(side=tk.BOTTOM, fill=tk.X)
        
        # Ustawienie początkowego trybu
        self.update_mode()
    
    def update_mode(self):
        """Aktualizuje interfejs na podstawie wybranego trybu tłumaczenia"""
        mode = self.mode_var.get()
        
        if mode == "text_to_morse":
            self.input_text.config(state=tk.NORMAL)
            self.play_button.config(state=tk.NORMAL)
        else:
            self.input_text.config(state=tk.NORMAL)
            # Odtwarzanie dźwięku niedostępne dla tłumaczenia z kodu Morse'a
            self.play_button.config(state=tk.DISABLED)
    
    def translate(self):
        """Tłumaczy tekst na podstawie wybranego trybu"""
        input_content = self.input_text.get("1.0", tk.END).strip()
        
        if not input_content:
            messagebox.showinfo("Informacja", "Wprowadź tekst do tłumaczenia.")
            return
        
        mode = self.mode_var.get()
        
        try:
            if mode == "text_to_morse":
                result = text_to_morse(input_content)
            else:
                result = morse_to_text(input_content)
                
            # Wyczyść poprzedni wynik i wyświetl nowy
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            self.output_text.config(state=tk.DISABLED)
            
            self.status_var.set("Tłumaczenie zakończone.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas tłumaczenia: {str(e)}")
            self.status_var.set("Wystąpił błąd.")
    
    def play_sound(self):
        """Odtwarza kod Morse'a jako dźwięk"""
        if self.is_playing:
            self.status_var.set("Odtwarzanie już trwa.")
            return
        
        morse_code = self.output_text.get("1.0", tk.END).strip()
        
        if not morse_code:
            messagebox.showinfo("Informacja", "Najpierw przetłumacz tekst na kod Morse'a.")
            return
        
        try:
            self.is_playing = True
            self.play_button.config(state=tk.DISABLED)
            self.status_var.set("Odtwarzanie dźwięku...")
            self.root.update()
            
            # Odtwórz dźwięk w prosty sposób (bez zależności od numpy)
            play_morse_with_simple_beep(morse_code, self.status_callback)
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas odtwarzania dźwięku: {str(e)}")
            self.status_var.set("Wystąpił błąd odtwarzania.")
            self.is_playing = False
            self.play_button.config(state=tk.NORMAL)
    
    def status_callback(self, message):
        """Callback do aktualizacji statusu odtwarzania"""
        self.status_var.set(message)
        if message == "Odtwarzanie zakończone.":
            self.is_playing = False
            self.play_button.config(state=tk.NORMAL)
        self.root.update()
    
    def clear_fields(self):
        """Czyści pola tekstowe"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.status_var.set("Pola wyczyszczone.")

def main():
    """Funkcja główna uruchamiająca aplikację"""
    root = tk.Tk()
    app = MorseTranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    # Sprawdzenie, czy moduły są w bieżącym katalogu
    try:
        # Spróbuj uruchomić z normalną strukturą importów
        print("Uruchamianie translatora kodu Morse'a...")
        main()
    except ImportError as e:
        print(f"Błąd importu: {e}")
        print("Próbuję uruchomić w trybie samodzielnym...")
        
        # Spróbuj zaimportować lokalne moduły jeśli są w tym samym katalogu
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        
        try:
            # Spróbuj zaimportować ponownie
            from morse_utils import text_to_morse, morse_to_text
            from morse_sound import play_morse_with_simple_beep
            print("Udało się zaimportować moduły. Uruchamianie aplikacji...")
            main()
        except ImportError:
            print("Nie można zaimportować modułów. Uruchamianie trybu awaryjnego.")
            # Tutaj możesz dodać kod do uruchomienia uproszczonej wersji
            # lub wyświetlić instrukcję do uruchomienia bezposredni_start.py
            print("Zalecamy użycie pliku bezposredni_start.py, który zawiera wszystkie funkcje w jednym pliku.")