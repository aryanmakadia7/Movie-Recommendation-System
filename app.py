import tkinter as tk
from tkinter import ttk, messagebox
import pickle


# ============================================================
# LOAD MODEL FILES
# ============================================================

with open("movie_data.pkl", "rb") as file:
    movies = pickle.load(file)

with open("similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

with open("movie_indices.pkl", "rb") as file:
    movie_indices = pickle.load(file)


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Movie Recommendation System")

root.geometry("950x800")

root.minsize(800, 650)

root.configure(bg="#1e1e1e")


# ============================================================
# SCROLLABLE MAIN AREA
# ============================================================

main_canvas = tk.Canvas(
    root,
    bg="#1e1e1e",
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    root,
    orient="vertical",
    command=main_canvas.yview
)

main_canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

main_canvas.pack(
    side="left",
    fill="both",
    expand=True
)


# Frame inside canvas
main_frame = tk.Frame(
    main_canvas,
    bg="#1e1e1e"
)

canvas_window = main_canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)


# Update scroll region
def update_scroll_region(event=None):

    main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )


main_frame.bind(
    "<Configure>",
    update_scroll_region
)


# Make inner frame width match canvas
def resize_frame(event):

    main_canvas.itemconfig(
        canvas_window,
        width=event.width
    )


main_canvas.bind(
    "<Configure>",
    resize_frame
)


# Mouse-wheel scrolling
def mouse_wheel(event):

    main_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


main_canvas.bind_all(
    "<MouseWheel>",
    mouse_wheel
)


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    main_frame,
    text="🎬 Movie Recommendation System",
    font=("Arial", 28, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title.pack(
    pady=(30, 10)
)


# ============================================================
# DESCRIPTION
# ============================================================

description = tk.Label(
    main_frame,
    text="Discover movies similar to your favorite films",
    font=("Arial", 13),
    bg="#1e1e1e",
    fg="#cccccc"
)

description.pack(
    pady=(0, 25)
)


# ============================================================
# MOVIE SELECTION
# ============================================================

selection_frame = tk.Frame(
    main_frame,
    bg="#1e1e1e"
)

selection_frame.pack(
    fill="x",
    padx=40
)


movie_label = tk.Label(
    selection_frame,
    text="🎥 Select a Movie",
    font=("Arial", 14, "bold"),
    bg="#1e1e1e",
    fg="white"
)

movie_label.pack(
    pady=8
)


# Movie list
movie_list = sorted(
    movies["title"].dropna().unique()
)


movie_combo = ttk.Combobox(
    selection_frame,
    values=movie_list,
    width=55,
    font=("Arial", 12),
    state="normal"
)

movie_combo.pack(
    pady=8
)


# ============================================================
# MOVIE SEARCH
# ============================================================

def search_movies(event=None):

    typed_text = movie_combo.get().lower().strip()

    if typed_text == "":
        movie_combo["values"] = movie_list
        return

    filtered_movies = [
        movie
        for movie in movie_list
        if typed_text in movie.lower()
    ]

    movie_combo["values"] = filtered_movies


movie_combo.bind(
    "<KeyRelease>",
    search_movies
)


# ============================================================
# MOVIE INFORMATION
# ============================================================

info_label = tk.Label(
    main_frame,
    text="Selected Movie Information",
    font=("Arial", 16, "bold"),
    bg="#1e1e1e",
    fg="white"
)

info_label.pack(
    pady=(25, 8)
)


movie_info_frame = tk.Frame(
    main_frame,
    bg="#2b2b2b",
    bd=2,
    relief="groove"
)

movie_info_frame.pack(
    padx=40,
    pady=5,
    fill="x"
)


movie_info = tk.Label(
    movie_info_frame,
    text="Select a movie to see its information.",
    font=("Arial", 11),
    bg="#2b2b2b",
    fg="white",
    wraplength=820,
    justify="left",
    anchor="w"
)

movie_info.pack(
    fill="x",
    padx=20,
    pady=15
)


# ============================================================
# SHOW MOVIE INFORMATION
# ============================================================

def show_movie_info(event=None):

    selected_movie = movie_combo.get().strip()

    if not selected_movie:
        return

    movie_rows = movies[
        movies["title"].str.lower()
        == selected_movie.lower()
    ]

    if movie_rows.empty:
        return

    movie = movie_rows.iloc[0]

    title_text = movie["title"]

    rating = movie["vote_average"]

    release_date = movie["release_date"]

    overview = movie.get(
        "overview",
        ""
    )

    if pd_is_missing(overview) or not overview:
        overview = "No overview available."

    if pd_is_missing(release_date) or not release_date:
        release_date = "Not available"

    information = (
        f"🎬 {title_text}\n\n"
        f"⭐ Rating: {rating}/10\n"
        f"📅 Release Date: {release_date}\n\n"
        f"📝 Overview:\n{overview}"
    )

    movie_info.config(
        text=information
    )


def pd_is_missing(value):

    try:
        return value != value
    except:
        return False


movie_combo.bind(
    "<<ComboboxSelected>>",
    show_movie_info
)


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    main_frame,
    bg="#1e1e1e"
)

