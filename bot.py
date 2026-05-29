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
# BOT TOKEN
# =========================

BOT_TOKEN = "8666526093:AAGSOaJuIof6JMlhGgOpd_hjyobcqRy2FB4"

# =========================
# PASSCODE
# =========================

PASSCODE = "753159"

# =========================
# ALLOWED TELEGRAM USERS
# =========================

ALLOWED_USERS = [
    7958120091,
    5463947091,
    1234567890,
    9876543210
]

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
# FORGOT PASSWORD SECRET
# =========================

FORGOT_SECRET = "CLCMFLWTNL4GZV5IODEUYRY6A6YUI7V5"

forgot_totp = pyotp.TOTP(
    FORGOT_SECRET,
    digits=6,
    interval=30,
    digest=hashlib.sha1
)

# =========================
# VERIFIED USERS STORAGE
# =========================

verified_users = {}

# =========================
# MESSAGE HANDLER
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        if update.message is None:
            return

        user_id = update.effective_user.id

        text = update.message.text.strip().lower()

        print("USER ID:", user_id)
        print("MESSAGE:", text)

        # =========================
        # BLOCK UNKNOWN USERS
        # =========================

        if user_id not in ALLOWED_USERS:

            print("BLOCKED USER:", user_id)

            await update.message.reply_text(
                "Access Denied ❌"
            )

            return

        # =========================
        # PASSCODE VERIFICATION
        # =========================

        if user_id not in verified_users:

            if text == PASSCODE:

                verified_users[user_id] = True

                await update.message.reply_text(
                    "PassCode Verified ✅\n\nAvailable Commands:\n\nanna otp for recharge\nanna admin otp\nanna forgot password otp\nlogout"
                )

            else:

                await update.message.reply_text(
                    "Enter PassCode First"
                )

            return

        # =========================
        # USER OTP
        # =========================

        if text == "anna otp for recharge":

            otp = user_totp.now()

            print("USER OTP:", otp)

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
        # FORGOT PASSWORD OTP
        # =========================

        elif text == "anna forgot password otp":

            forgot_otp = forgot_totp.now()

            print("FORGOT OTP:", forgot_otp)

            await update.message.reply_text(
                f"Forgot Password OTP: {forgot_otp}"
            )

        # =========================
        # LOGOUT
        # =========================

        elif text == "logout":

            verified_users.pop(user_id, None)

            await update.message.reply_text(
                "Logged Out ❌"
            )

        # =========================
        # HELP
        # =========================

        else:

            await update.message.reply_text(
                "Available Commands:\n\nanna otp for recharge\nanna admin otp\nanna forgot password otp\nlogout"
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
