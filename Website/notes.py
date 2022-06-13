from .sql_struct import Note
import json
from . import database
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, jsonify

notelist = Blueprint('notelist', __name__) #defines the blueprint



@notelist.route('/delete-note', methods=['POST'])
def remove_note():
    get_note = json.loads(request.data)
    get_id = get_note['noteId']
    current_note = Note.query.get(get_id)
    if current_note:
        if current_note.user_id == current_user.id:
            database.session.delete(current_note)
            database.session.commit()
            flash("Note has been deleted from your list!", category='success')
    return jsonify({})

@notelist.route('/', methods=['GET','POST']) #decorator
@login_required
def start():
    if request.method == 'POST':
        current_note = request.form.get('note')
        if len(current_note) > 1:
            create_note = Note(data=current_note, user_id=current_user.id)
            database.session.add(create_note)
            database.session.commit()
            flash('Note has been added to your list!', category='success')
        else:
            flash('The Note entered is too short. I recommend writing a longer note.', category='error')
        
    return render_template("start_page.html", user=current_user)