button_frame.pack(
    pady=20
)


# ============================================================
# RECOMMENDATION FUNCTION
# ============================================================

def recommend_movies():

    selected_movie = movie_combo.get().strip()

    if not selected_movie:

        messagebox.showwarning(
            "Warning",
            "Please select a movie."
        )

        return

    movie_name = selected_movie.lower()

    if movie_name not in movie_indices:

        messagebox.showerror(
            "Error",
            "Movie not found.\n\n"
            "Please select a movie from the search results."
        )

        return

    # Get movie index
    index = movie_indices[movie_name]

    # Get similarity scores
    similarity_scores = list(
        enumerate(similarity[index])
    )

    # Sort by similarity
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Clear previous results
    result_text.config(
        state="normal"
    )

    result_text.delete(
        "1.0",
        tk.END
    )

    result_text.insert(
        tk.END,
        f"🎬 Movies Similar to {selected_movie}\n\n",
        "heading"
    )

    # Display top 5
    for number, (i, score) in enumerate(
        similarity_scores[1:6],
        start=1
    ):

        movie = movies.iloc[i]

        title_text = movie["title"]

        rating = movie["vote_average"]

        release_date = movie["release_date"]

        result_text.insert(
            tk.END,
            f"{number}. {title_text}\n",
            "movie_title"
        )

        result_text.insert(
            tk.END,
            f"   ⭐ Rating: {rating}/10\n",
            "details"
        )

        result_text.insert(
            tk.END,
            f"   🎯 Similarity: {score * 100:.2f}%\n",
            "details"
        )

        if not pd_is_missing(release_date) and release_date:

            result_text.insert(
                tk.END,
                f"   📅 Release Date: {release_date}\n",
                "details"
            )

        result_text.insert(
            tk.END,
            "\n"
        )

    result_text.config(
        state="disabled"
    )


# ============================================================
# RECOMMEND BUTTON
# ============================================================

recommend_button = tk.Button(
    button_frame,
    text="🍿 Recommend Movies",
    font=("Arial", 12, "bold"),
    bg="#444444",
    fg="white",
    activebackground="#555555",
    activeforeground="white",
    padx=25,
    pady=10,
    cursor="hand2",
    command=recommend_movies
)

recommend_button.grid(
    row=0,
    column=0,
    padx=10
)


# ============================================================
# CLEAR FUNCTION
# ============================================================

def clear_results():

    result_text.config(
        state="normal"
    )

    result_text.delete(
        "1.0",
        tk.END
    )

    result_text.config(
        state="disabled"
    )

    movie_info.config(
        text="Select a movie to see its information."
    )


# ============================================================
# CLEAR BUTTON
# ============================================================

clear_button = tk.Button(
    button_frame,
    text="Clear",
    font=("Arial", 12, "bold"),
    bg="#444444",
    fg="white",
    activebackground="#555555",
    activeforeground="white",
    padx=25,
    pady=10,
    cursor="hand2",
    command=clear_results
)

clear_button.grid(
    row=0,
    column=1,
    padx=10
)


# ============================================================
# RESULTS TITLE
# ============================================================

results_label = tk.Label(
    main_frame,
    text="Recommended Movies",
    font=("Arial", 17, "bold"),
    bg="#1e1e1e",
    fg="white"
)

results_label.pack(
    pady=(15, 8)
)


# ============================================================
# RESULTS BOX
# ============================================================

result_frame = tk.Frame(
    main_frame,
    bg="#2b2b2b",
    bd=2,
    relief="groove"
)

result_frame.pack(
    padx=40,
    pady=5,
    fill="x"
)


result_text = tk.Text(
    result_frame,
    height=18,
    width=90,
    font=("Arial", 11),
    bg="#2b2b2b",
    fg="white",
    insertbackground="white",
    bd=0,
    padx=20,
    pady=15,
    wrap="word"
)

result_text.pack(
    fill="both",
    expand=True
)


# ============================================================
# TEXT FORMATTING
# ============================================================

result_text.tag_configure(
    "heading",
    font=("Arial", 15, "bold")
)

result_text.tag_configure(
    "movie_title",
    font=("Arial", 13, "bold")
)

result_text.tag_configure(
    "details",
    font=("Arial", 11)
)


result_text.config(
    state="disabled"
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    main_frame,
    text="Built with Python • Pandas • Scikit-learn • Tkinter",
    font=("Arial", 9),
    bg="#1e1e1e",
    fg="#888888"
)

footer.pack(
    pady=25
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()