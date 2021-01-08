import logging
from time import perf_counter

# PTB imports
from telegram import ReplyKeyboardMarkup, Update, message
import telegram
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    conversationhandler,
    filters,
)
from telegram.ext.dispatcher import run_async
from telegram.ext.handler import Handler

# Utility Import
import uuid
from queue import Queue
import os
from dotenv import load_dotenv

load_dotenv()

from utils import *

_BASE_DIR = os.getcwd()
_BASE_DIR_FILE = os.path.join(_BASE_DIR, "files")

TOKEN_ = os.getenv("TOKEN")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

caption = "😁 Converted By @fileconverterallbot made by @chapimenge"

to_pdf_reply_keyboard = [
    [
        "image to PDF",
        "Word to PDF",
    ],
    ["PPT to PDF", "Excel To PDf"],
    ["Back", "Main Menu"],
]
from_pdf_reply_keyboard = [
    [
        "PDF to Images",
        "PDF to Word",
    ],
    ["PDF to PPT", "PDF to Excel"],
    ["Back", "Main Menu"],
]

first_choice_keyboard = [
    ["Goes Convert to PDF"],
    ["Goes Convert from PDF"],
]

to_pdf_markup = ReplyKeyboardMarkup(to_pdf_reply_keyboard, one_time_keyboard=True)

from_pdf_markup = ReplyKeyboardMarkup(from_pdf_reply_keyboard, one_time_keyboard=True)

choice_markup = ReplyKeyboardMarkup(first_choice_keyboard, one_time_keyboard=True)


CHOOSE, TO_PDF_MAIN, FROM_PDF_MAIN, STAROVER = range(13, 17)

TO_PDF, FROM_PDF = 11, 12

PDF_JPG, PDF_WORD, PDF_PPT, PDF_EXCEL, PDF_HTML = range(5)

JPG_PDF, WORD_PDF, PPT_PDF, EXCEL_PDF, HTML_PDF = range(5, 10)


