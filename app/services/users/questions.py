questions_list = [
    {
        "question": "איך תרצה שנפנה אלייך? ",
        "options": ["נקבה", "זכר", "אחר"],
        "multiple": False
    },

    {
        "question": "מה הגיל שלך?",
        "options": ["פחות מ-18", "18-21", "22-30", "30-40", "41+"],
        "multiple": False
    },

    {
        "question": "מה אזור המגורים הנוכחי שלך?",
        "options": ["אזור הדרום", "אזור הצפון", "אזור תל אביב והמרכז", "אזור ירושלים", "אזור חיפה"],
        "multiple": True
    },

    {
        "question": "מה הסטטוס המשפחתי שלך?",
        "options": ["רווק/ה", "בזוגיות" ,"נשוי/נשואה", "גרוש/ה", "אלמן/ה", "אחר"],
        "multiple": False
    },

    {
        "question": "האם אתה מגדיר את עצמך כרוחני? ",
        "options": ["כן", "לא", "לא בטוח"],
        "multiple": False
    },

    {
        "question": "האם היית בטיפול בעבר / נמצא כרגע בטיפוך? ",
        "options": ["הייתי מטופל בעבר", "אני מטופל כרגע", "לא הייתי בטיפול"],
        "multiple": False
    },

    {
        "question": "מה הוביל אותך להירשם לאפלקציה שלנו? ",
        "options": ["תחושת חרדה", "תחושת דיכאון", "מצב הרוח שלי מפריע לי ביום יום", "אני מתקשה ליצור חיבור אישי", "אני מתאבל", "חוויתי טאראומה", "אני צריך לדבר עם מישהו שלא מכיר אותי אישית", "אני רוצה לצבור ביטחון", "המליצו לי להירשם", "אחר"],
        "multiple": True
    },

    {
        "question": "מה הציפיות שלך מאיתנו? ",
        "options": ["לקבל משוב מיידי לשאלות", "למצוא אנשים לדבר איתם", "אני לא יודע", "אחר"],
        "multiple": True
    },

    {
        "question": "האם אתה חווה כרגע דיכאון, לחץ או חרדה? ",
        "options": ["כן", "לא"],
        "multiple": False
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הרגשת הנאה או רגש חיובי? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הרגשת עצב או דיכאון? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הרגשת קושי להירדם או קושי לישון שינה רצופה? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הרגשת עייף או מוטרד? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הרגשת רע עם עצמך? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הרגשת שכל דבר הוא מאמץ עבורך? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הרגשת מפוחד שמשהו נורא עומד לקרות? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False
    },

    {
        "question": " האם אתה מרגיש שאתה מאבד עניין בדברים שפעם עניינו אותך? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כן"],
        "multiple": False
    },

    {
        "question": " האם אתה מרגיש ריחוק או ניתוק מאנשים אחרים? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כן"],
        "multiple": False
    },

    {
        "question": " האם קשה לך להרגיש רגשות חיוביים? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כן"],
        "multiple": False
    },

    {
        "question": "האם לקחת איזשהו סיכון או עשית דברים שיכולים להזיק לעצמך? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כן"],
        "multiple": False
    },

    {
        "question": " האם קשה לך להתרכז? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כן"],
        "multiple": False
    },

    {
        "question": "איזה סוג של חוויות או תחושות את/ה מרגיש/ה שהכי קשה לך להתמודד איתן?",
        "options": ["פחדים או חרדות", "עצב או דיכאון", "קושי במערכות יחסים", "תחושת ניתוק מהמציאות", "תחושות אחרות"],
        "multiple": True
    },

    {
        "question": "איך את/ה מתמודד/ת בדרך כלל עם מצבים קשים?",
        "options": ["מדבר/ת עם אחרים", "מתכנס/ת בתוך עצמי", "משתמש/ת בפעילות גופנית או יצירתית", "נעזר/ת בטיפול מקצועי", "אחר"],
        "multiple": True
    },

    {
        "question": "מהי הסביבה שאת/ה מרגיש/ה בה הכי בנוח לשתף חוויות?",
        "options": ["קבוצה קטנה ואינטימית", "שיחה אחד על אחד", "במרחב אנונימי", "אני לא מרגיש/ה בנוח לשתף"],
        "multiple": True
    },

    {
        "question": " כמה טוב אתה מרגיש עם עצמך? ",
        "options": ["בכלל לא", "יחסית טוב", "טוב", "טוב מאוד"],
        "multiple": False
    },

    {
        "question": "מהי רמת הפתיחות שלך לשיתוף פעולה עם אנשים חדשים?",
        "options": ["מאוד פתוח/ה", "פתוח/ה במידה מסוימת", "פחות פתוח/ה", "לא פתוח/ה בכלל"],
        "multiple": False
    },

    {
        "question": "איזה סוג של חיבור נראה לך מתאים לך יותר?",
        "options": ["אנשים בעלי חוויות דומות מאוד לשלי", "אנשים שנמצאים בשלבים דומים בהתמודדות", "אנשים עם גישות שונות שיכולות לעזור לי", "לא בטוח/ה"],
        "multiple": True
    },

    {
        "question": "האם אתה עובד כרגע? ",
        "options": ["כן", "לא", "בעבודות מזדמנות מדי פעם"],
        "multiple": False
    },

    {
        "question": "איך היית מגדיר את הרגלי השינה שלך? ",
        "options": ["טעון שיפור", "בסדר", "טוב מאוד"],
        "multiple": False
    },

    {
        "question": "אילו כלים אתה חושב שיעזרו לך? ",
        "options": ["חיבור אישי לאנשים שחווים/חוו חווית דומות לשלי", "קבלת מענה לשאלות בחיי היום-יום", "שיתוף בפלטרפומה חברתית", "אני לא יודע", "אחר"],
        "multiple": True
    },
    
    {
        "question": "תדרג את מצבך באופן כללי ",
        "options": ["מצבי רוח משתנים","הכי נורא שאפשר", "בסדר", "מעולה"],
        "multiple": False
    },

    {
        "question": " עד כמה אתה מצליח לשלוט ברגשותיך ולא נותן להם לשלוט בך? ",
        "options": ["בכלל לא מצליח", "בקושי", "יחסית מצליח", "ממש מצליח"],
        "multiple": False
    },

    {
        "question": " עד כמה הקשר שלך עם אחרים קרוב ומשמעותי? ",
        "options": ["בכלל לא", "קרוב יחסית", "קרוב מאוד"],
        "multiple": False
    },

    {
        "question": "האם חווית אירוע טראומטי?",
        "options": ["כן", "לא"],
        "multiple": False
    },
]

