def classify_user_profile_from_db(answers_list):
    categories = {
        "mental_health": False,
        "anxiety": False,
        "depression": False,
        "loneliness": False,
        "sleep_issues": False,
        "trauma": False,
        "self_confidence": False,
        "emotional_regulation": False,
        "social_support": False,
        "motivation": False
    }


    answer_mapping = {
        "מה הוביל אותך להירשם לאפלקציה שלנו? ": {
            "תחושת חרדה": "anxiety",
            "תחושת דיכאון": "depression",
            "מצב הרוח שלי מפריע לי ביום יום": "mental_health",
            "אני מתקשה ליצור חיבור אישי": "loneliness",
            "אני מתאבל": "mental_health",
            "חוויתי טאראומה": "trauma",
            "אני רוצה לצבור ביטחון": "self_confidence", 
            "אני צריך לדבר עם מישהו שלא מכיר אותי אישית": "social_support"
        },

        "האם אתה חווה כרגע דיכאון, לחץ או חרדה? ": {
            "כן": ["mental_health", "anxiety"]
        },

        " באיזה תדירות במהלך השבועיים האחרונים הרגשת עצב או דיכאון? ": {
            "יחסית הרבה": "depression",
            "כמעט כל יום": "depression"
        },

        " באיזה תדירות במהלך השבועיים האחרונים הרגשת רע עם עצמך? ": {
            "יחסית הרבה": "self_confidence",
            "כמעט כל יום": "self_confidence"
        },

        " האם אתה מרגיש שאתה מאבד עניין בדברים שפעם עניינו אותך? ": {
            "יחסית הרבה": "motivation",
            "כן": "motivation"
        },


        " באיזה תדירות במהלך השבועיים האחרונים הרגשת מפוחד שמשהו נורא עומד לקרות? ": {
            "יחסית הרבה": "anxiety",
            "כמעט כל יום": "anxiety"
        },

        " באיזה תדירות במהלך השבועיים האחרונים הרגשת קושי להירדם או קושי לישון שינה רצופה? ": {
            "יחסית הרבה": "sleep_issues",
            "כמעט כל יום": "sleep_issues"
        },

        " באיזה תדירות במהלך השבועיים האחרונים הרגשת עייף או מוטרד? ": {
            "יחסית הרבה": "mental_health",
            "כמעט כל יום": "mental_health"
        },

        "איך היית מגדיר את הרגלי השינה שלך? ": {
            "טעון שיפור": "sleep_issues"
        },

        " האם אתה מרגיש ריחוק או ניתוק מאנשים אחרים? ": {
            "יחסית הרבה": "loneliness",
            "כן": "loneliness"
        },

        "מהי הסביבה שאת/ה מרגיש/ה בה הכי בנוח לשתף חוויות?": {
            "במרחב אנונימי": "social_support",
            "אני לא מרגיש/ה בנוח לשתף": "loneliness"
        },

        "מהי רמת הפתיחות שלך לשיתוף פעולה עם אנשים חדשים?": {
            "לא פתוח/ה בכלל": "social_support"
        },


        "האם חווית אירוע טראומטי?": {
            "כן": "trauma"
        },

        "איזה סוג טראומה חווית?": {
            "טראומה רגשית": "trauma",
            "טראומה פיזית": "trauma",
            "טראומה מינית": "trauma",
            "מלחמה/שירות צבאי": "trauma",
            "דחייה חברתית": "trauma"
        },

        " באיזה תדירות במהלך השבועיים האחרונים הגיעו אלייך זיכרונות/חלומות טורדניים ולא רצויים של חוויה טראומתית? ": {
            "יחסית הרבה": "trauma",
            "כמעט כל יום": "trauma"
        },


        "איך את/ה מתמודד/ת בדרך כלל עם מצבים קשים?": {
            "מתכנס/ת בתוך עצמי": "emotional_regulation",
            "נעזר/ת בטיפול מקצועי": "social_support"
        },

        " עד כמה אתה מצליח לשלוט ברגשותיך ולא נותן להם לשלוט בך? ": {
            "בכלל לא מצליח": "emotional_regulation",
            "בקושי": "emotional_regulation"
        },


        "תדרג את מצבך באופן כללי ": {
            "הכי נורא שאפשר": "mental_health",
            "מצבי רוח משתנים": "mental_health"
        },

        "מה התחומי עניין שלך?": {
            "ספורט": "motivation",
            "מדיטציה ויוגה": "mental_health",
            "פיתוח אישי": "self_confidence"
        }
    }

    for entry in answers_list:
        question_text = entry["question"]
        answer_value = entry["answers"]

        if question_text in answer_mapping:
            category_map = answer_mapping[question_text]

            if isinstance(answer_value, list): 
                for ans in answer_value:
                    if ans in category_map:
                        category = category_map[ans]
                        if isinstance(category, list):
                            for cat in category:
                                categories[cat] = True
                        else:
                            categories[category] = True
            else: 
                if answer_value in category_map:
                    category = category_map[answer_value]
                    if isinstance(category, list):
                        for cat in category:
                            categories[cat] = True
                    else:
                        categories[category] = True
        
    return categories