def done(update, context):
    if "Files" in context.user_data and len(context.user_data["Files"]) != 0:
        del_user_files(context.user_data["Files"])
    if "SIZE" in context.user_data:
        context.user_data["SIZE"] = 0
        
    update.message.reply_text(
        "To start over send me /start\n"
        "Thank you for using My bot, if you have any comment contact me @chapimenge",
        reply_markup=telegram.ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


def start(update: Update, context: CallbackContext) -> int:
    # for i in update:
    #     print(i)
    # print(dir(update))
    # print("Startover")
    if "SIZE" in context.user_data:
        context.user_data["SIZE"] = 0
    if "Files" in context.user_data and len(context.user_data["Files"]) != 0:
        del_user_files(context.user_data["Files"])
    update.message.reply_text(
        "Hi! My name is File Convertor Bot. I will convert any files to and from PDF and other Formats. \n"
        "to see how to use the bot send /help\n"
        "File Must be less than 10MB , if you have more than 10 MB File please Contact @chapimenge",
        reply_markup=choice_markup,
    )
    context.user_data["Back"] = [
        start,
    ]

    # context.user_data['Back'] = CHOOSE

    return CHOOSE


def startover(update: Update, context: CallbackContext) -> int:
    if "Files" in context.user_data and len(context.user_data["Files"]) != 0:
        del_user_files(context.user_data["Files"])
    if "SIZE" in context.user_data:
        context.user_data["SIZE"] = 0
    update.message.reply_text(
        "Glad to see you are still here\n"
        "To see how to use the bot send /help\n"
        "File Must be less than 10MB , if you have more than 10 MB File please Contact @chapimenge",
        reply_markup=choice_markup,
    )
    if "Back" in context.user_data:
        context.user_data["Back"] = [
            startover,
        ]
    # context.user_data['Back'] = CHOOSE
    return CHOOSE


def to_pdf_convertor(update: Update, context: CallbackContext):

    update.message.reply_text(
        "Please Choose What Do you want to convert\n", reply_markup=to_pdf_markup
    )

    context.user_data["Back"].append(to_pdf_convertor)

    return TO_PDF_MAIN


def from_pdf_convertor(update: Update, context: CallbackContext):

    update.message.reply_text(
        "Please Choose What Do you want to convert\n", reply_markup=from_pdf_markup
    )
    context.user_data["Back"].append(from_pdf_convertor)

    return FROM_PDF_MAIN


def back(update: Update, context: CallbackContext):
    BACK_ = startover
    if "Files" in context.user_data and len(context.user_data["Files"]) != 0:
        del_user_files(context.user_data["Files"])

    if len(context.user_data["Back"]) > 1:
        context.user_data["Back"].pop()
        BACK_ = context.user_data["Back"][-1]
        return BACK_(update, context)
    else:
        return BACK_(update, context)


def jpg_to_pdf(update, context):
    done_keyboard = [["Done"]]
    done_keyboard_markup = ReplyKeyboardMarkup(done_keyboard, one_time_keyboard=True)
    # print(update.message)
    has_photo = len(update.message.photo) if update.message.photo else False
    bot = context.bot
    has_document = update.message.document or False
    if "Files" not in context.user_data:
        context.user_data["Files"] = []
    if "SIZE" is not context.user_data:
        context.user_data["SIZE"] = 0
    if has_photo:
        file_ = [
            [fil["file_size"], fil["file_id"], fil["file_unique_id"]]
            for fil in update.message.photo
        ]
        file_.sort()
        # print("Files")
        # print(file_)
        file_name = str(uuid.uuid1())
        context.user_data["SIZE"] += int( 0.5 + (file_[-1][0]/10**6) )
        if  context.user_data["SIZE"] > 50:
            update.message.reply_text("Total Fize is more than your limitation")
            return JPG_PDF
        print("FIles size" , file_[-1][0]) 
        download_file = bot.getFile(file_[-1][1])
        download_address = os.path.join(_BASE_DIR_FILE, file_name)
        # print("Download Address", download_address)
        download_file.download(custom_path=download_address)
        context.user_data["Files"].append(file_name)
        update.message.reply_text("I received", reply_markup=done_keyboard_markup)
    elif has_document:
        in_file = update.message.document
        file_ext = in_file["mime_type"].split("/")[-1]
        file_name = str(uuid.uuid1()) + "." + file_ext
        context.user_data["SIZE"] += int( 0.5 + (in_file['file_size']/10**6) )
        if  context.user_data["SIZE"] > 50:
            update.message.reply_text("Total Fize is more than your limitation")
            return JPG_PDF
        # print(f"File size = {in_file['file_size']}")
        
        file_ = [in_file["file_size"], in_file["file_id"], in_file["file_unique_id"]]
        download_address = os.path.join(_BASE_DIR_FILE, file_name)
        # print("Download Address", download_address)
        download_file = bot.getFile(update.message.document["file_id"])
        download_file.download(custom_path=download_address)
        context.user_data["Files"].append(file_name)
        update.message.reply_text("I received.", reply_markup=done_keyboard_markup)
    else:
        update.message.reply_text(
            "Please Send Me Photos you want to change to pdf. \nclick done when you finish!!!\n"
            "Make sure the File Size is less than 5MB.",
            reply_markup=done_keyboard_markup,
        )
    return JPG_PDF


def done_jpg_to_pdf(update, context):
    if "Files" not in context.user_data and len(context.user_data["Files"]) == 0:
        update.message.reply_text("You Didn't Upload any file. Please Try Again!")
        return startover(update, context)

    mid = update.message.reply_text(
        "Please wait it is converting your images to pdf ....."
    )
    # print(mid)
    if "SIZE" not in context.user_data:
       context.user_data["SIZE"] = 0
        
    if context.user_data["SIZE"] > 50:
        update.message.reply_text("Total Fize is more than your limitation")
        del_user_files(context.user_data["Files"])
        return startover(update, context)
    
    bot = context.bot
    chat_id = update.message.chat.id
    pdf_name = str(uuid.uuid1())
    pdf_address = os.path.join(_BASE_DIR_FILE, pdf_name + ".pdf")
    try:
        pdf = process_image_to_pdf(context.user_data["Files"], pdf_name) + ".pdf"
        pdf_address = os.path.join(_BASE_DIR_FILE, pdf)
        with open(pdf_address, "rb") as pdf_file:
            bot.edit_message_text(
                chat_id=chat_id, message_id=mid.message_id, text="Your file is Ready✅"
            )
            bot.send_document(
                chat_id=chat_id,
                document=pdf_file,
                filename="fileconverterallbot image-to-pdf.pdf",
                caption=caption,
            )
        os.remove(pdf_address)
        del_user_files(context.user_data["Files"])
        # print("Successfully Sent and Removed")
        return done(update, context)

    except Exception as e:
        print("*****This is Traceback*****")
        import traceback

        traceback.print_exc()
        print("*****This is Traceback*****")
        del_one_file(pdf_address)
        update.message.reply_text("Sorry 😔, Something is wrong! Please Try Again Later")
        return startover(update, context)


def word_to_pdf(update, context):
    has_doc = update.message.document or False
    bot = context.bot
    chat_id = update.message.chat.id
    if "SIZE" not in context.user_data:
           context.user_data["SIZE"] = 0
        
    if not has_doc:
        update.message.reply_text(
            "Please Send me Word file, or send me /cancel",
            reply_markup=telegram.ReplyKeyboardRemove(),
        )
        return WORD_PDF
    else:
        # print(has_doc)
        if "Files" not in context.user_data:
            context.user_data["Files"] = []
        file_name = str(uuid.uuid1())
        if has_doc.mime_type == "application/msword":
            file_name += ".doc"
        else:
            file_name += ".docx"
        download_address = os.path.join(_BASE_DIR_FILE, file_name)
        download_file = bot.getFile(has_doc["file_id"])
        
        context.user_data["SIZE"] += int( 0.5 + (has_doc['file_size']/10**6) )
        if  context.user_data["SIZE"] > 50:
            update.message.reply_text("Total Fize is more than your limitation")
            del_user_files(context.user_data["Files"])
            return WORD_PDF
        
        download_file.download(custom_path=download_address)
        context.user_data["Files"].append(file_name)
        ms = update.message.reply_text("Please wait , i am converting your file to pdf")
        convert_2_pdf = process_word_to_pdf(file_name)
        if convert_2_pdf == -1:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=ms.message_id,
                text="Sorry there is some problem couldn't convert your file 😔",
            )
        else:
            file_address = os.path.join(_BASE_DIR_FILE, convert_2_pdf)
            # print(file_address)
            with open(file_address, "rb") as pdf_file:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=ms.message_id,
                    text="Your file is Ready✅",
                )
                bot.send_document(
                    chat_id=chat_id,
                    document=pdf_file,
                    filename="Converted word to pdf.pdf",
                    caption=caption,
                )
            del_one_file(convert_2_pdf)
            del_user_files(context.user_data["Files"])
        return WORD_PDF