questions_with_trauma = [
    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הגיעו אלייך זיכרונות/חלומות טורדניים ולא רצויים של חוויה טראומתית? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False,
        "trauma": True
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הרגשת שהטראומה שחווית קורית שוב? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False,
        "trauma": True
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הרגשת מצוקה כאשר משהו הזכיר לך את החוויה הטראומטית? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False,
        "trauma": True
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים מנעת מעצמך לחשוב או להרגיש דברים שמזכירים לך את החוויה הטראומטית? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False,
        "trauma": True
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הרגשת שאתה נמנע מלהיפגש עם אנשים שמזכירים לך את החוויה הטראומטית? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False,
        "trauma": True
    },

    {
        "question": " באיזה תדירות במהלך השבועיים האחרונים הרגשת שאתה לא זוכר חלקים חשובים מתוך החוויה הטראומטית? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False,
        "trauma": True
    },

    {
        "question": " באיזה תדירות אתה מרגיש שמישהו אשם על מה שקרה באירוע או אחריו? ",
        "options": ["בכלל לא", "פעמים מעטות", "יחסית הרבה", "כמעט כל יום"],
        "multiple": False,
        "trauma": True
    },



]


photo_girl = [
        {
            "question": "תבחרי עבורך תמונה :)",
            "options": ["girl_avatar1.png", "girl_avatar2.png", "girl_avatar3.png", "girl_avatar4.png", "girl_avatar5.png", "girl_avatar6.png", "girl_avatar7.png", "girl_avatar8.png", "girl_avatar9.png", "girl_avatar10.png", "girl_avatar11.png", "girl_avatar12.png"],
            "multiple": False,
            "trauma": False
        }
]

photo_boy = [
        {
            "question": "תבחר עבורך תמונה :)",
            "options": ["boy_avatar1.png", "boy_avatar2.png", "boy_avatar3.png", "boy_avatar4.png", "boy_avatar5.png", "boy_avatar6.png", "boy_avatar7.png", "boy_avatar8.png" ],
            "multiple": False,
            "trauma": False
        }
]