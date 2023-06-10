from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def update_weekly_leaderboard(db, user_uid, username, imgUrl, points):
    today = datetime.now().date()
    current_week_start = today - timedelta(days=today.weekday())
    current_week_end = current_week_start + timedelta(days=6)

    week_id = f"{current_week_start.strftime('%d-%m-%Y')}_{current_week_end.strftime('%d-%m-%Y')}"
    print(week_id)

    doc_ref = db.collection('weekly-leaderboard').document(week_id)

    leaderboard_doc = doc_ref.get()

    if leaderboard_doc.exists:
        leaderboard = leaderboard_doc.get('leaderboard')
        new_entry = {
            'user_uid': user_uid,
            'username': username,
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
            'imgUrl': imgUrl,
            'point': points
        }

        leaderboard = [new_entry]

        doc_ref.set({
            '_id': week_id,
            'weekStartDate': current_week_start.strftime('%d-%m-%Y'),
            'weekEndDate': current_week_end.strftime('%d-%m-%Y'),
            'leaderboard': leaderboard
        })


def update_monthly_leaderboard(db, user_uid, username, imgUrl, points):
    today = datetime.now().date()
    current_month_start = today.replace(day=1)
    current_month_end = (current_month_start + relativedelta(months=1) - timedelta(days=1))

    month_id = current_month_start.strftime('%m-%Y')
    print(month_id)

    doc_ref = db.collection('monthly-leaderboard').document(month_id)

    leaderboard_doc = doc_ref.get()

    if leaderboard_doc.exists:
        leaderboard = leaderboard_doc.get('leaderboard')
        new_entry = {
            'user_uid': user_uid,
            'username': username,
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