def ppt_to_pdf(update, context):
    has_doc = update.message.document or False
    bot = context.bot
    chat_id = update.message.chat.id
    if "SIZE" not in context.user_data:
        context.user_data['SIZE'] = 0
    if not has_doc:
        update.message.reply_text(
            "Please Send me Powerpoint file, or send me /cancel",
            reply_markup=telegram.ReplyKeyboardRemove(),
        )
        return PPT_PDF
    else:
        # print(has_doc)
        if "Files" not in context.user_data:
            context.user_data["Files"] = []
        file_name = str(uuid.uuid1())
        if has_doc.mime_type == "application/vnd.ms-powerpoint":
            file_name += ".ppt"
        else:
            file_name += ".pptx"
        context.user_data["SIZE"] += int( 0.5 + (has_doc['file_size']/10**6) )
        
        if  context.user_data["SIZE"] > 50:
            update.message.reply_text("Total Fize is more than your limitation")
            del_user_files(context.user_data["Files"])
            return PPT_PDF
        
        download_address = os.path.join(_BASE_DIR_FILE, file_name)
        download_file = bot.getFile(has_doc["file_id"])
        download_file.download(custom_path=download_address)
        context.user_data["Files"].append(file_name)
        ms = update.message.reply_text("Please wait , i am converting your file to pdf")
        convert_2_pdf = process_word_to_pdf(file_name)
        if convert_2_pdf == -1:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=ms.message_id,
                text="Sorry there is some problem couldn't convert your file 😔",
            )
        else:
            file_address = os.path.join(_BASE_DIR_FILE, convert_2_pdf)
            # print(file_address)
            with open(file_address, "rb") as pdf_file:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=ms.message_id,
                    text="Your file is Ready✅",
                )
                bot.send_document(
                    chat_id=chat_id,
                    document=pdf_file,
                    filename="Converted powerpoint to pdf.pdf",
                    caption=caption,
                )
            del_one_file(convert_2_pdf)
            del_user_files(context.user_data["Files"])
        return startover(update, context)


