import hashlib
import pyotp
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)

# =========================
# BOT CONFIG
# =========================

BOT_TOKEN = "8666526093:AAGSOaJuIof6JMlhGgOpd_hjyobcqRy2FB4"

# =========================
# USER OTP SECRET
# =========================

USER_SECRET = "RAZJCMDXT2OJVJVQH5XIGHUM4DJYASUH"

user_totp = pyotp.TOTP(
    USER_SECRET,
    digits=8,
    interval=30,
    digest=hashlib.sha1
)

# =========================
# ADMIN OTP SECRET
# =========================

ADMIN_SECRET = "DRVHDGKL27FIIKRKIWD4Z3N2R7ARMEJS"

admin_totp = pyotp.TOTP(
    ADMIN_SECRET,
    digits=6,
    interval=30,
    digest=hashlib.sha1
)

# =========================
# Master Forgot Password
# =========================

FORGOT_SECRET = "CLCMFLWTNL4GZV5IODEUYRY6A6YUI7V5"

FORGOT_totp = pyotp.TOTP(
    FORGOT_SECRET,
    digits=6,
    interval=30,
    digest=hashlib.sha1
)

# =========================
# MESSAGE HANDLER
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        if update.message is None:
            return

        text = update.message.text.lower().strip()

        print("MESSAGE:", text)

        # =========================
        # USER OTP
        # =========================

        if text == "anna otp for recharge":

            otp = user_totp.now()

            print("Current OTP:", otp)

            await update.message.reply_text(
                f"User OTP: {otp}"
            )

        # =========================
        # ADMIN OTP
        # =========================

        elif text == "anna admin otp":

            admin_otp = admin_totp.now()

            print("ADMIN OTP:", admin_otp)

            await update.message.reply_text(
                f"Admin OTP: {admin_otp}"
            )

        # =========================
        # Master Forgot Password OTP
        # =========================

        elif text == "anna forgot password otp":

            FORGOT_otp = FORGOT_totp.now()

            print("Master Forgot Password OTP OTP:", FORGOT_otp)

            await update.message.reply_text(
                f"Admin OTP: {FORGOT_otp}"
            )

        # =========================
        # HELP MESSAGE
        # =========================

        else:

            await update.message.reply_text(
                "Send: Wait"
            )

    except Exception as e:

        print("ERROR:", e)

# =========================
# MAIN
# =========================

def main():

    print("BOT STARTING...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("BOT RUNNING...")

    app.run_polling()

# =========================
# START
# =========================

if __name__ == "__main__":

    main()