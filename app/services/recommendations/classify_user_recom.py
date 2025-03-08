def classify_user_profile(answers):

    categories = { 
        "mental_health": False,  # מצב נפשי כללי
        "anxiety": False,  # חרדה
        "depression": False,  # דיכאון
        "loneliness": False,  # בדידות
        "sleep_issues": False,  # קשיי שינה
        "trauma": False,  # טראומה
        "self_confidence": False,  # ביטחון עצמי
        "emotional_regulation": False,  # ויסות רגשי
        "social_support": False,  # תמיכה חברתית
        "motivation": False  # מוטיבציה כללית
    }

    category_mapping = {
        "question_7": ("mental_health",),  # מה הוביל אותך להירשם לאפליקציה?
        "question_9": ("mental_health", "anxiety"),  # האם חווה חרדה/לחץ?
        "question_10": ("mental_health", "motivation"),  # האם הרגשת הנאה?
        "question_11": ("mental_health", "depression"),  # חווית דיכאון?
        "question_12": ("sleep_issues",),  # קשיי שינה
        "question_13": ("mental_health",),  # מרגיש עייף/מוטרד?
        "question_14": ("depression",),  # מרגיש רע עם עצמך?
        "question_15": ("mental_health",),  # הכל מאמץ עבורך?
        "question_16": ("anxiety",),  # חרדה מפני אסון עתידי?
        "question_17": ("motivation",),  # איבדת עניין?
        "question_18": ("loneliness", "social_support"),  # ריחוק מאנשים?
        "question_19": ("emotional_regulation",),  # קושי לחוות רגשות חיוביים?
        "question_20": ("mental_health", "emotional_regulation"),  # לקחת סיכון עצמי?
        "question_21": ("mental_health",),  # קושי להתרכז?
        "question_22": ("mental_health", "trauma"),  # אילו חוויות קשה לך להתמודד איתן?
        "question_23": ("emotional_regulation", "social_support"),  # איך את/ה מתמודד/ת עם מצבים קשים?
        "question_24": ("social_support",),  # איפה אתה מרגיש בנוח לשתף?
        "question_25": ("self_confidence",),  # כמה טוב אתה מרגיש עם עצמך?
        "question_26": ("social_support",),  # פתיחות לשיתוף פעולה עם אחרים?
        "question_27": ("social_support",),  # איזה סוג חיבור מתאים לך?
        "question_29": ("sleep_issues",),  # איך היית מגדיר את הרגלי השינה שלך?
        "question_30": ("mental_health", "social_support"),  # אילו כלים יכולים לעזור לך?
        "question_31": ("mental_health", "motivation"),  # דירוג מצב כללי
        "question_32": ("emotional_regulation",),  # שליטה ברגשות
        "question_33": ("social_support",),  # קרבה לקשרים חברתיים
        "question_35": ("trauma",),  # האם חווית אירוע טראומטי?
        "question_36": ("trauma",),  # זיכרונות טראומטיים חוזרים?
        "question_37": ("trauma",),  # תחושת חזרה על החוויה הטראומטית?
        "question_38": ("trauma",),  # תחושת מצוקה בעקבות זיכרון טראומטי?
        "question_39": ("trauma",),  # הימנעות ממחשבות על הטראומה?
        "question_40": ("trauma",),  # הימנעות מאנשים שמזכירים את הטראומה?
        "question_41": ("trauma",),  # חוסר זיכרון של חלקים מהחוויה?
        "question_42": ("trauma",),  # תחושת אשמה על האירוע?
    }

    trigger_values = {
        "כן": True,
        "יחסית הרבה": True,
        "כמעט כל יום": True,
        "פעמים מעטות": False, 
        "בכלל לא": False
    }

    for question, categories_list in category_mapping.items():
        if question in answers and answers[question] in trigger_values:
            for category in categories_list:
                categories[category] = trigger_values[answers[question]]

    return categories