def excel_to_pdf(update, context):
    # print("excel excel")
    # print(update.message.document)
    has_doc = update.message.document or False

    bot = context.bot
    chat_id = update.message.chat.id
    if "SIZE" is not context.user_data:
        context.user_data['SIZE'] = 0

    if not has_doc:
        update.message.reply_text(
            "Please Send me Excel file, or send me /cancel",
            reply_markup=telegram.ReplyKeyboardRemove(),
        )
        return EXCEL_PDF
    else:
        # print(has_doc)
        if "Files" not in context.user_data:
            context.user_data["Files"] = []
        file_name = str(uuid.uuid1())

        file_name += ".xlsx"
        context.user_data["SIZE"] += int( 0.5 + (has_doc['file_size']/10**6) )
        
        if  context.user_data["SIZE"] > 50:
            update.message.reply_text("Total Fize is more than your limitation")
            del_user_files(context.user_data["Files"])
            return EXCEL_PDF
        
        download_address = os.path.join(_BASE_DIR_FILE, file_name)
        download_file = bot.getFile(has_doc["file_id"])
        download_file.download(custom_path=download_address)
        context.user_data["Files"].append(file_name)
        ms = update.message.reply_text("Please wait , i am converting your file to pdf")
        convert_2_pdf = process_word_to_pdf(file_name)
        if convert_2_pdf == -1:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=ms.message_id,
                text="Sorry there is some problem couldn't convert your file 😔",
            )
            return startover(update, context)
        else:
            file_address = os.path.join(_BASE_DIR_FILE, convert_2_pdf)
            # print(file_address)
            with open(file_address, "rb") as pdf_file:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=ms.message_id,
                    text="Your file is Ready✅\nNow I am Sending the file",
                )
                bot.send_document(
                    chat_id=chat_id,
                    document=pdf_file,
                    filename="Converted Excel to pdf.pdf",
                    caption=caption,
                )
            del_one_file(convert_2_pdf)
            del_user_files(context.user_data["Files"])
            return done(update, context)


def pdf_to_image(update, context):
    has_doc = update.message.document or False
    bot = context.bot
    chat_id = update.message.chat.id
    if "SIZE" not in context.user_data:
        context.user_data = 0
    if has_doc:
        ms = update.message.reply_text("Downloading the file")
        file_name = str(uuid.uuid1()) + ".pdf"
        file_address = os.path.join(_BASE_DIR_FILE, file_name)
        
        context.user_data["SIZE"] += int( 0.5 + (has_doc['file_size']/10**6) )
        
        if  context.user_data["SIZE"] > 50:
            update.message.reply_text("Total Fize is more than your limitation")
            del_user_files(context.user_data["Files"])
            return PDF_JPG
        
        download_file = bot.getFile(has_doc["file_id"])
        download_file.download(custom_path=file_address)
        context.user_data["Files"].append(file_name)
        ms = bot.edit_message_text(
            chat_id=chat_id,
            message_id=ms.message_id,
            text="Successfully Downloaded\nNow i am converting to images 🖼...",
        )
        output_folder = process_pdf_to_images(file_name)
        if output_folder == -1:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=ms.message_id,
                text="Sorry there is some problem couldn't convert your file 😔",
            )
            return startover(update, context)
        else:
            ms = bot.edit_message_text(
                chat_id=chat_id,
                message_id=ms.message_id,
                text="Your file is Ready✅\n Now I Am sending the images",
            )
            try:
                count = 1
                for image in os.listdir(output_folder):
                    photo_address = os.path.join(output_folder, image)
                    with open(photo_address, "rb") as file:
                        bot.send_document(
                            chat_id=chat_id,
                            document=file,
                            filename=f"image {count}.jpeg",
                            caption=caption,
                        )
                    count += 1
            except:
                print("*******traceback******")
                import traceback

                traceback.print_exc()
                print("*******traceback******")

                try:
                    del_one_file(file_address)
                    import shutil

                    shutil.rmtree(output_folder)
                except:
                    pass
                update.message.reply_text(
                    "Sorry there is some problem couldn't convert your file 😔"
                )
                return startover(update, context)
            try:
                del_one_file(file_address)
                import shutil

                shutil.rmtree(output_folder)
            except:
                pass
            return done(update, context)
    update.message.reply_text(
        "Please Send me the PDF file.\nPlease Make Sure the PDF File is not more than 25MB"
    )
    return PDF_JPG


