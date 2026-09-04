"""
load_sql_data.py
----------------
Reads data from sandip_karmakar_data.sql and returns a structured Python dictionary.
No MySQL server needed – pure Python parsing of the INSERT statements.
"""

import re
from pathlib import Path
from datetime import datetime, timedelta
from calendar import monthrange

SQL_FILE = Path(__file__).parent / "sandip_karmakar_data.sql"


# ============================================================
# DURATION HELPERS
# ============================================================
def calc_duration(start_date: str, end_date: str = None, *, include_days: bool = True) -> str:
    if not start_date:
        return ""

    def parse_date(s: str):
        s = (s or "").strip()
        if not s or s.lower() in ("till date", "present", "current", "ongoing", "onging", "—", "-", "na", "n/a"):
            return datetime.now()
        if len(s) >= 3 and s[:2] == "00" and s[2] in "/-":
            s = "01" + s[2:]
        for fmt in (
            "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
            "%m/%Y", "%m-%Y",
            "%B %Y", "%b %Y",
            "%Y",
            "%d %B %Y", "%d %b %Y",
        ):
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                continue
        return None

    start = parse_date(start_date)
    end = parse_date(end_date) if end_date is not None else datetime.now()

    if not start or not end or end < start:
        return ""

    years = end.year - start.year
    months = end.month - start.month
    days = end.day - start.day

    if days < 0:
        months -= 1
        prev_month_days = 31 if end.month == 1 else monthrange(end.year, end.month - 1)[1]
        days += prev_month_days

    if months < 0:
        years -= 1
        months += 12

    parts = []
    if years:
        parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months:
        parts.append(f"{months} month{'s' if months != 1 else ''}")
    if include_days and days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")

    return " ".join(parts) if parts else "Less than a day"


def _calc_duration(doj: str, dor: str) -> str:
    return calc_duration(doj, dor, include_days=True)


def _total_duration(items: list, duration_key: str = "duration") -> str:
    total_years = total_months = total_days = 0

    for item in items:
        d = item.get(duration_key) or ""
        parts = d.lower().replace("years", "year").replace("months", "month").replace("days", "day").split()
        for i, part in enumerate(parts):
            if str(part).isdigit() and i + 1 < len(parts):
                value = int(part)
                unit = parts[i + 1]
                if unit == "year":
                    total_years += value
                elif unit == "month":
                    total_months += value
                elif unit == "day":
                    total_days += value

    while total_days >= 30:
        total_days -= 30
        total_months += 1
    while total_months >= 12:
        total_months -= 12
        total_years += 1

    out = []
    if total_years:
        out.append(f"{total_years} year{'s' if total_years != 1 else ''}")
    if total_months:
        out.append(f"{total_months} month{'s' if total_months != 1 else ''}")
    if total_days:
        out.append(f"{total_days} day{'s' if total_days != 1 else ''}")
    return " ".join(out) if out else "—"


def _is_within_last_year(date_str: str) -> bool:
    if not date_str:
        return False
    s = str(date_str).strip().lower()
    if s in ("till date", "present", "current", "ongoing", "onging", "—", "-", "na", "n/a"):
        return True

    now = datetime.now()
    one_year_ago = now - timedelta(days=365)

    if len(s) >= 3 and s[:2] == "00" and s[2] in "/-":
        s = "01" + s[2:]

    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%m/%Y", "%m-%Y", "%B %Y", "%b %Y", "%Y"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt >= one_year_ago
        except ValueError:
            continue
    return False


def _is_recent(date_str) -> bool:
    if not date_str:
        return False
    s = str(date_str).strip().lower()
    if s in ("ongoing", "till date", "present", "current", "onging"):
        return True
    return _is_within_last_year(date_str)


# ============================================================
# SQL PARSING HELPERS
# ============================================================
def _clean(value: str):
    value = value.strip()
    if value.upper() == "NULL":
        return None
    if value.upper() == "TRUE":
        return True
    if value.upper() == "FALSE":
        return False
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        value = value[1:-1]
    value = value.replace("''", "'")
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        return int(value)
    return value


def _parse_values_block(block: str) -> list:
    values = []
    current = []
    in_quote = False
    quote_char = None
    i = 0
    text = block.strip()

    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]

    while i < len(text):
        char = text[i]
        if not in_quote:
            if char in ("'", '"'):
                in_quote = True
                quote_char = char
                current.append(char)
            elif char == ",":
                values.append(_clean("".join(current).strip()))
                current = []
            else:
                current.append(char)
        else:
            current.append(char)
            if char == quote_char:
                if i + 1 < len(text) and text[i + 1] == quote_char:
                    current.append(text[i + 1])
                    i += 1
                else:
                    in_quote = False
                    quote_char = None
        i += 1

    if current:
        values.append(_clean("".join(current).strip()))
    return values


