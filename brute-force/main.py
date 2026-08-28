import hashlib
import time
from flask import Flask, request, render_template

app = Flask(__name__)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# Número máximo de tentativas
MAX_ATTEMPTS = 5

# Tempo de bloqueio em segundos
LOCK_TIME = 30

# Guarda as tentativas falhadas
failed_attempts = {}

# Passwords (SHA-256)
USER_DATABASE = {
    "admin1": "044f07d3e9f586bffda43c444322142ff313fc6f044c5b9ae74db00ab360f706",
    "admin2": "a1d8529ac580b2e643526d7fda61bd8e0aa759d64092ad7886129c8eef3cc898",
}


@app.route("/", methods=["GET", "POST"])
def login():

    message = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Verifica se o utilizador está bloqueado
        if username in failed_attempts:

            attempts, blocked_until = failed_attempts[username]

            # Se o tempo de bloqueio terminou, limpa o contador
            if time.time() >= blocked_until and blocked_until != 0:
                failed_attempts.pop(username)

            # Ainda está bloqueado
            elif time.time() < blocked_until:
                return (
                    "Zu viele Fehlversuche. Bitte in 30 Sekunden erneut versuchen.",
                    429,
                )

        # Login correto
        if USER_DATABASE.get(username) == hash_password(password):

            failed_attempts.pop(username, None)

            return (
                f"<h1>Herzlichen Glückwunsch! Zugriff für {username} erfolgreich gewährt.</h1>"
            )

        # Login incorreto
        attempts = failed_attempts.get(username, (0, 0))[0] + 1

        # Se atingir o limite, bloqueia imediatamente
        if attempts >= MAX_ATTEMPTS:

            failed_attempts[username] = (
                attempts,
                time.time() + LOCK_TIME,
            )

            return (
                "Zu viele Fehlversuche. Bitte in 30 Sekunden erneut versuchen.",
                429,
            )

        # Guarda o número de tentativas
        failed_attempts[username] = (
            attempts,
            0,
        )

        message = "Ungültige Anmeldedaten. Bitte versuchen Sie es erneut."

        return render_template("login.html", message=message), 401

    return render_template("login.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)