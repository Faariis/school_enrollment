import random

pupil_ids = list(range(1, 90))
class_ids = ["VI", "VII", "VIII", "IX"]
subjects = ["MM", "ENG", "BIO", "FIZ", "INF", "HIS", "GEO", "BJZ", "NJZ", "LK",
            "MK", "HEM", "TIZO", "TK", "GOB", "VJR"]

with open("output.txt", "w") as f:
    for pupil_id in pupil_ids:
        for class_id in class_ids:
            for subject in subjects:
                if (class_id == "VI" and subject in ["HEM", "FIZ", "GOB"]) or \
                   (class_id == "VII" and subject in ["HEM", "GOB"]) or \
                   (class_id == "IX" and subject == "GOB"):
                    continue
                score = random.randint(2, 5)
                f.write(f'''
{{
    "model": "student.PupilClassesCoursesGrades",
    "fields": {{
      "pupil_id": {pupil_id},
      "class_id": "{class_id}",
      "course_code": "{subject}",
      "score": {score}
    }}
}},''')