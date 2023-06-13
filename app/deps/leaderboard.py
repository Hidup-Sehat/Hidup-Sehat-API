from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from app.deps.firebase import db

def get_week_id() -> str:
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return f"{start_of_week.strftime('%d-%m-%Y')}_{end_of_week.strftime('%d-%m-%Y')}"

def get_month_id() -> str:
    today = datetime.now().date()
    month_year = today.strftime('%m-%Y')
    return month_year

def update_total_points(user_uid: str, points: int) -> int:
    user_ref = db.collection('users').document(user_uid)
    doc_snapshot = user_ref.get()

    if doc_snapshot.exists:
        data = doc_snapshot.to_dict()
        current_total_points = data.get('totalPoints', 0)
        new_total_point = current_total_points + points

        try:
            user_ref.update({
                'totalPoints': new_total_point
            })
            return new_total_point
        except ValueError as e:
            raise ValueError(str(e))
    else:
        raise ValueError("User not found")

def update_weekly_points(user_uid: str, weekly_point_id: str, points: int) -> int:
    user_ref = db.collection('users').document(user_uid)
    weekly_points_ref = user_ref.collection("weekly-points").document(weekly_point_id)

    existing_weekly_points = 0
    combined_weekly_points = 0

    if weekly_points_ref.get().exists:
        existing_weekly_points = weekly_points_ref.get().to_dict().get("points", 0)
        combined_weekly_points = existing_weekly_points + points

    weekly_points_result = {
        "points": combined_weekly_points
    }

    weekly_points_ref.set(weekly_points_result)
    return combined_weekly_points

def update_monthly_points(user_uid: str, monthly_point_id: str, points: int) -> int:
    user_ref = db.collection('users').document(user_uid)
    monthly_points_ref = user_ref.collection("monthly-points").document(monthly_point_id)

    existing_monthly_points = 0
    combined_monthly_points = 0

    if monthly_points_ref.get().exists:
        existing_monthly_points = monthly_points_ref.get().to_dict().get("points", 0)
        combined_monthly_points = existing_monthly_points + points

    monthly_points_result = {
        "points": combined_monthly_points
    }

    monthly_points_ref.set(monthly_points_result)
    return combined_monthly_points

def update_weekly_leaderboard(user_uid, username, name, imgUrl, points):
    week_id = get_week_id()

    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    doc_ref = db.collection('weekly-leaderboard').document(week_id)

    leaderboard_doc = doc_ref.get()

    if leaderboard_doc.exists:
        leaderboard = leaderboard_doc.get('leaderboard')
        new_entry = {
            'user_uid': user_uid,
            'username': username,
            'name': name,
            'imgUrl': imgUrl,
            'point': points
        }

        existing_entry = next((entry for entry in leaderboard if entry['user_uid'] == new_entry['user_uid']), None)

        if existing_entry:
            # Update the existing entry with the new score
            existing_entry['point'] += new_entry['point']
        else:
            leaderboard.append(new_entry)

        # Sort the leaderboard by points in descending order
        leaderboard.sort(key=lambda entry: entry['point'], reverse=True)

        # Limit the leaderboard to 10 entries
        leaderboard = leaderboard[:10]

        doc_ref.update({
            'leaderboard': leaderboard
        })
    else:
        new_entry = {
            'user_uid': user_uid,
            'username': username,
            'name': name,
            'imgUrl': imgUrl,
            'point': points
        }

        leaderboard = [new_entry]

        doc_ref.set({
            '_id': week_id,
            'weekStartDate': start_of_week.strftime('%d-%m-%Y'),
            'weekEndDate': end_of_week.strftime('%d-%m-%Y'),
            'leaderboard': leaderboard
        })


def update_monthly_leaderboard(user_uid, username, name, imgUrl, points):
    today = datetime.now().date()
    current_month_start = today.replace(day=1)
    current_month_end = (current_month_start + relativedelta(months=1) - timedelta(days=1))

    month_id = current_month_start.strftime('%m-%Y')

    doc_ref = db.collection('monthly-leaderboard').document(month_id)

    leaderboard_doc = doc_ref.get()

    if leaderboard_doc.exists:
        leaderboard = leaderboard_doc.get('leaderboard')
        new_entry = {
            'user_uid': user_uid,
            'username': username,
            'name': name,
            'imgUrl': imgUrl,
            'point': points
        }

        existing_entry = next((entry for entry in leaderboard if entry['user_uid'] == new_entry['user_uid']), None)

        if existing_entry:
            # Update the existing entry with the new score
            existing_entry['point'] += new_entry['point']
        else:
            leaderboard.append(new_entry)

        # Sort the leaderboard by points in descending order
        leaderboard.sort(key=lambda entry: entry['point'], reverse=True)

        # Limit the leaderboard to 10 entries
        leaderboard = leaderboard[:10]

        doc_ref.update({
            'leaderboard': leaderboard
        })
    else:
        new_entry = {
            'user_uid': user_uid,
            'username': username,
            'name': name,
            'imgUrl': imgUrl,
            'point': points
        }

        leaderboard = [new_entry]

        doc_ref.set({
            '_id': month_id,
            'monthStartDate': current_month_start.strftime('%d-%m-%Y'),
            'monthEndDate': current_month_end.strftime('%d-%m-%Y'),
            'leaderboard': leaderboard
        })
