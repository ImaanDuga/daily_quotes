import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# Use DATABASE_URL from environment (Railway injects this automatically)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///quotes.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- Model ---
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Quote {self.id} - {self.author}>"

# --- Routes ---

@app.route("/")
def index():
    # Pick quote of the day based on date ordinal
    quotes = Quote.query.all()
    if not quotes:
        quote = {"text": "No quotes yet. Add some!", "author": "System"}
    else:
        today_index = datetime.now().toordinal() % len(quotes)
        q = quotes[today_index]
        quote = {"text": q.text, "author": q.author}
    today = datetime.now().strftime("%B %d, %Y — %I:%M %p")
    return render_template("index.html", quote=quote, today=today)

@app.route("/quotes")
def list_quotes():
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    return render_template("quotes.html", quotes=quotes)

@app.route("/quotes/add", methods=["GET", "POST"])
def add_quote():
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        author = request.form.get("author", "").strip()
        if not text or not author:
            flash("Both fields are required.", "error")
        else:
            new_quote = Quote(text=text, author=author)
            db.session.add(new_quote)
            db.session.commit()
            flash("Quote added successfully!", "success")
            return redirect(url_for("list_quotes"))
    return render_template("add_quote.html")

@app.route("/quotes/edit/<int:quote_id>", methods=["GET", "POST"])
def edit_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        author = request.form.get("author", "").strip()
        if not text or not author:
            flash("Both fields are required.", "error")
        else:
            quote.text = text
            quote.author = author
            db.session.commit()
            flash("Quote updated.", "success")
            return redirect(url_for("list_quotes"))
    return render_template("edit_quote.html", quote=quote)

@app.route("/quotes/delete/<int:quote_id>", methods=["POST"])
def delete_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    flash("Quote deleted.", "success")
    return redirect(url_for("list_quotes"))

@app.route("/health")
def health():
    return {"status": "ok"}

# Seed data
DEFAULT_QUOTES = [
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"text": "In the middle of every difficulty lies opportunity.", "author": "Albert Einstein"},
    {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
    {"text": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
    {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
    {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill"},
    {"text": "You miss 100% of the shots you don't take.", "author": "Wayne Gretzky"},
    {"text": "Whether you think you can or you think you can't, you're right.", "author": "Henry Ford"},
    {"text": "The best time to plant a tree was 20 years ago. The second best time is now.", "author": "Chinese Proverb"},
    {"text": "An unexamined life is not worth living.", "author": "Socrates"},
]

# Create tables and seed on startup
with app.app_context():
    db.create_all()
    if Quote.query.count() == 0:
        for q in DEFAULT_QUOTES:
            db.session.add(Quote(text=q["text"], author=q["author"]))
        db.session.commit()
        print("Database seeded with default quotes.")

if __name__ == "__main__":
    app.run(debug=True)
