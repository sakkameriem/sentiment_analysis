import re
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['']

keywords = {

    "Celebration/Event": ["Siège social", "salon international", "stand", "غابة", "حلقة", "talkshow", "remercie",
                          "بكالوريا", "أمي", "Coming", "Ifm", "Radio Ifm", "هدية", "مسابقة", "مولد", "شهداء", "مدرسية",
                          "رمضان", "كريم", "القرعة", "🇹🇳", "مرأة", "القدوة", "وفاة", "تحيا", "مفاجأة", "يتمنالكم",
                          "شريف", "كادوات", "بأحر التعازي", "مربوحة", "match", "الفرحة", "مساهمتكم", "بسبب", "مستقلة",
                          "خير", "عيد", "مباركة", "شكرا", "كل عام", "بخير", "مبروك", "حظ", "إن شاء الله بالنجاح", "jeu",
                          "concours", "شارك", "شاركوا", "ربح", "طلع", "طلّع"],

    "New branch opening": ["فرع", "افتتاح", "فروع"],

    "Auto loan": ["Hyundai", "opel", "سيّارة", "شاحنات", "سيارات", "voiture", "auto", "véhicule", "كرهبة", "سيارة",
                  "كميون", "مستحق", "Berlingo", "Citroën", "mahindra", "ford"],

    "Personal loan": ["نفقات", "Istithmar", "Robot", "médical", "matériel", "soldes", "Black Friday", "صيف", "سافر",
                      "رحلات", "gamer", "ordinateur", "تليفون", "watch", "Galaxy", "أثاث", "meuble", "hôtel", "piscine",
                      "تفرهيدة", "روسيا", "المعدات", "مشتريات", "معدات", "العرس", "مصروف", "shopping", "صحيّة", "السفر",
                      "voyage", "Samsung", "lave vaisselle", "machine", "Télé", "smartphone", "refrigerateur",
                      "cuisiniere", "PC", "TV", "عمرة", "رحلة", "projet", "مشروع", "مشروعك", ],

    "Home loan": ["Tamouil Menzel", "البني", "طبية", "سفر", "حج", "الدّار", "bien", "immobilier", "maison",
                  "appartement", "عقار", "بيت", "شقة", "سكني", "منزل", "تحسينات", "بناءات", "تحسين", "بناء", "مكتب",
                  "محل", "تجاري", "عقارات", "مؤسسات", "دار", "دارك", "أرض"],

    "Student loan": ["مستقبلك", "دراسة", "قراية", "دراسات", "الجامعات", "جامعة خاصّة", "faculté", "étudie", "études",
                     "étude", "الباك", "الجامعة", "يقرى", "تقرى"],

    "Money transfer/Online banking": ["Hisseb Racid", "الخارج", "الإلكترونية", "الأنترنت ", "الأنترنات", "à distance",
                                      "الانترنات", "الالكتروني", "موزع آلي", "مو", "بطاقات", "بطاقة", "carte",
                                      "MasterCard", "البطاقة التكنولوجية", "paiement sans contact", "تواصل",
                                      "l’étranger", "العملة", "tawassol", "application", "technologique",
                                      "carte technologique", "ما تتنقل", "عن بعد", "TPE", "en ligne",
                                      "مواطينينا بالخارج", "devise", "تبدلو", "تحويل الأموال", "western union", "ria",
                                      "moneygram", "حوالة"],

    "Saving": ["خزنة", "Tawfir", "الادّخار", "توفير"]

}


def classify_post(caption):
    keyword_count = {
        "Celebration/Event": 0,
        "New branch opening": 0,
        "Auto loan": 0,
        "Personal loan": 0,
        "Home loan": 0,
        "Student loan": 0,
        "Money transfer/Online banking": 0,
        "Saving": 0,
        "Other": 0
    }

    for key, words in keywords.items():
        for word in words:
            if bool(re.search(word, caption, re.IGNORECASE)):
                keyword_count[key] += 1

    max_count = 0
    category = None
    for key, count in keyword_count.items():
        if count > max_count:
            max_count = count
            category = key
    if max_count == 0:
        category = "Other"

    return category



posts = collection.find({})

for post in posts:
    post_id = post['_id']
    caption = post['postTitle']
    category = classify_post(caption)
    collection.update_one({'_id': post_id}, {'$set': {'Banking product': category}})

print("Classification completed and updated in MongoDB")