def _find_insert_blocks(sql_content: str, table_name: str) -> list[str]:
    pattern = rf"INSERT\s+INTO\s+{table_name}\s*\([^)]*\)\s*VALUES\s*"
    blocks = []
    for m in re.finditer(pattern, sql_content, re.IGNORECASE | re.DOTALL):
        start = m.end()
        i = start
        in_quote = False
        quote_char = None
        while i < len(sql_content):
            char = sql_content[i]
            if not in_quote:
                if char in ("'", '"'):
                    in_quote = True
                    quote_char = char
                elif char == ";":
                    blocks.append(sql_content[start:i])
                    break
            else:
                if char == quote_char:
                    if i + 1 < len(sql_content) and sql_content[i + 1] == quote_char:
                        i += 1
                    else:
                        in_quote = False
                        quote_char = None
            i += 1
    return blocks


def _extract_inserts(sql_content: str, table_name: str) -> list[list]:
    blocks = _find_insert_blocks(sql_content, table_name)
    rows = []
    for text in blocks:
        groups = []
        depth = 0
        start = None
        in_quote = False
        quote_char = None
        i = 0
        while i < len(text):
            char = text[i]
            if not in_quote:
                if char in ("'", '"'):
                    in_quote = True
                    quote_char = char
                elif char == "(":
                    if depth == 0:
                        start = i
                    depth += 1
                elif char == ")":
                    depth -= 1
                    if depth == 0 and start is not None:
                        groups.append(text[start:i + 1])
                        start = None
            else:
                if char == quote_char:
                    if i + 1 < len(text) and text[i + 1] == quote_char:
                        i += 1
                    else:
                        in_quote = False
                        quote_char = None
            i += 1
        for group in groups:
            row = _parse_values_block(group)
            if row:
                rows.append(row)
    return rows