def pdf_to_word(update, context):
    has_doc = update.message.document or False
    bot = context.bot
    chat_id = update.message.chat.id
    if has_doc:
        print(has_doc)
        if "Files" not in context.user_data:
            context.user_data["Files"] = []
        if "SIZE" not in context.user_data:
            context.user_data["SIZE"] = 0
            
        context.user_data["SIZE"] += int( 0.5 + (has_doc['file_size']/10**6) )
        
        if context.user_data["SIZE"] > 50:
            update.message.reply_text("Total Fize is more than your limitation")
            del_user_files(context.user_data["Files"])
            return PDF_WORD
        
        ms = update.message.reply_text("Downloading the file")
        file_name = str(uuid.uuid1()) + ".pdf"
        file_address = os.path.join(_BASE_DIR_FILE, file_name)
        download_file = bot.getFile(has_doc["file_id"])
        download_file.download(custom_path=file_address)
        context.user_data["Files"].append(file_name)
        ms = bot.edit_message_text(
            chat_id=chat_id,
            message_id=ms.message_id,
            text="Successfully Downloaded\nNow i am converting to word(document file) 🖼...",
        )
        
        import time

        t0 = perf_counter()
        converted_file = process_pdf_to_word(file_name)
        l0 = perf_counter()
        del_one_file(file_name)
        if converted_file == -1:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=ms.message_id,
                text="Sorry there is some problem couldn't convert your file 😔",
            )
            return startover(update, context)
        else:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=ms.message_id,
                text=f"Your file is Ready✅\nNow I am sending you file\nYour file is converted to docx file with {l0-t0:.2f} seconds",
            )
            with open(converted_file, "rb") as file:
                bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    filename=f"converted word.docx",
                    caption=caption,
                )
            del_one_file(converted_file)
            return done(update, context)        
        return PDF_WORD
    
    update.message.reply_text(
        "Please Send me the PDF file.\nPlease Make Sure the PDF File is not more than 25MB"
    )
    return PDF_WORD

def pdf_to_ppt(update, context):
    update.message.reply_text("This Feature is not yet Done.\nWe are working on it. Soon It will be available!")
    return startover(update, context)
def pdf_to_excel(update, context):
    update.message.reply_text("This Feature is not yet Done.\nWe are working on it. Soon It will be available!")
    return startover(update, context)

def main():
    updater = Updater(token=TOKEN_)
    dispatcher = updater.dispatcher

    conv_hander = ConversationHandler(
        allow_reentry=True,
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
                MessageHandler(
                    Filters.all,
                    startover,
                ),
            ],
            TO_PDF_MAIN: [
                MessageHandler(
                    Filters.regex(
                        "^(image to PDF)$",
                    ),
                    jpg_to_pdf,
                    # run_async=True
                ),
                MessageHandler(
                    Filters.regex(
                        "^(Word to PDF)$",
                    ),
                    word_to_pdf,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(PPT to PDF)$",
                    ),
                    ppt_to_pdf,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(Excel To PDf)$",
                    ),
                    excel_to_pdf,
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
                    startover,
                ),
            ],
            FROM_PDF_MAIN: [
                MessageHandler(
                    Filters.regex(
                        "^(PDF to Images)$",
                    ),
                    pdf_to_image,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(PDF to Word)$",
                    ),
                    pdf_to_word,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(PDF to PPT)$",
                    ),
                    pdf_to_ppt,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(PDF to Excel)$",
                    ),
                    pdf_to_excel,
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
                    startover,
                ),
            ],
            JPG_PDF: [
                MessageHandler(
                    Filters.photo | Filters.document.category("image"), jpg_to_pdf
                ),
                MessageHandler(Filters.regex("^(Done)$"), done_jpg_to_pdf),
            ],
            WORD_PDF: [
                MessageHandler(
                    Filters.document.doc | Filters.document.docx, word_to_pdf
                )
            ],
            PPT_PDF: [
                MessageHandler(
                    Filters.document.file_extension("ppt")
                    | Filters.document.file_extension("pptx"),
                    ppt_to_pdf,
                ),
            ],
            EXCEL_PDF: [
                MessageHandler(
                    Filters.document.file_extension("xlsx")
                    | Filters.document.file_extension(".xlsm")
                    | Filters.document.file_extension("xlsb")
                    | Filters.document.file_extension("xltx")
                    | Filters.document.file_extension("xltm"),
                    excel_to_pdf,
                )
            ],
            PDF_JPG: [
                MessageHandler(Filters.document.pdf, pdf_to_image),
            ],
            PDF_WORD: [
                MessageHandler(Filters.document.pdf, pdf_to_word),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.regex("^(start|done|cancel)$"), startover),
            CommandHandler("start", startover),
            CommandHandler("cancel", startover),
        ],
    )

    dispatcher.add_handler(conv_hander)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()