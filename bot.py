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
# TEMP USER REQUEST STORAGE
# =========================

pending_requests = {}

# =========================
# MESSAGE HANDLER
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        if update.message is None:
            return

        user_id = update.effective_user.id

        text = update.message.text.strip().lower()

        print("USER:", user_id)
        print("MESSAGE:", text)

        # =========================
        # BLOCK UNKNOWN USERS
        # =========================

        if user_id not in ALLOWED_USERS:

            await update.message.reply_text(
                "Access Denied ❌"
            )

            return

        # =========================
        # CHECK PASSCODE
        # =========================

        if user_id in pending_requests:

            # User entered passcode
            if text == PASSCODE:

                request_type = pending_requests[user_id]

                # USER OTP
                if request_type == "user_otp":

                    otp = user_totp.now()

                    await update.message.reply_text(
                        f"User OTP: {otp}"
                    )

                # ADMIN OTP
                elif request_type == "admin_otp":

                    otp = admin_totp.now()

                    await update.message.reply_text(
                        f"Admin OTP: {otp}"
                    )

                # FORGOT PASSWORD OTP
                elif request_type == "forgot_otp":

                    otp = forgot_totp.now()

                    await update.message.reply_text(
                        f"Forgot Password OTP: {otp}"
                    )

                # Remove request after use
                pending_requests.pop(user_id)

            else:

                await update.message.reply_text(
                    "Wrong PassCode ❌"
                )

            return

        # =========================
        # ASK PASSCODE FOR EACH COMMAND
        # =========================

        if text == "anna otp for recharge":

            pending_requests[user_id] = "user_otp"

            await update.message.reply_text(
                "Enter PassCode For User OTP"
            )

        elif text == "anna admin otp":

            pending_requests[user_id] = "admin_otp"

            await update.message.reply_text(
                "Enter PassCode For Admin OTP"
            )

        elif text == "anna forgot password otp":

            pending_requests[user_id] = "forgot_otp"

            await update.message.reply_text(
                "Enter PassCode For Forgot Password OTP"
            )

        else:

            await update.message.reply_text(
                "Available Commands:\n\nanna otp for recharge\nanna admin otp\nanna forgot password otp"
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