# ============================================================
# MAIN LOADER
# ============================================================
def load_data_from_sql(sql_path: str | Path = SQL_FILE) -> dict:
    sql_path = Path(sql_path)
    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    content = sql_path.read_text(encoding="utf-8")

    # ---------- 1. PERSONAL DETAILS ----------
    personal_rows = _extract_inserts(content, "personal_details")
    p = personal_rows[0] if personal_rows else [None] * 29
    personal = {
        "profile_image": p[0],
        "page_background": p[1],
        "logo": p[2],
        "name": p[3],
        "current_designation": p[4],
        "current_department": p[5],
        "current_organization": p[6],
        "current_address": p[7],
        "gender": p[8],
        "dob": p[9],
        "home_add": p[10],
        "phone1": f"{p[11]} {p[12]}" if p[11] and p[12] else None,
        "phone2": f"{p[13]} {p[14]}" if p[13] and p[14] else None,
        "email1": p[15],
        "email2": p[16],
        "portfolio": p[17],
        "github": p[18],
        "linkedin": p[19],
        "scholar": p[20],
        "orcid": p[21],
        "researchgate": p[22],
        "resume_link": p[23],
        "father": p[24],
        "mother": p[25],
        "siblings": p[26],
        "siblings_name": p[27],
        "spouse": p[28],
    }

    # ---------- 1.1 HOBBIES ----------
    hobby_rows = _extract_inserts(content, "hobbies")
    hobbies = [r[0] for r in hobby_rows]

    # ---------- 1.2 LANGUAGES ----------
    lang_rows = _extract_inserts(content, "languages")
    languages = []
    for r in lang_rows:
        languages.append({
            "name": r[1],
            "level": r[2],
            "read": bool(r[3]),
            "write": bool(r[4]),
            "speak": bool(r[5]),
        })

    # ---------- 2. EDUCATION ----------
    edu_rows = _extract_inserts(content, "education")
    education = []
    for r in edu_rows:
        start, end = r[6], r[7]
        education.append({
            "sl": r[0],
            "level": r[1],
            "degree": r[2],
            "school": r[3],
            "board": r[4],
            "stream": r[5],
            "start": start,
            "end": end,
            "duration": _calc_duration(start, end),
            "yop": r[8] or "—",
            "score": r[11],
            "thesis": r[12],
            "supervisor": r[13],
            "abstract": r[14],
            "link": r[15],
            "address": r[16],
        })
    education.sort(key=lambda x: x["sl"] if x.get("sl") is not None else 0, reverse=True)
    total_education_duration = _total_duration(education)

    # ---------- 3. EXPERIENCE ----------
    exp_rows = _extract_inserts(content, "experience")
    experience = []
    for r in exp_rows:
        doj, dor = r[4], r[5]
        experience.append({
            "sl": r[0],
            "position": r[1],
            "organization": r[2],
            "department": r[3],
            "doj": doj,
            "dor": dor,
            "duration": _calc_duration(doj, dor),
            "job_type": r[6],
            "salary": r[7],
            "responsibilities": r[8],
            "other": r[9],
            "org_link": r[10],
            "org_add": r[11],
        })
    experience.sort(key=lambda x: x["sl"] or 0, reverse=True)
    total_duration = _total_duration(experience)

    # ---------- 4. INDUSTRIAL TRAINING ----------
    train_rows = _extract_inserts(content, "industrial_training")
    training = []
    for r in train_rows:
        start, end = r[6], r[7]
        training.append({
            "sl": r[0],
            "topic": r[1],
            "topic_display": r[2],
            "topic_description": r[3],
            "org": r[4],
            "org_add": r[5],
            "start": start,
            "end": end,
            "duration": _calc_duration(start, end),
        })
    training.sort(key=lambda x: x["sl"] or 0, reverse=True)
    total_training_duration = _total_duration(training)

    # ---------- 5. PUBLICATIONS ----------
    pub_rows = _extract_inserts(content, "publications")
    publications = []
    for r in pub_rows:
        if r[2] == "TBA":
            continue
        publications.append({
            "sl": r[0],
            "type": r[1],
            "title": r[2],
            "authors": r[3],
            "venue": r[4],
            "doi": r[5],
            "status": r[6],
            "link": r[7],
        })
    publications.sort(key=lambda x: x.get("sl") or 0, reverse=True)

    # ---------- 6. PROJECTS ----------
    proj_rows = _extract_inserts(content, "projects")
    projects = []
    for r in proj_rows:
        start, end = r[7], r[8]
        projects.append({
            "sl": r[0],
            "title": r[1],
            "proj_display": r[2],
            "supervisor": r[3],
            "abstract": r[4],
            "tools": r[5],
            "status": r[6],
            "start": start,
            "end": end,
            "duration": _calc_duration(start, end),
        })
    projects.sort(key=lambda x: x["sl"] or 0, reverse=True)
    total_projects_duration = _total_duration(projects)

    # ---------- 7. ACHIEVEMENTS ----------
    ach_rows = _extract_inserts(content, "achievements")
    achievements = []
    for r in ach_rows:
        achievements.append({
            "sl": r[0],
            "title": r[1],
            "category": r[2],
            "status": r[3],
            "description": r[4],
            "organization": r[5],
            "location": r[6],
            "start": r[7],
            "end": r[8],
            "link": r[9],
        })
    achievements.sort(key=lambda x: x["sl"] or 0)

    # ============================================================
    # RECENT UPDATES – last 1 year from ALL tables
    # ============================================================
    recent_updates = []

    def _add_update(title, status, description, organization=None, location=None,
                    start=None, end=None, link=None, category="Update", icon="fa-award"):
        recent_updates.append({
            "title": title,
            "status": status,
            "description": description,
            "organization": organization,
            "location": location,
            "start": start,
            "end": end,
            "link": link,
            "category": category,
            "icon": icon,
        })

    # 1) Achievements
    for ach in achievements:
        if _is_recent(ach.get("start")) or _is_recent(ach.get("end")):
            _add_update(
                title=ach.get("title"),
                status=ach.get("status") or "Update",
                description=ach.get("description"),
                organization=ach.get("organization"),
                location=ach.get("location"),
                start=ach.get("start"),
                end=ach.get("end"),
                link=ach.get("link"),
                category=ach.get("category") or "Achievement",
                icon={
                    "Exam": "fa-medal",
                    "Position": "fa-briefcase",
                    "Publication": "fa-file-circle-check",
                    "Teaching": "fa-chalkboard-user",
                    "Training": "fa-laptop-code",
                    "Education": "fa-user-graduate",
                }.get(ach.get("category"), "fa-award"),
            )

    # 2) Education (any within last 1 year)
    for edu in education:
        if _is_recent(edu.get("start")) or _is_recent(edu.get("end")):
            status = "Ongoing" if str(edu.get("end") or "").lower() in ("ongoing", "till date", "present", "onging") else "Completed"
            _add_update(
                title=str(edu.get("degree") or edu.get("level") or "Education"),
                status=status,
                description=f"{edu.get('degree')} in {edu.get('stream')} at {edu.get('school')}"
                            + (f" under {edu.get('supervisor')}" if edu.get("supervisor") else "") + ".",
                organization=edu.get("school"),
                start=edu.get("start"),
                end=edu.get("end"),
                link=edu.get("link"),
                category="Education",
                icon="fa-user-graduate",
            )

    # 3) Experience
    for exp in experience:
        if _is_recent(exp.get("doj")) or _is_recent(exp.get("dor")):
            status = "Ongoing" if str(exp.get("dor") or "").lower() in ("ongoing", "till date", "present", "onging") else "Completed"
            _add_update(
                title=exp.get("position"),
                status=status,
                description=exp.get("responsibilities"),
                organization=exp.get("organization"),
                start=exp.get("doj"),
                end=exp.get("dor"),
                link=exp.get("org_link"),
                category="Position",
                icon="fa-briefcase",
            )

    # 4) Industrial Training
    for t in training:
        if _is_recent(t.get("start")) or _is_recent(t.get("end")):
            _add_update(
                title=t.get("topic"),
                status="Completed",
                description=t.get("topic_description") or t.get("topic"),
                organization=t.get("org"),
                location=t.get("org_add"),
                start=t.get("start"),
                end=t.get("end"),
                category="Training",
                icon="fa-laptop-code",
            )

    # 5) Publications (current year + previous year)
    current_year = datetime.now().year
    last_year = current_year - 1

    for pub in publications:
        status = (pub.get("status") or "").lower()
        venue = ((pub.get("venue") or "") + " " + (pub.get("title") or "")).lower()

        if status in ("published", "accepted", "under review") and (
            str(current_year) in venue or str(last_year) in venue
        ):
            _add_update(
                title="Paper " + (pub.get("status") or "Update"),
                status=pub.get("status"),
                description=pub.get("title"),
                organization=pub.get("venue"),
                link=pub.get("link"),
                category="Publication",
                icon="fa-file-circle-check",
            )

    # 6) Projects
    for proj in projects:
        if _is_recent(proj.get("start")) or _is_recent(proj.get("end")):
            status = proj.get("status") or (
                "Ongoing" if str(proj.get("end") or "").lower() in ("ongoing", "till date", "present", "onging") else "Completed"
            )
            desc = proj.get("abstract") or proj.get("title")
            if desc and len(desc) > 180:
                desc = desc[:180] + "..."
            _add_update(
                title=proj.get("title"),
                status=status,
                description=desc,
                organization=proj.get("supervisor"),
                start=proj.get("start"),
                end=proj.get("end"),
                category="Project",
                icon="fa-laptop-code",
            )

    # Remove duplicates
    seen = set()
    unique_updates = []
    for u in recent_updates:
        key = (str(u.get("title") or "").strip().lower(), str(u.get("organization") or "").strip().lower())
        if key not in seen:
            seen.add(key)
            unique_updates.append(u)

    # Sort by newest date first (Option B)
    def _parse_sort_date(u):
        for key in ("end", "start"):
            val = u.get(key)
            if not val:
                continue
            s = str(val).strip().lower()
            if s in ("ongoing", "till date", "present", "current", "onging"):
                return datetime.now()
            if len(s) >= 3 and s[:2] == "00" and s[2] in "/-":
                s = "01" + s[2:]
            for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%B %Y", "%b %Y", "%Y"):
                try:
                    return datetime.strptime(s, fmt)
                except ValueError:
                    continue
        return datetime.min

    recent_updates = sorted(unique_updates, key=_parse_sort_date, reverse=True)[:10]

    # ---------- RETURN ----------
    return {
        "personal": personal,
        "experience": experience,
        "total_experience_duration": total_duration,
        "training": training,
        "total_training_duration": total_training_duration,
        "education": education,
        "total_education_duration": total_education_duration,
        "projects": projects,
        "total_projects_duration": total_projects_duration,
        "publications": publications,
        "languages": languages,
        "hobbies": hobbies,
        "achievements": achievements,
        "recent_updates": recent_updates,
    }


if __name__ == "__main__":
    data = load_data_from_sql()
    print("✅ Data loaded successfully from sandip_karmakar_data.sql\n")
    print("Name         :", data["personal"]["name"])
    print("Experience   :", len(data["experience"]))
    print("Education    :", len(data["education"]))
    print("Projects     :", len(data["projects"]))
    print("Publications :", len(data["publications"]))
    print("Achievements :", len(data["achievements"]))
    print("Recent Updates:", len(data["recent_updates"]))
    print("Languages    :", [l["name"] for l in data["languages"]])
    print("Hobbies      :", data["hobbies"])
    print("\n--- Recent Updates (newest first) ---")
    for u in data["recent_updates"]:
        print(f" • [{u['status']}] {u['title']}")