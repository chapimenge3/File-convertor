import logging
import queue
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    conversationhandler,
)

from queue import Queue


import os
from dotenv import load_dotenv

load_dotenv()


TOKEN_ = os.getenv("TOKEN")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

to_pdf_reply_keyboard = [
    [
        "JPG to PDF",
        "Word to PDf",
    ],
    ["PPT to PDF", "Excel To PDf"],
    ["Back", "Main Menu"],
]
from_pdf_reply_keyboard = [
    [
        "PDF to JPG",
        "PDF to Word",
    ],
    ["PDF to PPT", " PDF to Excel"],
    ["Back", "Main Menu"],
]

first_choice_keyboard = [
    ["Goes Convert to PDF"],
    ["Goes Convert from PDF"],
]

to_pdf_markup = ReplyKeyboardMarkup(to_pdf_reply_keyboard, one_time_keyboard=True)

from_pdf_markup = ReplyKeyboardMarkup(from_pdf_reply_keyboard, one_time_keyboard=True)

choice_markup = ReplyKeyboardMarkup(first_choice_keyboard, one_time_keyboard=True)


CHOOSE, TO_PDF_MAIN, FROM_PDF_MAIN = 13, 14, 15

TO_PDF, FROM_PDF = 11, 12

PDF_JPG, PDF_WORD, PDF_PPT, PDF_EXCEL, PDF_HTML = range(5)

JPG_PDF, WORD_PDF, PPT_PDF, EXCEL_PDF, HTML_PDF = range(5, 10)


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Hi! My name is Doctor File Convertor Bot. I will convert any files to and from PDF and other Formats. \n"
        "to see how to use the bot send /help\n"
        "File Must be less than 10MB , if you have more than 10 MB File please Contact @chapimenge",
        reply_markup=choice_markup,
    )
    context.user_data['Back'] = CHOOSE
    return CHOOSE


def to_pdf_convertor(update: Update, context: CallbackContext):

    update.message.reply_text(
        "Please Choose What Do you want to convert\n", reply_markup=to_pdf_markup
    )
    
    context.user_data['Back'] = TO_PDF_MAIN
    
    return TO_PDF_MAIN


def from_pdf_convertor(update: Update, context: CallbackContext):

    update.message.reply_text(
        "Please Choose What Do you want to convert\n", reply_markup=to_pdf_markup
    )
    context.user_data['Back'].put(FROM_PDF_MAIN)
    
    return FROM_PDF_MAIN

def back(update: Update, context: CallbackContext):
    
    
    BACK_ = context.user_data['Back']
        
    # print(BACK_)
    return BACK_ if BACK_ else CHOOSE 


def main():
    updater = Updater(token=TOKEN_)
    dispatcher = updater.dispatcher

    conv_hander = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE: [
                MessageHandler(
                    Filters.regex(
                        "^(Goes Convert to PDF)$",
                    ),
                    to_pdf_convertor,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(Goes Convert from PDF)$",
                    ),
                    from_pdf_convertor,
                ),
            ],
            TO_PDF_MAIN: [
                MessageHandler(
                    Filters.regex(
                        "^(JPG to PDF)$",
                    ),
                    from_pdf_convertor,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(WORD to PDF)$",
                    ),
                    from_pdf_convertor,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(PPT to PDF)$",
                    ),
                    from_pdf_convertor,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(Excel To PDf)$",
                    ),
                    from_pdf_convertor,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(Back)$",
                    ),
                    back,
                ),
                 MessageHandler(
                    Filters.regex(
                        "^(Main Menu)$",
                    ),
                    from_pdf_convertor,
                ),
            ],
            FROM_PDF_MAIN: [
                MessageHandler(
                    Filters.regex(
                        "^(Goes Convert from PDF)$",
                    ),
                    from_pdf_convertor,
                ),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.regex("^(start|done|cancel)$"), start),
            CommandHandler("start", start),
            CommandHandler("cancel", start),
        ],
    )

    dispatcher.add_handler(conv_hander)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()